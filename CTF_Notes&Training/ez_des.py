from Crypto.Cipher import DES
import secrets
import string

flag = 'moectf{???}'
characters = string.ascii_letters + string.digits + string.punctuation
#string.ascii_letters包含所有大小写和小写英文字母;string.digits包含所有数字字符;string.punctuation包含所有标点符号和特殊字符!"#$%&'()*+,-./:;<=>?@[\]^_{|}~`。

key = 'ezdes'+''.join(secrets.choice(characters) for _ in range(3))
#secrets.choice(characters)：从characters中随机抽取一个
assert key[:5] == 'ezdes'
key = key.encode('utf-8')
l = 8

def encrypt(text, key):
    cipher = DES.new(key, DES.MODE_ECB)
    """DES.new()这是pycrytodome中用于初始化DES加密对象,
        ECBMODE(Electronic Codebook)模式，块大小固定，ECB模式会将明文分割成一个个8字节块。如果最后一个块不足8字节
        那么使用*填充，对每个块进行相同key独立进行加密
    """
    padded_text = text + (l - len(text) % l) * chr(len(text))
    #对text进行padding，padding内容是chr(len(text))
    data = cipher.encrypt(padded_text.encode('utf-8'))
    return data

c = encrypt(flag, key)
print('c =', c)

# c = b'\xe6\x8b0\xc8m\t?\x1d\xf6\x99sA>\xce \rN\x83z\xa0\xdc{\xbc\xb8X\xb2\xe2q\xa4"\xfc\x07'