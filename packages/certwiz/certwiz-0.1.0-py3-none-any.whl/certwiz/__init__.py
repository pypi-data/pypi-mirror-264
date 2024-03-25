try:
    from main import cert_wiz
except ImportError:
    from .main import cert_wiz

certwiz = cert_wiz
