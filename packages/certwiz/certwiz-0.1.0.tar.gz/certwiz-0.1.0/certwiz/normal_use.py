import os
from build_settings import BuildSettings
from main import cert_wiz

setpath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
settings = BuildSettings(setpath + '/tests_output.ini', setpath + '/tests.ini')

cert_wiz(settings)
