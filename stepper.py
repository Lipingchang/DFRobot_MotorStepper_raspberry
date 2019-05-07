from smbus2 import SMBus
import time

localMotor = {
    "BeginA0" : 0,
    "BeginA1" : 0
}


wire = SMBus(1)

A0 = 0x18
SA = 5
CW = 0  #正向
CCW = 1 #反向

id = SA
addr = A0

def begin(addr):
    Num = 3
    print("start ---- A0 ---- ")
    wire.write_byte_data(addr, 0x00, 0x00)
    res = wire.read_i2c_block_data(addr,0x00,Num)
    print('Product ID:'+str(res[0]))
    print('Version ID:'+str(res[1]))
    print('ID:'+str(res[2]))

    Write_Motor(addr,0x00,[ord('o'),ord('k'),ord('0')] )
    while(True):
        if( Read_Motor(addr,0x00,1) == 0x10 ):
            print('OK!')
            return
        time.sleep(0.02)

def Write_Motor(addr,reg,buf):
    wire.write_i2c_block_data(addr,reg, buf)
    print('write'+str(buf))
def Read_Motor(addr,reg,Num):
    str = ''
    wire.write_byte_data(addr,reg,0x00)
    str = wire.read_i2c_block_data(addr,Num)
    print('read'+str(str)+" [-1]:"+str(ord(str[-1])))
    return ord(str[-1])

def init():
    begin(addr)
    w_data = [1,0]
    Write_Motor(addr,0,w_data)

def start(angle,speed,dir):
    W_Data = [0,0,0,0,0]
    count = 0 
    _angle = angle*10
    speed = (1024-speed)*3+5
    if _angle % 9 <= _angle%18 :
        count = _angle / 9
        W_Data[0] = count>>8  
        W_Data[1] = count
        W_Data[2] = speed>>8  
        W_Data[3] = speed
        if dir == CW :
            Write_Motor(addr,8,W_Data)
        elif dir == CCW :
            Write_Motor(addr,31,W_Data)
        stepperADir = dir
    else:
        count=angle/1.8
        speed = speed*2-1
        W_Data[0] = count>>8
        W_Data[1] = count
        W_Data[2] = speed>>8  
        W_Data[3] = speed; 
        if dir == CW :
            Write_Motor(addr,6,W_Data)
        elif dir == CCW :
            Write_Motor(addr,7,W_Data)
        stepperADir = dir

stepperADir = 0
def getDir():
    return stepperADir


init()
start(0,1023,CW)