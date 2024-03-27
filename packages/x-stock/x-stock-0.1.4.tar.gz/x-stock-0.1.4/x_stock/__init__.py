__version__ = '0.1.1'

def get_version():
    return __version__


from ..alarm import nine_turn
from ..data import akshare, fushare, tushare
