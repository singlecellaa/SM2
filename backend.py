from PySide6.QtCore import QObject, Slot, Signal, Property
import os
from enum import Enum
from cipher import SM2Curve,SM2Backend

class Backend(QObject):
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
        
        curve = SM2Curve()
        k_pr, k_pub = curve.generate_keypair()
        self.sm2 = SM2Backend(k_pr, k_pub)
        
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
        
        # dir_name = os.path.dirname(input_path)
        # output_path = os.path.join(dir_name,"output.txt").replace('\\','/')
        
        output_path = input_path[:-4] + "_output" + input_path[-4:]
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
            self.sm2.encrypt(self.input_path_,self.output_path_)
        elif self.choice == self.Mode.dec:
            self.sm2.decrypt(self.input_path_,self.output_path_)
            
        #process completed
        self.outputTextGot.emit()