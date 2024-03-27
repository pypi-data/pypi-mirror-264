import os

if os.environ.get('DB_TYPE', 'MYSQL').upper() == 'DM8':
    from .dm import *
else:
    from .mysql import *