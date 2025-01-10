import math
import os
from gmssl import sm3

class SM2Curve():
    def __init__(self):
        self.p = 0xFFFFFFFE_FFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_00000000_FFFFFFFF_FFFFFFFF
        self.a = 0xFFFFFFFE_FFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_00000000_FFFFFFFF_FFFFFFFC
        self.b = 0x28E9FA9E_9D9F5E34_4D5A9E4B_CF6509A7_F39789F5_15AB8F92_DDBCBD41_4D940E93
        self.Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
        self.Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
        self.n = 0x8542D69E4C044F18E8B9245BF6FF7DD297720630485628D5AE74EE7C32E79B7
        self.h = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
        self.G = (self.Gx, self.Gy)

    def generate_keypair(self):
        # 生成 SM2 密钥对
        d = int.from_bytes(os.urandom(32)) % self.n
        Px, Py = self._multiply_point(d, (self.Gx, self.Gy))
        return d, (Px, Py)

    def _point_add(self, P, Q):
        """双重加法"""
        if P == (0, 0):
            return Q
        if Q == (0, 0):
            return P

        Px, Py = P
        Qx, Qy = Q

        if Px == Qx and Py == Qy:
            return self._point_double(P)

        p = self.p
        lamb = ((Qy - Py) * pow(Qx - Px, -1, p)) % p
        x3 = (lamb * lamb - Px - Qx) % p
        y3 = (lamb * (Px - x3) - Py) % p
        return (x3, y3)

    def _point_double(self, P):
        """对于点的加法"""
        Px, Py = P

        if Py == 0:
            return (0, 0)

        p = self.p
        lamb = ((3 * Px * Px + self.a) * pow(2 * Py, -1, p)) % p
        x3 = (lamb * lamb - 2 * Px) % p
        y3 = (lamb * (Px - x3) - Py) % p
        return (x3, y3)


    def _multiply_point(self, d, P):
        """根据标量乘法计算点值"""
        result = (0, 0)  # 无穷远点
        addend = P

        while d:
            if d & 1:
                result = self._point_add(result, addend)
            addend = self._point_double(addend)
            d >>= 1

        return result

class SM2Backend():
    def __init__(self, k_pr, k_pub):

        self.curve = SM2Curve()

        self.k_pr = k_pr
        self.k_pub = k_pub

    def encrypt_block(self, block_num: int):
        while True:
            k = int.from_bytes(os.urandom(32)) % self.curve.n
            x1, y1 = self.curve._multiply_point(k, (self.curve.Gx, self.curve.Gy))
            if (y1 * y1 % self.curve.p) != ((x1 * x1 * x1 + self.curve.a * x1 + self.curve.b) % self.curve.p):
                raise Exception("Invalid C1", (x1, y1))
            x2, y2 = self.curve._multiply_point(k, self.k_pub)

            Z = (hex(x2)[2:] + hex(y2)[2:]).encode("utf-8")
            if len(Z) % 2 == 1:
                Z = Z + b'0'

            klen = math.ceil(len(hex(block_num)[2:]) / 2)
            t = sm3.sm3_kdf(Z ,klen)
            if int(t, 16) != 0:
                break
        C2 = block_num ^ int(t, 16)
        C3 = int(sm3.sm3_hash(list((hex(x2)[2:] + hex(block_num)[2:] + hex(y2)[2:]).encode("utf-8"))), 16)

        return [x1, y1, C2, C3]

    def decrypt_block(self, cipherlist: list):
        x1, y1, C2, C3 = cipherlist
        if (y1 * y1 % self.curve.p) != ((x1 * x1 * x1 + self.curve.a * x1 + self.curve.b) % self.curve.p):
            raise Exception("Invalid C1", (x1, y1))

        S = curve._multiply_point(curve.h, (x1, y1))
        if S == (0, 0):
            raise Exception("invalid public key", (x1, y1))

        x2, y2 = curve._multiply_point(self.k_pr, (x1, y1))

        Z = (hex(x2)[2:] + hex(y2)[2:]).encode("utf-8")
        if len(Z) % 2 == 1:
            Z = Z + b'0'
        klen = math.ceil(len(hex(C2)[2:]) / 2)
        t = sm3.sm3_kdf(Z, klen)
        if int(t, 16) == 0:
            raise Exception("t is zero", t)

        block_num = C2 ^ int(t, 16)

        u = int(sm3.sm3_hash(list((hex(x2)[2:] + hex(block_num)[2:] + hex(y2)[2:]).encode("utf-8"))), 16)
        if u != C3:
            raise Exception("Wrong hash")

        return block_num

    def encrypt(self,input_path,output_path):
        path = input_path
        byt_array = []
        hex_array = []
        ret_array = []
        ret_arrar_to_bytes = []
        temp_bytes = b''
        byt_Z = b'3887612864938539271238590944288822203666063777565269259181046397098621227741858415090285805853795430735950794908279233294502408668229789873746914546467267741596403575911176670361005664804708787945914987352171744766345763049890679867419169715124998566929765462281415040084752028381137083977510907764710818683642755540748942297837146936102783141562102197983276235732414156607545388449958816089993123300002867145457322920168143136652933122673858507432322755950096794988906215071353366209058043288149564680307917901380744560385883229635533689014780180929145559446483224593240044746434627839766949133036683565181019834796495444045103667797916536298349713161124766674284465564817891402514157657699175749811449603542089436926871474372237758318362172946182513432665464510746472048311673303510348598434314361339824000713679441403528519856231799308375224235277833849110207012449174823156954264316230667943706558071081717648593166395079551661030511072347733618308174953491527041186327621294934051076514639750973051673504650010541992403'
        Z = int.from_bytes(byt_Z, 'little', signed=False)
        with open(path[8:] if "file:///" in path else path, 'rb') as file:
            file.seek(0)
            while True:
                data = file.read(0x400)
                byt_array.append(data)
                if not data:
                    break

        del byt_array[len(byt_array) - 1]
        flag = False

        lenth = 0
        for b in byt_array[len(byt_array) - 1]:
            if b != b'':
                lenth+=1

        if len(byt_array) == 1:
            hex_array.append(int.from_bytes(byt_array[0], 'little',signed=False))
            ret_array.append(self.encrypt_block(hex_array[0]))
            ret_arrar_to_bytes.append([0,0,0,0])
            ret_arrar_to_bytes[0][0] = ret_array[0][0].to_bytes(length=0x20, byteorder='little', signed=False)  #
            ret_arrar_to_bytes[0][1] = ret_array[0][1].to_bytes(length=0x20, byteorder='little', signed=False)  #
            ret_arrar_to_bytes[0][2] = ret_array[0][2].to_bytes(length=lenth, byteorder='little', signed=False)  #
            ret_arrar_to_bytes[0][3] = ret_array[0][3].to_bytes(length=0x20, byteorder='little', signed=False)  #
        else:
            if lenth != 0x400:
                flag = True
            for index in range(len(byt_array)):
                if index == len(byt_array) - 1 and flag:
                    temp_bytes = ret_array[index - 1][2].to_bytes(length=0x400, byteorder='little', signed=False)
                    ret_array[index - 1][2] = int.from_bytes(temp_bytes[:lenth], 'little',signed=False)
                    byt_array[index] = temp_bytes[lenth:] + byt_array[index][:lenth]

                hex_array.append(int.from_bytes(byt_array[index], 'little', signed=False))
                
                if index == 0:
                    hex_array[index] = hex_array[index] ^ Z
                elif index == len(byt_array) - 1 and flag:
                    temp_bytes = ret_array[index - 1][2].to_bytes(length=0x400, byteorder='little', signed=False)
                    temp = int.from_bytes(temp_bytes, 'little',signed=False)
                    hex_array[index] = hex_array[index] ^ ret_array[index - 1][2]
                else:
                    hex_array[index] = hex_array[index] ^ ret_array[index - 1][2]

                ret_array.append(self.encrypt_block(hex_array[index]))

            for index in range(len(ret_array)):           
                ret_arrar_to_bytes.append([0,0,0,0])
                ret_arrar_to_bytes[index][0] = ret_array[index][0].to_bytes(length=0x20, byteorder='little', signed=False)  #
                ret_arrar_to_bytes[index][1] = ret_array[index][1].to_bytes(length=0x20, byteorder='little', signed=False)  #
                if index == len(ret_array) - 2 and flag:
                    ret_arrar_to_bytes[index][2] = ret_array[index][2].to_bytes(length=lenth, byteorder='little', signed=False)  #
                else:
                    ret_arrar_to_bytes[index][2] = ret_array[index][2].to_bytes(length=0x400, byteorder='little', signed=False)  #
                ret_arrar_to_bytes[index][3] = ret_array[index][3].to_bytes(length=0x20, byteorder='little', signed=False)  #
        path = output_path
        with open(path[8:] if "file:///" in path else path, 'wb') as file:
            for index in range(len(ret_array)):
                file.write(ret_arrar_to_bytes[index][0])  
                file.write(ret_arrar_to_bytes[index][1]) 
                file.write(ret_arrar_to_bytes[index][2])  
                file.write(ret_arrar_to_bytes[index][3])  

    def decrypt(self,input_path,output_path):
        path = input_path
        ord_array = []
        byt_array = []
        hex_array = []
        ret_array = []
        byt_Z = b'3887612864938539271238590944288822203666063777565269259181046397098621227741858415090285805853795430735950794908279233294502408668229789873746914546467267741596403575911176670361005664804708787945914987352171744766345763049890679867419169715124998566929765462281415040084752028381137083977510907764710818683642755540748942297837146936102783141562102197983276235732414156607545388449958816089993123300002867145457322920168143136652933122673858507432322755950096794988906215071353366209058043288149564680307917901380744560385883229635533689014780180929145559446483224593240044746434627839766949133036683565181019834796495444045103667797916536298349713161124766674284465564817891402514157657699175749811449603542089436926871474372237758318362172946182513432665464510746472048311673303510348598434314361339824000713679441403528519856231799308375224235277833849110207012449174823156954264316230667943706558071081717648593166395079551661030511072347733618308174953491527041186327621294934051076514639750973051673504650010541992403'
        Z = int.from_bytes(byt_Z, 'little', signed=False)
        with open(path[8:] if "file:///" in path else path, 'rb') as file:
            file.seek(0)
            while True:
                data = file.read(0x460)
                ord_array.append(data)
                if not data:
                    break
        
        del ord_array[len(ord_array) - 1]

        lenth = 0
        for b in ord_array[len(ord_array) - 1]:
            if b != b'':
                lenth+=1

        if len(ord_array) == 1:
            byt_array.append([ord_array[0][:0x20],ord_array[0][0x20:0x40],ord_array[0][0x40:lenth - 0x20],ord_array[0][lenth - 0x20:]])
            hex_array.append([int.from_bytes(byt_array[0][0], 'little', signed=False),
                              int.from_bytes(byt_array[0][1], 'little', signed=False),
                              int.from_bytes(byt_array[0][2], 'little', signed=False),
                              int.from_bytes(byt_array[0][3], 'little', signed=False)])
            ret_array.append(self.decrypt_block(hex_array[0]))
        else:
            if lenth != 0x460:
                ord_array[len(ord_array) - 1] = ord_array[len(ord_array) - 2][lenth:] + ord_array[len(ord_array) - 1][:lenth]
                ord_array[len(ord_array) - 2] = ord_array[len(ord_array) - 2][:lenth]
            for index in range(len(ord_array)):
                l = len(ord_array[index])
                byt_array.append([ord_array[index][:0x20],ord_array[index][0x20:0x40],ord_array[index][0x40:l - 0x20],ord_array[index][l - 0x20:]])
            for index in range(len(ord_array)):
                print(len(byt_array[index][0]))
                print(len(byt_array[index][1]))
                print(len(byt_array[index][2]))
                print(len(byt_array[index][3]))

            for index in range(len(ord_array)):
                hex_array.append([int.from_bytes(byt_array[index][0], 'little', signed=False),
                                int.from_bytes(byt_array[index][1], 'little', signed=False),
                                int.from_bytes(byt_array[index][2], 'little', signed=False),
                                int.from_bytes(byt_array[index][3], 'little', signed=False)])

                if index == len(byt_array) - 2 and len(byt_array[index][2]) != 0x400:
                    temp = int.from_bytes(byt_array[index][2], 'little', signed=False)
                    temp_bytes = temp.to_bytes(length=0x400, byteorder='little', signed=False)
                    ret_array.append(0)
                    ret_array.append(0)
                    hex_array.append([int.from_bytes(byt_array[index + 1][0], 'little', signed=False),
                                    int.from_bytes(byt_array[index + 1][1], 'little', signed=False),
                                    int.from_bytes(byt_array[index + 1][2], 'little', signed=False),
                                    int.from_bytes(byt_array[index + 1][3], 'little', signed=False)])
                    ret_array[index + 1] = self.decrypt_block(hex_array[index + 1])
                    ret_array[index + 1] = ret_array[index + 1] ^ int.from_bytes(temp_bytes, 'little', signed=False)
                    temp_bytes = ret_array[index + 1].to_bytes(length=0x400, byteorder='little', signed=False)
                    byt_array[index][2] = byt_array[index][2] + temp_bytes[:0x400 - len(byt_array[index][2])]
                    hex_array[index][2] = int.from_bytes(byt_array[index][2], 'little', signed=False)
                    ret_array[index] = self.decrypt_block(hex_array[index])
                    if index == 0:
                        ret_array[index] = ret_array[index] ^ Z
                    else:
                        ret_array[index] = ret_array[index] ^ hex_array[index - 1][2]
                    temp_bytes = ret_array[index + 1].to_bytes(length=0x400, byteorder='little', signed=False)
                    ret_array[index + 1] =  int.from_bytes(temp_bytes[0x460 - lenth:], 'little', signed=False)
                    break

                ret_array.append(self.decrypt_block(hex_array[index]))

                if index == 0:
                    ret_array[index] = ret_array[index] ^ Z
                else:
                    ret_array[index] = ret_array[index] ^ hex_array[index - 1][2]

        path = output_path
        with open(path[8:] if "file:///" in path else path, 'wb') as file:
            for index in range(len(ord_array)):
                if index == len(ord_array) - 1 and lenth!=0x460:
                    file.write(ret_array[index].to_bytes(length=lenth-0x60, byteorder='little', signed=False))
                else:
                    file.write(ret_array[index].to_bytes(length=0x400, byteorder='little', signed=False))


curve = SM2Curve()
k_pr, k_pub = curve.generate_keypair()
sm2 = SM2Backend(k_pr, k_pub)

if __name__ == "__main__":
    sm2.encrypt("file:///E:/qt_project/SM2/2.txt","file:///E:/qt_project/SM2/enc.txt")
    sm2.decrypt("file:///E:/qt_project/SM2/enc.txt","file:///E:/qt_project/SM2/dec.txt")