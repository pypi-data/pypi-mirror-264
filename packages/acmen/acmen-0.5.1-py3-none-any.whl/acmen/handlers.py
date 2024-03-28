import abc, base64, hashlib, functools, time, datetime, uuid, hmac, json, os, socket, ssl, threading, logging, tempfile
import typing
from urllib.parse import quote

import tld, requests, dns.resolver
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat import backends
from cryptography.x509 import NameOID

from .__version__ import __version__

__all__ = [
    'ChallengeHandlerBase',
    'CloudflareDnsHandler',
    'GodaddyDnsHandler',
    'AliyunDnsHandler',
    'DnspodDnsHandler',
    'HandlerSet',
    'ManualDnsHandler',
    'ManualHttpHandler',
    'FileHttpHandler',
    'TlsAlpn01Handler'
]


class ChallengeHandlerBase(abc.ABC):

    @abc.abstractmethod
    def get_handler_type(self, identifier: str) -> str:
        """Get handler type of the identifier.

        :param identifier: The identifier in the ACME authorization object.
        :return: Which type of challenge this handler can handle for this identifier.
        """
        pass

    @abc.abstractmethod
    def pre_handle(self):
        """Preserved for future use."""
        pass

    @abc.abstractmethod
    def handle(self, url, identifier, token, key_thumbprint) -> bool:
        """Process the challenge.

        :param url: The url of the challenge. This could be used for uniquely identify a challenge.
        :param identifier: The identifier value of the authorization object.
        :param token: The challenge token.
        :param key_thumbprint: The account key's thumbprint.
        :return: Whether the challenge is fulfilled.
        """
        pass

    @abc.abstractmethod
    def post_handle(self, url, identifier, token, key_thumbprint, succeed) -> bool:
        """Undo the action have been taken before to fulfill the challenge.

        :param url: The url of the challenge. This could be used for uniquely identify a challenge.
        :param identifier: The identifier value of the authorization object.
        :param token: The challenge token.
        :param key_thumbprint: The account key's thumbprint.
        :param succeed: Whether the previous challenge handling process is succeed. It should be the return value of
                        handle(), not the response of the ACME server.
        :return: Whether the process is succeeded.
        """
        pass


class Dns01Handler(ChallengeHandlerBase):
    """This class handles dns-01 challenge."""

    # A map from the challenge url to the dns provider's record id.
    def __init__(self):
        self.__record_ids = {}
        self.__resolver = dns.resolver.Resolver(configure=False)
        self.__resolver.nameservers = ['8.8.8.8', '1.1.1.1', '9.9.9.9']
        self.__resolver.retry_servfail = False

    @staticmethod
    def txt_value(token, key_thumbprint):
        """Compute the value of the TXT record.

        :param token: The token from the challenge.
        :param key_thumbprint: The thumbprint of the account key.
        :return: The desired TXT record value.
        """
        key_authz = f'{token}.{key_thumbprint}'
        key_authz = hashlib.sha256(key_authz.encode('utf8')).digest()
        return base64.urlsafe_b64encode(key_authz).decode().rstrip('=')

    def check_txt_record(self, domain: str, value: str) -> bool:
        """Query the dns server to check whether the record match the expected value.

        :param domain: The domain.
        :param value: The expected value.
        :return: whether the record match the expected value.
        """
        records = set()
        try:
            for record in self.__resolver.resolve(domain, rdtype='TXT').rrset:
                records.add(record.to_text().strip('"'))
        except dns.exception.DNSException:
            return False
        return bool(value in records)

    def get_handler_type(self, identifier: str):
        return 'dns-01'

    def pre_handle(self):
        pass

    def handle(self, url, identifier, token, key_thumbprint) -> bool:
        # TODO: Check the validity of the token.
        # possibly, token = re.sub(r"[^A-Za-z0-9_\-]", "_", token)
        domain = tld.get_tld(identifier, as_object=True, fix_protocol=True)
        r = self.set_record(f'_acme-challenge.{domain.subdomain}'.rstrip('.'), domain.fld, self.txt_value(token, key_thumbprint))

        if not r:
            return False

        # check dns record every 10 seconds, 600 seconds at most.
        for i in range(60):
            if self.check_txt_record(f'_acme-challenge.{identifier}'.rstrip('.'), self.txt_value(token, key_thumbprint)):
                return True
            else:
                time.sleep(10)
        return False

    def post_handle(self, url, identifier, token, key_thumbprint, succeed) -> bool:
        domain = tld.get_tld(identifier, as_object=True, fix_protocol=True)
        return self.del_record(f'_acme-challenge.{domain.subdomain}'.rstrip('.'), domain.fld,
                               self.txt_value(token, key_thumbprint), self.__record_ids.pop(url, None))

    @abc.abstractmethod
    def set_record(self, subdomain, fld, value):
        """Set a DNS TXT record to fulfill the dns-01 challenge.

        The return value of this method should be the id of the dns record. And will pass directly to the del_record
        method. If the action failed, return False.
        :param subdomain: The subdomain of the identifier value.
        :param fld: The top level domain of the identifier value.
        :param value: The value of the TXT record.
        :return: The id of the TXT record if succeeded. False if the action failed.
        """
        pass

    @abc.abstractmethod
    def del_record(self, subdomain, fld, value, record_id) -> bool:
        """Delete the DNS record set to fulfill the challenge.

        :param subdomain: The subdomain of the identifier value.
        :param fld: The top level domain of the identifier value.
        :param value: The expected value of the TXT record. If this is mismatch with dns server's record, abort the
                      action and return False.
        :param record_id: The return value of the set_record.
        :return: Whether the action is succeeded.
        """
        pass


class CloudflareDnsHandler(Dns01Handler):
    """A dns-01 handler using the cloudflare api."""

    def __init__(self, api_token: str):
        """
        :param api_token: The cloudflare token, api-key is deprecated.
        """
        super().__init__()
        self.__log = logging.getLogger(__name__)
        self.__session = requests.Session()
        self.__api_url = 'https://api.cloudflare.com/client/v4'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': f'AcmeN/{__version__}',
            'Authorization': f'Bearer {api_token}'
        }
        self.__session.headers.update(headers)

    @functools.lru_cache()
    def _get_zone_id(self, fld):
        """Get zone id of a domain.

        :param fld: the domain.
        :raises RuntimeError: If server return an unsuccessful status code.
        :raises RuntimeError: If query result is empty.
        :return: the zone id.
        """

        r = self.__session.get(f'{self.__api_url}/zones', params={'name': fld, 'match': 'all', 'status': 'active'})
        if not (r.ok and r.json()['success']):
            raise RuntimeError(f'Query zone id failed: {fld}, {r.status_code} {r.reason}, {r.text}')

        result = r.json()['result']
        if len(result) == 0:
            raise RuntimeError(f'Cannot get zone id of "{fld}", possibly it does not exist or is inactive.')
        return r.json()['result'][0]['id']

    def set_record(self, subdomain, fld, value):
        r = self.__session.post(f'{self.__api_url}/zones/{self._get_zone_id(fld)}/dns_records',
                                json={'type': 'TXT', 'name': f'{subdomain}.{fld}', 'content': value, 'ttl': 60})
        if not (r.ok and r.json()['success']):
            raise RuntimeError(f'Set record for {subdomain}.{fld} failed: {r.status_code} {r.reason}, {r.text}')
        return r.json()['result']['id']

    def del_record(self, subdomain, fld, value, record_id) -> bool:
        # delete record directly if record_id is provided.
        if record_id:
            r = self.__session.delete(f'{self.__api_url}/zones/{self._get_zone_id(fld)}/dns_records/{record_id}')
            if r.ok:
                return True
            else:
                self.__log.warning(f'Del record {subdomain}.{fld} failed: {r.status_code} {r.status_code}, {r.text}')
                return False

        # otherwise, query the record first.
        r = self.__session.get(f'{self.__api_url}/zones/{self._get_zone_id(fld)}/dns_records',
                               params={'match': 'all', 'name': f'{subdomain}.{fld}', 'content': value, 'type': 'TXT'})
        if not (r.ok and r.json()['success']):
            raise RuntimeError(f'Query record id failed: {subdomain}.{fld}, {r.status_code} {r.reason}, {r.text}')
        result = r.json()['result']
        if len(result) == 0:
            # TODO: return false, make log, and do not raise RuntimeError.
            self.__log.warning(f'No matching record found for {subdomain}.{fld}')
            return False
        else:
            return self.del_record(subdomain, fld, value, result[0]['id'])


class GodaddyDnsHandler(Dns01Handler):
    def __init__(self, api_key: str, api_secret: str):
        """A dns-01 handler using Godaddy API.

        :param api_key: The "key" of your api key.
        :param api_secret: The "secret" of your api key.
        """
        super().__init__()
        self.__session = requests.Session()
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': f'AcmeN/{__version__}',
            'Authorization': f'sso-key {api_key}:{api_secret}'
        }
        self.__session.headers.update(headers)
        self.__api_url = 'https://api.godaddy.com/v1'

    def set_record(self, subdomain, fld, value):
        payload = [
            {
                'data': value,
                'name': subdomain,
                'ttl': 600,
                'type': 'TXT'
            }
        ]
        r = self.__session.patch(f'{self.__api_url}/domains/{fld}/records', json=payload)
        if r.status_code != 200:
            raise RuntimeError(f'Set record for {subdomain}.{fld} failed: {r.status_code} {r.reason}, {r.text}')

        # Godaddy API does not have RecordID.
        return str(time.time())

    def del_record(self, subdomain, fld, value, record_id) -> bool:
        # get dns records
        r = self.__session.delete(f'{self.__api_url}/domains/{fld}/records/TXT/{subdomain}')
        if not r.ok:
            raise RuntimeError(f'Failed to delete record {subdomain.rstrip(".")}.{fld}: {r.status_code} {r.reason}, {r.text}')
        return True


class AliyunDnsHandler(Dns01Handler):
    def __init__(self, access_key_id, access_key_secret):
        """A dns-01 handler using Aliyun API.

        :param access_key_id: The AccessKey ID.
        :param access_key_secret: The AccessKey Secret.
        """
        super().__init__()
        self.__base_url = 'https://alidns.aliyuncs.com'
        self.__key_id = access_key_id
        self.__key_secret = access_key_secret + '&'
        self.__session = requests.Session()
        headers = {
            'Accept': 'application/json',
            'User-Agent': f'AcmeN/{__version__}',
        }
        self.__session.headers.update(headers)

    def __sign_request(self, req: dict):
        params = {
            'Format': 'JSON',
            'Version': '2015-01-09',
            'AccessKeyId': self.__key_id,
            'SignatureMethod': 'HMAC-SHA1',
            'Timestamp': f'{datetime.datetime.utcnow().isoformat("T", "seconds")}Z',
            'SignatureVersion': '1.0',
            'SignatureNonce': str(uuid.uuid4())
        }
        params.update(req)
        string_to_sign = [f'{quote(k, safe="~")}={quote(params[k], safe="~")}' for k in sorted(params)]
        string_to_sign = "&".join(string_to_sign)
        string_to_sign = f'POST&%2F&{quote(string_to_sign)}'
        signature = hmac.new(self.__key_secret.encode('utf8'), msg=string_to_sign.encode('utf8'),
                             digestmod='sha1').digest()
        params['Signature'] = base64.b64encode(signature)
        return params

    def set_record(self, subdomain, fld, value):
        req = {
            'Action': 'AddDomainRecord',
            'DomainName': fld,
            'RR': subdomain,
            'Type': 'TXT',
            'Value': value
        }
        req = self.__sign_request(req)
        r = self.__session.post(self.__base_url, data=req)
        if not r.ok:
            raise RuntimeError(f'Set record for {subdomain}.{fld} failed: {r.status_code} {r.reason}, {r.text}')
        return r.json()['RecordId']

    def del_record(self, subdomain, fld, value, record_id) -> bool:
        if not record_id:
            req = {
                'Action': 'DescribeDomainRecords',
                'DomainName': fld,
                'SearchMode': 'EXACT',
                'KeyWord': subdomain,
                'TypeKeyWord': 'TXT'
            }
            r = self.__session.post(self.__base_url, data=self.__sign_request(req))
            if not r.ok:
                raise RuntimeError(f'Failed to query records: {subdomain}.{fld}, {r.status_code} {r.reason} {r.text}')
            r = r.json()['DomainRecords']['Record']
            records_to_delete = [i['RecordId'] for i in r
                                 if i['RR'] == subdomain and (i['Value'] == value or value is None)]
        else:
            records_to_delete = [record_id]

        if len(records_to_delete) == 0:
            raise RuntimeError('No matching record.')

        for i in records_to_delete:
            req = {
                'Action': 'DeleteDomainRecord',
                'RecordId': i
            }
            r = self.__session.post(self.__base_url, data=self.__sign_request(req))
            if not r.ok:
                raise RuntimeError(f'Failed to delete record: {i}, {r.status_code} {r.reason} {r.text}')
        return True


class DnspodDnsHandler(Dns01Handler):
    def __init__(self, secret_id, secret_key):
        super().__init__()
        self.__session = requests.Session()
        self.__secret_id = secret_id
        self.__secret_key = secret_key

    def send_request(self, action: str, params: dict) -> requests.Response:
        timestamp = int(time.time())
        date = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Host': 'dnspod.tencentcloudapi.com',
            'X-TC-Action': action,
            'X-TC-Timestamp': str(timestamp),
            'X-TC-Version': '2021-03-23'
        }
        payload = json.dumps(params)
        canonical_request = [
            'POST',
            '/',
            '',
            ''.join([f'{i.lower()}:{headers[i].lower()}\n' for i in sorted(headers, key=str.lower)]),
            ';'.join([i.lower() for i in sorted(headers, key=str.lower)]),
            hashlib.sha256(payload.encode('utf8')).hexdigest()
        ]
        canonical_request = '\n'.join(canonical_request)

        string_to_sign = [
            'TC3-HMAC-SHA256',
            str(timestamp),
            f'{date}/dnspod/tc3_request',
            hashlib.sha256(canonical_request.encode('utf8')).hexdigest()
        ]
        string_to_sign = '\n'.join(string_to_sign)
        sign_key = hmac.new(f'TC3{self.__secret_key}'.encode(), msg=date.encode(), digestmod='sha256').digest()
        sign_key = hmac.new(sign_key, msg=b'dnspod', digestmod='sha256').digest()
        sign_key = hmac.new(sign_key, msg=b'tc3_request', digestmod='sha256').digest()
        signature = hmac.new(sign_key, msg=string_to_sign.encode(), digestmod='sha256').hexdigest()

        headers['Authorization'] = f'TC3-HMAC-SHA256 Credential={self.__secret_id}/{date}/dnspod/tc3_request, ' \
                                   f'SignedHeaders={";".join([i.lower() for i in sorted(headers, key=str.lower)])}, ' \
                                   f'Signature={signature}'
        return self.__session.post('https://dnspod.tencentcloudapi.com', data=payload, headers=headers)

    def set_record(self, subdomain, fld, value):
        params = {
            'Domain': fld,
            'RecordType': 'TXT',
            'RecordLine': '默认',
            'Value': value,
            'SubDomain': subdomain
        }
        r = self.send_request('CreateRecord', params)
        if not r.ok or 'Error' in r.json()['Response']:
            raise RuntimeError(f'Set record for {subdomain}.{fld} failed: {r.status_code} {r.reason}, {r.text}')
        return r.json()['Response']['RecordId']

    def del_record(self, subdomain, fld, value, record_id) -> bool:
        if not record_id:
            params = {
                'Domain': fld,
                'Subdomain': subdomain,
                'RecordType': 'TXT'
            }
            r = self.send_request('DescribeRecordList', params)
            if not r.ok or 'Error' in r.json()['Response']:
                raise RuntimeError(f'Failed to query records: {subdomain}.{fld}, {r.status_code} {r.reason} {r.text}')
            r = r.json()['Response']['RecordList']
            records_to_delete = [i['RecordId'] for i in r
                                 if i['Value'] == value or value is None]
        else:
            records_to_delete = [record_id]

        if len(records_to_delete) == 0:
            raise RuntimeError('No matching record.')

        for i in records_to_delete:
            r = self.send_request('DeleteRecord', {'Domain': fld, 'RecordId': i})
            if not r.ok or 'Error' in r.json()['Response']:
                raise RuntimeError(f'Failed to delete record: {i}, {r.status_code} {r.reason} {r.text}')
        return True


class HandlerSet(ChallengeHandlerBase):
    def __init__(self, default_handler: ChallengeHandlerBase = None):
        super().__init__()
        self.__default_handler = default_handler
        # map from domain to handler
        self.__handlers = {}  # type: dict[str, ChallengeHandlerBase]

    @property
    def default_handler(self) -> ChallengeHandlerBase:
        return self.__default_handler

    @default_handler.setter
    def default_handler(self, value: ChallengeHandlerBase):
        self.__default_handler = value

    def get_handler_type(self, identifier: str) -> str:
        identifier = tld.get_tld(identifier, as_object=True, fix_protocol=True).fld
        return self[identifier].get_handler_type(identifier)

    def pre_handle(self):
        pass

    def handle(self, url, identifier, token, key_thumbprint) -> bool:
        domain = tld.get_tld(identifier, as_object=True, fix_protocol=True).fld
        return self[domain].handle(url, identifier, token, key_thumbprint)

    def post_handle(self, url, identifier, token, key_thumbprint, succeed) -> bool:
        domain = tld.get_tld(identifier, as_object=True, fix_protocol=True).fld
        return self[domain].post_handle(url, identifier, token, key_thumbprint, succeed)

    def __setitem__(self, domain: str, handler: ChallengeHandlerBase):
        self.__handlers[domain] = handler

    def __getitem__(self, domain: str):
        handler = self.__handlers.get(domain, self.__default_handler)
        if handler is None:
            raise KeyError(f'No handler exist for domain: {domain}')
        return handler

    def __delitem__(self, domain):
        not_exist = []
        if self.__handlers.pop(domain, not_exist) is not_exist:
            raise KeyError(f'No handler exist for domain: {domain}')


class ManualDnsHandler(Dns01Handler):
    def set_record(self, subdomain, fld, value):
        input(f'manually set record and press ENTER:\n{subdomain}.{fld}\n{value}')
        return True

    def del_record(self, subdomain, fld, value, record_id) -> bool:
        input(f'challenge is validated, delete record and press ENTER.\n{subdomain}.{fld}\n{value}')
        return True


class Http01Handler(ChallengeHandlerBase):
    """This class handles http-01 challenges."""

    def get_handler_type(self, identifier: str) -> str:
        return 'http-01'

    def pre_handle(self):
        pass

    def handle(self, url, identifier, token, key_thumbprint) -> bool:
        return self.set_resource(identifier, token, f'{token}.{key_thumbprint}'.encode('utf8'))

    def post_handle(self, url, identifier, token, key_thumbprint, succeed) -> bool:
        return self.del_resource(identifier, token, f'{token}.{key_thumbprint}'.encode('utf8'))

    @abc.abstractmethod
    def set_resource(self, identifier, filename: str, content: bytes) -> bool:
        pass

    @abc.abstractmethod
    def del_resource(self, identifier, filename: str, content: bytes) -> bool:
        pass


class ManualHttpHandler(Http01Handler):
    def set_resource(self, identifier, filename: str, content: bytes):
        input(f'manually complete http-01 challenge for: {identifier}\n'
              f'path: /.well-known/acme-challenge/{filename}\n'
              f'filename: {filename}\n'
              f'content: {content.decode()}\n'
              f'press ENTER to continue.')
        return True

    def del_resource(self, identifier, filename: str, content: bytes):
        input(f'delete challenge file for: {identifier}\n'
              f'path: /.well-known/acme-challenge/{filename}\n'
              f'filename: {filename}\n'
              f'content: {content.decode()}\n'
              f'press ENTER to continue.')
        return True


class FileHttpHandler(Http01Handler):
    def __init__(self, base_dir: str):
        super().__init__()
        self.__base_dir = base_dir.rstrip('/\\')

    def set_resource(self, identifier, filename: str, content: bytes):
        path = os.path.join(self.__base_dir, '.well-known', 'acme-challenge', filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(content)
        return True

    def del_resource(self, identifier, filename: str, content: bytes):
        path = os.path.join(self.__base_dir, '.well-known', 'acme-challenge', filename)
        os.remove(path)
        return True


class TlsAlpn01Handler(ChallengeHandlerBase):
    def __init__(self, listen_addr: str = '0.0.0.0', listen_port: int = 443):
        """

        :param listen_addr: address to listen on
        :param listen_port: port to listen on
        """
        self.__log = logging.getLogger(__name__)
        self.__shutdown_flag = False
        self.__tls_thread = None
        self.__listen_addr = listen_addr
        self.__listen_port = listen_port

    def get_handler_type(self, identifier: str) -> str:
        return 'tls-alpn-01'

    def pre_handle(self):
        pass

    def create_acmetls1_cert(self, identifier, token, key_thumbprint) -> (bytes, bytes):
        """Create a self-signed certificate contains an acmeIdentifier extension.

        :param identifier: The identifier in the ACME authorization object.
        :param token: The token from the challenge.
        :param key_thumbprint: The thumbprint of the account key.
        :return: (private key, certificate), both in pem format.
        """

        key_authz = f'{token}.{key_thumbprint}'
        key_authz = hashlib.sha256(key_authz.encode('utf8')).digest()
        key_authz = b'\x04\x20' + key_authz  # ASN.1 OCTET STRING format

        # This key is used to complete the tls-alpn-01 challenge only.
        # So, it doesn't respect the key_generate_method setting of the acmen.
        key = rsa.generate_private_key(65537, 2048, backends.default_backend())

        subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, f'ACME Client(AcmeN/{__version__})')])

        # Generate a self-signed certificate contains an acmeIdentifier extension.
        # According to RFC 8737, Section 3, the acmeIdentifier extension must be critical.
        # And the oid of the acmeIdentifier extension is 1.3.6.1.5.5.7.1.31(RFC 5280, Section 4.2.2).
        cert = x509.CertificateBuilder() \
            .subject_name(subject) \
            .issuer_name(subject) \
            .add_extension(x509.SubjectAlternativeName([x509.DNSName(identifier)]), critical=False) \
            .add_extension(x509.UnrecognizedExtension(x509.oid.ObjectIdentifier('1.3.6.1.5.5.7.1.31'), key_authz), True) \
            .serial_number(x509.random_serial_number()) \
            .not_valid_before(datetime.datetime.utcnow()) \
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=1)) \
            .public_key(key.public_key()) \
            .sign(key, hashes.SHA256(), backends.default_backend())

        # Export the private key and certificate in pem format.
        key = key.private_bytes(serialization.Encoding.PEM,
                                serialization.PrivateFormat.TraditionalOpenSSL,
                                serialization.NoEncryption())
        cert = cert.public_bytes(serialization.Encoding.PEM)
        return key, cert

    def handle(self, url, identifier, token, key_thumbprint) -> bool:
        key, cert = self.create_acmetls1_cert(identifier, token, key_thumbprint)
        self.__tls_thread = threading.Thread(target=self.__tls_server_entry,
                                             args=(key, cert, (self.__listen_addr, self.__listen_port)),
                                             daemon=True)
        self.__tls_thread.start()
        time.sleep(5)  # wait for the server to start
        return True

    def post_handle(self, url, identifier, token, key_thumbprint, succeed) -> bool:
        self.__shutdown_flag = True
        self.__tls_thread.join()
        self.__shutdown_flag = False
        return True

    def __tls_server_entry(self, key: bytes, cert: bytes, bind_addr: typing.Tuple[str, int]):
        """Start a TLS server.

        :param bind_addr: The address to bind to. eg: ('0.0.0.0', 443)
        :param key: The private key in PEM format.
        :param cert: The certificate in PEM format.
        """

        # create a tls context using the key and cert
        # according to RFC 8737 section 4, server will use TLSv1.2 or higher
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # set alpn_protocols to acme-tls-1
        context.set_alpn_protocols(['acme-tls/1'])

        # write the key and cert to a temporary file
        key_file = tempfile.NamedTemporaryFile(delete=False)
        cert_file = tempfile.NamedTemporaryFile(delete=False)
        self.__log.debug(f'write key to {key_file.name}')
        self.__log.debug(f'write cert to {cert_file.name}')
        key_file.write(key)
        key_file.flush()
        cert_file.write(cert)
        cert_file.flush()
        key_file.close()
        cert_file.close()

        # load the key and cert from the temporary file
        context.load_cert_chain(cert_file.name, key_file.name)

        # TODO: add dual-stack support
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(bind_addr)
        listener.listen(1)
        listener.settimeout(1)
        self.__log.debug('tls server is waiting for connection')
        while not self.__shutdown_flag:
            try:
                sock, addr = listener.accept()
            except socket.timeout:
                continue

            self.__log.debug(f'accepted connection from {addr}')

            # If an ignorant client, like a browser, connected to the server during the validation process,
            # there will be a SSLError.
            try:
                sock = context.wrap_socket(sock, server_side=True)
            except ssl.SSLError as e:
                self.__log.error(f'failed to wrap socket: {e}')
            finally:
                sock.close()

        listener.close()
        self.__log.debug('tls server is shutdown')
        os.remove(key_file.name)
        os.remove(cert_file.name)
