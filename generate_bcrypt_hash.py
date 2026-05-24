import sys
try:
    import bcrypt
except ImportError as exc:
    print(f'IMPORT_ERROR: {exc}')
    sys.exit(2)
password = b'CarePlus@123'
hash_value = bcrypt.hashpw(password, bcrypt.gensalt(rounds=11)).decode('utf-8')
print(hash_value)
