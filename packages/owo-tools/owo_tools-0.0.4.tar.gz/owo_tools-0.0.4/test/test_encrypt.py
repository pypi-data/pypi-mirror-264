#%%
from owo_tools.encrypt import encrypt
import random


def test_example_password():
    assert encrypt("password", "Hello World!") == '8\x04\x1f\x1f\x18O%\x0b\x02\r\x17R'
    
def test_decrypt():
    for i in range(100):
        # 產生隨機的密鑰
        key = ''.join([chr(random.randint(0, 255)) for i in range(10)])
        # 產生隨機的訊息
        message = ''.join([chr(random.randint(0, 255)) for i in range(10)])
        # 加密訊息
        encrypted_message = encrypt(key, message)
        # 解密訊息
        decrypted_message = encrypt(key, encrypted_message)
        # 比較解密後的訊息與原始訊息是否相同
        assert decrypted_message == message
    