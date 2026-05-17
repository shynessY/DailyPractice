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
