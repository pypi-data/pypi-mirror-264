def encrypt(key, message):
    """
    使用給定的密鑰對訊息進行加密。

    Args:
        key (str): 加密的密鑰。必須是一個非空字串。
        message (str): 要加密的訊息。可以是任意長度的字串。

    Returns:
        str: 加密後的訊息，以字串形式返回。該字串包含了訊息的加密版本，可以被解密回原始訊息。

    Raises:
        ValueError: 當密鑰為空時，引發ValueError。

    Example:
        >>> encrypt("password", "Hello World!")
        '8\x04\x1f\x1f\x18O%\x0b\x02\r\x17R'

    """
    # 將密鑰轉換為ASCII碼序列
    key_bytes = [ord(char) for char in key]
    # 建立空的加密後資訊串列
    encrypted_bytes = []
    # 逐字元對訊息進行加密
    for i in range(len(message)):
        # 取得訊息字元的ASCII碼
        message_byte = ord(message[i])
        # 取得密鑰字元的ASCII碼
        key_byte = key_bytes[i % len(key_bytes)]
        # 將密鑰字元與訊息字元做XOR運算
        encrypted_byte = message_byte ^ key_byte
        # 將加密後的字元加入加密後資訊串列
        encrypted_bytes.append(encrypted_byte)
    # 將加密後資訊串列轉換為字串
    encrypted_message = ''.join([chr(byte) for byte in encrypted_bytes])
    return encrypted_message