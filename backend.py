from PySide6.QtCore import QObject

class SM2Backend(QObject):
    def __init__(self):
        super().__init__()
        self.input_path = "path/to/file/plaintext.txt"
        self.output_path = self.input_path + "/output/ciphertext.txt"
        
        #参数
        self.p = 0
        self.a = 0
        self.b = 0
        self.G = 0
        self.n = 0
        self.h = 0
        
        self.k_pr = 0
        self.k_pub = 0
        
    def encrypt_block(block_num: int):
        pass 
    
    def decrypt_block(block_num: int):
        pass 
    
    def encrypt(self):
        path = self.input_path
        #读取txt文件
        
        #str -> 分组 -> str段 -> hex
        
        hex_array = [int]
        #对hex加密
        for hex in hex_array:
            encrypted_hex = self.encrypt(hex)
            hex = encrypted_hex

        #hex -> str段 -> CBC链接 -> str 
        
        #保存到 output_path 里
        output_path = self.output_path
        
        pass

    def decrypt():
        pass