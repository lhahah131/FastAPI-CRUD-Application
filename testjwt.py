import sys
from jose import jwt

before = set(sys.modules)
token = jwt.encode({'sub': 'test'}, 'secret', algorithm='HS256')
after = set(sys.modules)
print('ecdsa loaded:', any(x == 'ecdsa' or x.startswith('ecdsa.') for x in after - before))