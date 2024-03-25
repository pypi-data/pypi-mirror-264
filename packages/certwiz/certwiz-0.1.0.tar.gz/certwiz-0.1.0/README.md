# CertWiz

CertWiz is a Python module that simplifies the creation of self-signed x509 certificates.

## Usage
*see normal_use.py for example*

The default settings file should contain the following keys before operation
```
[settings]
ssl_dir
ssl_key_file
ssl_cert_file
ssl_version
ssl_cert_reqs
ssl_ciphers
host
base_url
[secure]
ssl_key_file_password
```
Certwiz will populate these values if not already present using a series of defaults that may be edited after the first 
run

*ensure an existing build_settings object is passed*
```
from build_settings import BuildSettings

setpath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
settings = BuildSettings(setpath + '/tests_output.ini', setpath + '/tests.ini')
```
Import and call certwiz
```
from certwiz import certwiz

certwiz(settings)
```
The resulting configuration file *(located within the project directory)*
```
[settings]
ssl_dir = '.ssl'
base_url = localhost
use_ssl = True
ssl_key_file = '.ssl/ss.key'
ssl_cert_file = '.ssl/ss.crt'
ssl_version = ssl.PROTOCOL_SSLv23
ssl_cert_reqs = ssl.CERT_OPTIONAL
ssl_ciphers = TLSv1
host = <your ip address>
[secure]
ssl_key_file_password = 3215ddaa-4d4f-4948-bb6e-a81f94e1fbb0
```
If one wishes to use properly signed certificates, simply update the configuration to reflect those values
*(self-signed certificates and the matching configuration will only be created if the `ssl_cert_file` and `ssl_key_file`
values do not point to existing files)*

It is important to note that the self-signed certificates are **hostname specific** and may experience problems
should it be changed. This can be resolved by simple removing the self-signed certificate files and re-running certwiz

## Installation

You can install CertWiz using pip:

```bash
pip install certwiz
