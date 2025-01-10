from PySide6.QtCore import QObject, Slot, Signal, Property
import os
from enum import Enum
from cipher import SM2Curve,SM2Backend

class Backend(QObject):
    inputTextGot = Signal()
    outputPathGot = Signal()
    outputTextGot = Signal()
    processFinished = Signal()
    
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
        
        self.processFinished.connect(self.flush_input_output_content)
    @Slot(bool)
    def get_enc_or_dec_choice(self,choice: bool):
        self.choice = self.Mode.enc if choice == 0 else self.Mode.dec
        
    @Slot(str)
    def get_input_filepath(self,input_path):
        print("get input filepath")
        self.input_path_ = input_path
        
        output_path = input_path[:-4] + "_output" + input_path[-4:]
        self.output_path_ = output_path[8:]
        self.outputPathGot.emit()
        
        self.input_content_ = ""
        try:
            with open(self.input_path_[8:] if "file:///" in self.input_path_ else self.input_path_ , 'r') as file:
                content = file.read()
                self.input_content_ = content
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        self.inputTextGot.emit()
    
    @Slot(str)
    def flush_input_output_content(self):
        print("flush")
        self.input_content_ = ""
        self.output_content_ = ""
        try:
            with open(self.input_path_[8:] if "file:///" in self.input_path_ else self.input_path_ , 'r') as file:
                content = file.read()
                self.input_content_ = content
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        self.inputTextGot.emit()
        
        try:
            with open(self.output_path_[8:] if "file:///" in self.output_path_ else self.output_path_ , 'r') as file:
                content = file.read()
                self.output_content_ = content
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        self.outputTextGot.emit()
        
    @Property(str,notify=inputTextGot)
    def input_content(self):
        return self.input_content_
    @Property(str,notify=outputPathGot)
    def output_path(self):
        return self.output_path_
    @Property(str,notify=outputTextGot)
    def output_content(self):
        print(self.output_content_)
        return self.output_content_
    
    @Slot()
    def start_process(self):
        # start point of backend
        print("start processing")
        
        #processing
        if self.choice == self.Mode.enc:
            print("encrypt")
            self.sm2.encrypt(self.input_path_,self.output_path_)
        elif self.choice == self.Mode.dec:
            print("decrypt")
            self.sm2.decrypt(self.input_path_,self.output_path_)
            
        #process completed
        self.processFinished.emit()