import os
import hashlib
import struct
# from secret import password

# 哈希函数定义
def md5(bytestring):
    return hashlib.md5(bytestring).digest()
"""
.hashlib.md5(byetstring) 返回的是一个MD5对象
.digest() hash对象的一个方法,返回类型是bytes(32字节的原始二进制数据)
MD5产生128位hash值,即16位bytes
"""

def sha(bytestring):
    return hashlib.sha1(bytestring).digest()
"""
SHA-1产生160位（20字节）的哈希值，即hashlib.sha1(bytestring).digest()返回的是一个长度位20字节字节流
从安全性以及发展来说，MD5->SHA-1->SHA-256/SHA-3

"""

def blake(bytestring):
    return hashlib.blake2b(bytestring).digest()
"""
blake2b算法，默认产生512位的哈希值（64字节）
BLAKE2是目前最安全的哈希算法之一，旨在替代MD5和SHA-1，甚至在某一方面优于SHA-3。他没有已知的严重安全漏洞。
可配置性：虽然默认输出 64 字节，但可以通过参数 digest_size 指定输出长度（1~64 字节）。
例如：hashlib.blake2b(data, digest_size=32) 会生成 32 字节的哈希。
"""

def scrypt(bytestring):
    l = int(len(bytestring) / 2)
    salt = bytestring[:l]
    p = bytestring[l:]
    return hashlib.scrypt(p, salt=salt, n=2**16, r=8, p=1, maxmem=67111936)
"""
MD5、SHA-1、BLAKE2b 是通用哈希函数（General-purpose Hash Functions）
而 scrypt 是一种密钥派生函数（Key Derivation Function, KDF）专门设计用于密码哈希（Password Hashing）
hashlib.scrypt 默认返回 64 字节 (512位) 的数据（除非指定 dklen 参数）
在这个自定义函数中他把输入的bytestring强行拆分成两半，前半部分当作salt(盐),后半部分当作password(密码)
其中hashlib.scrypt()中
n=2**16 (CPU/计算成本)：迭代次数。数值越大，计算越慢。
r=8 (块大小)：影响内存使用量。
p=1 (并行度)：并行线程数。
maxmem:允许使用的最大内存
"""

def xor(s1, s2):
    return bytes([s1[i] ^ s2[i % len(s2)] for i in range(len(s1))])

# 哈希函数映射
hash_functions = {
    'md5': md5,
    'sha': sha,
    'blake': blake,
    'scrypt': scrypt
}
class HashGenerator:
    hashes = [md5, sha, blake, scrypt]
    total_rounds = 32

    def generate_salt(self, password):
        salt_size = 128 - len(password)
        return os.urandom(salt_size)
        """
        os.urandom(salt_size) 的意思是：生成指定长度（salt_size 字节）的强随机二进制数据。
        """

    def generate_rounds(self):
        rand = struct.unpack("Q", os.urandom(8))[0]
        """
        将 8 个字节的随机二进制数据，解释为一个巨大的无符号 64 位整数。
        """
        """
        struct.unpack()返回的是一个元组(tuple)
        参数介绍:
        第一个参数:格式字符串(format)
        "Q":无符号长整型
        "i":有符号整数
        "f":浮点数
        "d"双精度浮点数
        "s":字符串/字节串
        """
        rounds = []
        for i in range(self.total_rounds):#self.total_rounds=32
            rounds.append(self.hashes[rand % len(self.hashes)])
            rand = rand >> 2
        return rounds

    def calculate_hash(self, password, salt=None, hash_rounds=None):
        if salt is None:
            salt = self.generate_salt(password)
        if hash_rounds is None:
            hash_rounds = self.generate_rounds()
            
        payload = salt + password#前面的salt生成逻辑告诉我，这里pyload长度为128
        interim_salt = payload[:64]
        interim_hash = payload[64:]
        
        for i in range(len(hash_rounds)):#hash_rounds=32
            interim_salt = xor(interim_salt, hash_rounds[-1-i](interim_hash))
            """
            salt[i]=salt[i-1]^HASH[hash[i]]
            hash[i+1]=hash[i]]^HASH[salt[i]]
            我们分析，最后结局就是这样，所以，可以利用xor性质得到
            A:
            pre_hash=final_hash^hash_rounds[31](final_salt)
            从而得到倒数第二个hash
            可以得到倒数第二个salt
            pre_salt=final_salt^hash_rounds[0](pre_hash)
            goto->A(直到32轮回溯):
            """
            interim_hash = xor(interim_hash, hash_rounds[i](interim_salt))
            
        return salt + interim_salt + interim_hash, [h.__name__ for h in hash_rounds]  # 返回名称列表
"""
if __name__ == "__main__":
    generator = HashGenerator()
    password_hash, rounds_names = generator.calculate_hash(password)
    
    print(f"password_hash={password_hash.hex()}")#bytes.hex(str)->bytes是将字节串转换为十六进制字符串，其逆操作是.fromhex()
    print(f"rounds_names={rounds_names}")
"""
'''
password_hash=0xa9a12c176f6e5c8ecabad6df0d983976eb37eeb144fc3377ce261fc67849817ab1ba2a0895c87fc4febf3f9cd2d7e3ce2254af791d31619770f3abe71c90ec83fc4fa720b45f9667e32d1f8cfb0f6c7c8614e85d9d699afae63acc5460c45e3705b2619d19b67ce05ca49043d112bea49d38d64216da97486f9ce3dabcd26d371bd0b9428740bfc9a44389d6933ef094f12b382a3fbb9bbb76e695a3106be7d7c702b8c7ded1ea1d530d8f88207926d496ad8e38b7b81bfad2b7fecb8938bf4f02430aa8e05c8985b38a028a6d98511c4a32772d4638fcd644fec0dfced13d022b450f3b4eda
rounds_names=['blake', 'md5', 'sha', 'md5', 'md5', 'sha', 'scrypt', 'blake', 'scrypt', 'sha', 'scrypt', 'scrypt', 'sha', 'scrypt', 'sha', 'md5', 'md5', 'scrypt', 'sha', 'scrypt', 'blake', 'md5', 'scrypt', 'blake', 'blake', 'sha', 'blake', 'scrypt', 'md5', 'scrypt', 'sha', 'sha']
'''














####题解
import os
import hashlib
import struct
from fakehash import md5,sha,blake,scrypt,xor
password_hash="a9a12c176f6e5c8ecabad6df0d983976eb37eeb144fc3377ce261fc67849817ab1ba2a0895c87fc4febf3f9cd2d7e3ce2254af791d31619770f3abe71c90ec83fc4fa720b45f9667e32d1f8cfb0f6c7c8614e85d9d699afae63acc5460c45e3705b2619d19b67ce05ca49043d112bea49d38d64216da97486f9ce3dabcd26d371bd0b9428740bfc9a44389d6933ef094f12b382a3fbb9bbb76e695a3106be7d7c702b8c7ded1ea1d530d8f88207926d496ad8e38b7b81bfad2b7fecb8938bf4f02430aa8e05c8985b38a028a6d98511c4a32772d4638fcd644fec0dfced13d022b450f3b4eda"
rounds_names=['blake', 'md5', 'sha', 'md5', 'md5', 'sha', 'scrypt', 'blake', 'scrypt', 'sha', 'scrypt', 'scrypt', 'sha', 'scrypt', 'sha', 'md5', 'md5', 'scrypt', 'sha', 'scrypt', 'blake', 'md5', 'scrypt', 'blake', 'blake', 'sha', 'blake', 'scrypt', 'md5', 'scrypt', 'sha', 'sha']
password_hash_bytes=bytes.fromhex(password_hash)
hashes = {  
            'md5':0,
            'sha':1, 
            'blake':2,
            'scrypt':3
          }
randMod4=[hashes[i] for i in rounds_names]
#程序到此运行没有问题
"""
根据源代码分析，之前的rand在32轮循环过后为0
for i in range(self.total_rounds):#self.total_rounds=32
    rounds.append(self.hashes[rand % len(self.hashes)])
    rand = rand >> 2
我们从数学上开始分析，其实rand>>2，即rand=rand//4
而randMod4为我们提供个位数

"""
#开始恢复rand
rand=0
for i in range(32):
    rand=rand*4+randMod4[31-i]
#检验
rounds=[]
for i in range(32):#self.total_rounds=32
    if randMod4[i] != rand % 4:
        print("error answer")
    rand = rand >> 2
#rand正确
"""
根据
return salt + interim_salt + interim_hash, [h.__name__ for h in hash_rounds]  # 返回名称列表
"""
hash_functions = [md5, sha, blake, scrypt]
final_interim_hash = password_hash_bytes[-64:]
final_interim_salt = password_hash_bytes[-128:-64]
salt=password_hash_bytes[:-128]
curr_salt = final_interim_salt
curr_hash = final_interim_hash
for i in range(31, -1, -1):
    """
    根据源代码iterim_hash,iterim_salt分别是从hash_rounds前后面尝试hash函数
    """
    prev_hash = xor(curr_hash, hash_functions[randMod4[i]](curr_salt))
    prev_salt = xor(curr_salt, hash_functions[randMod4[31 - i]](prev_hash))
    # 更新当前状态，进入前一轮
    curr_salt = prev_salt
    curr_hash = prev_hash
initial_payload = curr_salt + curr_hash
# 5. 提取密码
# payload = salt + password
password = initial_payload[len(salt):]

print(password.decode("utf-8"))
