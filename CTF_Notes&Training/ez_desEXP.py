from Crypto.Cipher import DES
import string
import itertools
c = b'\xe6\x8b0\xc8m\t?\x1d\xf6\x99sA>\xce \rN\x83z\xa0\xdc{\xbc\xb8X\xb2\xe2q\xa4"\xfc\x07'

characters = string.ascii_letters + string.digits + string.punctuation
key_prefix = b'ezdes'
for c1 in characters:
    for c2 in characters:
        for c3 in characters:
            key_str = 'ezdes' + c1 + c2 + c3
            key = key_str.encode('utf-8')
            
        
            # 初始化解密对象
            cipher = DES.new(key, DES.MODE_ECB)
            # 解密
            decrypted_padded = cipher.decrypt(c)
            if decrypted_padded.startswith(b"moectf{"):
                print(f"c1是{c1},c2是{c2},c3是{c3}")
                print(decrypted_padded)
                break