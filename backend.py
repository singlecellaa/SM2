from PySide6.QtCore import QObject, Slot, Signal, Property
import os
from enum import Enum

class SM2Backend(QObject):
    inputTextGot = Signal()
    outputPathGot = Signal()
    outputTextGot = Signal()
    
    
    def __init__(self):
        
        super().__init__()
        self.Mode = Enum("Mode",["enc","dec"])
        self.choice = self.Mode.enc #default is 0, i.e: encrypt
        self.input_path_ = ""
        self.input_content_ = ""
        self.output_path_ = ""
        self.output_content_ = ""
        
        #参数
        self.p = 0
        self.a = 0
        self.b = 0
        self.G = 0
        self.n = 0
        self.h = 0
        
        self.k_pr = 0
        self.k_pub = 0
    
    @Slot(bool)
    def get_enc_or_dec_choice(self,choice: bool):
        self.choice = self.Mode.enc if choice == 0 else self.Mode.dec
        
    @Slot(str)
    def get_input_filepath(self,input_path):
        self.input_path_ = input_path
        with open('E:/qt_project/test.txt' , 'r') as file:
            content = file.read()
            self.input_content_ = content
        self.inputTextGot.emit()
        
        dir_name = os.path.dirname(input_path)
        output_path = os.path.join(dir_name,"output.txt").replace('\\','/')
        self.output_path_ = output_path[8:]
        self.outputPathGot.emit()
        
    @Property(str,notify=inputTextGot)
    def input_content(self):
        return self.input_content_
    @Property(str,notify=outputPathGot)
    def output_path(self):
        return self.output_path_
    @Property(str,notify=outputTextGot)
    def output_content(self):
        return self.output_content_
    
    @Slot()
    def start_process(self):
        # start point of backend
        print("start processing")
        
        #processing
        if self.choice == self.Mode.enc:
            self.encrypt()
        elif self.choice == self.Mode.dec:
            self.decrypt()
            
        #process completed
        self.outputTextGot.emit()
        
    def encrypt_block(block_num: int):
        pass 
    
    def decrypt_block(block_num: int):
        pass 
    
    def encrypt(self):
        print("encrypt")
        path = self.input_path_
        return 
        #读取txt文件
        
        #str -> 分组 -> str段 -> hex
        
        hex_array = [int]
        #对hex加密
        for hex in hex_array:
            encrypted_hex = self.encrypt(hex)
            hex = encrypted_hex

        #hex -> str段 -> CBC链接 -> str 
        
        #保存到 output_path 里
        output_path = self.output_path_
        
        pass

    def decrypt(self):
        print("decrypt")
        pass