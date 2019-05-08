from smbus2 import SMBus
import time

localMotor = {
    "BeginA0" : 0,
    "BeginA1" : 0
}


wire = SMBus(1)
I2C_ADDR = 0x18
SA = 5  # Stepper A
SB = 6  # Stepper B
CW = 0  # 正向
CCW = 1 # 反向


# 启动单片机
def begin(addr):
    Num = 3

    wire.write_byte_data(addr, 0x00, 0x00)
    res = wire.read_i2c_block_data(addr,0x00,Num)
    print('Product ID:'+str(res[0]))
    print('Version ID:'+str(res[1]))
    print('ID:'+str(res[2]))

    print("正在启动 下位机")
    Write_Motor(addr,0x00,[ord('o'),ord('k'),ord('0')] )
    while(True):
        if( Read_Motor(addr,0x00,1)[0] == 0x10 ):
            print('OK!')
            return
        time.sleep(0.02)

def Write_Motor(addr,reg,buf):
    wire.write_i2c_block_data(addr,reg, buf)
    print('write'+str(buf))
def Read_Motor(addr,reg,Num):
    readStr = ''
    # wire.write_byte_data(addr,reg,0x00)
    readStr = wire.read_i2c_block_data(addr,reg,Num)
    print('read'+ str( [ord(x) for x in readStr]))
    return readStr

# 初始化单片机上对应的stepper motor的接口
def init(id):
    begin(addr)

    w_data = [1,0]
    if id == SA:
        Write_Motor(addr,0,w_data)
    if id == SB:
        Write_Motor(addr,16,w_data)
    
# 要启动的stepper的ID，旋转的角度（0是不停止），速度，方向
def start(id,angle,speed,dir):
    W_Data = [0,0,0,0,0]
    count = 0 
    _angle = angle*10
    if speed >1023 or speed<=0 :
        return
    speed = (1024-speed)*3+5
    if _angle % 9 <= _angle%18 :
        count = _angle / 9
        W_Data[0] = count>>8  
        W_Data[1] = count
        W_Data[2] = speed>>8  
        W_Data[3] = speed
        if id == SA:
            if dir == CW :
                Write_Motor(addr,8,W_Data)
            elif dir == CCW :
                Write_Motor(addr,9,W_Data)
            localMotor['stepperA'] = dir
        elif id == SB:
            if dir == CW :
                Write_Motor(addr,30,W_Data)
            elif dir == CCW:
                Write_Motor(addr,31,W_Data)
            localMotor['stepperB'] = dir
    else:
        count=angle/1.8
        speed = speed*2-1
        W_Data[0] = count>>8
        W_Data[1] = count
        W_Data[2] = speed>>8  
        W_Data[3] = speed
        if id == SA:
            if dir == CW :
                Write_Motor(addr,6,W_Data)
            elif dir == CCW :
                Write_Motor(addr,7,W_Data)
            localMotor['stepperA'] = dir
        elif id == SB: 
            if dir == CW :
                Write_Motor(addr,28,W_Data)
            elif dir == CCW :
                Write_Motor(addr,29,W_Data)
            localMotor['stepperB'] = dir
def getDir(id):
    if id == SA:
        return localMotor['stepperA']
    elif id == SB:
        return localMotor['stepperB']
    return None
def stop(id):
    W_Data = [1,0]
    if id == SA:
        Write_Motor(addr,32,W_Data)
    elif id == SB:
        Write_Motor(addr,33,W_Data)
id = SA
addr = I2C_ADDR

init(id)
start(id,180,1023,CW)