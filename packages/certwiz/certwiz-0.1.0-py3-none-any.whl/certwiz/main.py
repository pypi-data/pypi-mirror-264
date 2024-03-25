import socket
from OpenSSL import crypto
import random
import uuid
from pathlib import Path
from build_settings import BuildSettings

REQUIRED_VALUES = [
    'ssl_dir',
    'ssl_key_file',
    'ssl_cert_file',
    'ssl_key_file_password',
    'ssl_version',
    'ssl_cert_reqs',
    'ssl_ciphers',
    'host',
    'base_url',

]


def get_netinfo() -> tuple:
    """
    This returns a tuple (hostname, ipv4 addresses)
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return socket.gethostname(), ip


def cert_wiz(settings: [BuildSettings, any]) -> [BuildSettings, any]:
    """
    This creates a default set of self-signed x509 certificates
    :param settings: Instance of BuildSettings initialised from settings.py
    """
    certs = settings.ssl_dir
    CERTS = Path(certs).expanduser()  # noqa
    if not CERTS.is_dir():
        CERTS.mkdir()
    KEY_FILE = Path(certs + '/ss.key').expanduser()  # noqa
    CERT_FILE = Path(certs + '/ss.crt').expanduser()  # noqa
    if not KEY_FILE.is_file() or not CERT_FILE.is_file():
        print('Creating self signed SSL certificates...')
        print('NOTE if using more than one application on the same system \n '
              'the passphrase must be copied inbetween settings.ini files!')
        print('NOTE it may be required to rebuild certificates in the event of a host name change.')
        KEY_FILE.touch()
        CERT_FILE.touch()
        host, ip = get_netinfo()
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 4096)
        cert = crypto.X509()
        cert.get_subject().CN = host
        suffix = str()
        if '.' not in host:
            suffix += '.local'
        cert.get_subject().emailAddress = 'admin@' + host + suffix
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        sn = random.randint(10000, 99999)
        cert.set_serial_number(sn)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)
        # noinspection PyTypeChecker
        cert.sign(key, 'sha512')
        passphrase = str(uuid.uuid4())
        with open(CERT_FILE, "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
        with open(KEY_FILE, "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key, passphrase=passphrase.encode()).decode("utf-8"))
        print('creating key_file:', passphrase)
        settings.set('ssl_key_file', "'" + KEY_FILE.as_posix() + "'")
        settings.set('ssl_cert_file', "'" + CERT_FILE.as_posix() + "'")
        settings.set_secure('ssl_key_file_password', passphrase)
        settings.set('ssl_version', 'ssl.PROTOCOL_SSLv23')
        settings.set('ssl_cert_reqs', 'ssl.CERT_OPTIONAL')
        settings.set('ssl_ciphers', 'TLSv1')
    # Setup network variables.
    try:
        net_info = get_netinfo()
        ip = net_info[1]
    except OSError as err:
        print('unable to start network listeners\n', err)
        ip = '127.0.0.1'
    settings.set('host', ip)
    if settings.base_url == 'api.mydomain.com':
        settings.set('base_url', ip)
    settings.save()

    if not settings.use_ssl:  # Remove variables if we aren't using ssl (but keep the values).
        settings.set('ssl_key_file', None)
        settings.set('ssl_cert_file', None)
        settings.set('ssl_version', None)
        settings.set('ssl_cert_reqs', None)
        settings.set('ssl_ciphers', None)
    return settings
