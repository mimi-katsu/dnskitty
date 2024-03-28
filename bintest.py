
domain = 'www.test.com'

parts = domain.split('.')

bytes_ = b''

for p in parts:
    length = len(p).to_bytes(1,'big')
    bytes_ += length
    bytes_ += p.encode()

print(bytes_)