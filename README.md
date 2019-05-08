> 用python的库把arduino的库重写了部分函数，可以用raspberry运行

# 用到的py库

smbus2 <https://pypi.org/project/smbus2/>

# 下位机

<https://wiki.dfrobot.com/FireBeetle_Covers-DC_Motor_%26_Stepper_Driver_SKU_DFR0508>

# Arduino的库

<https://github.com/DFRobot/DFRobot_MotorStepper>

# 使用

- raspberry 开启i2c功能

  

- 使用 i2c-tools 查找已经在线的设备，和设备的**地址**：

  i2cdetect -l  ==> 找到当前主机上的i2c bus有几个

  i2cdetect -f -y 1 ==> 列出bus1 上的其他机器的地址

  

- 改参数

  修改py文件中`SMBus(..)`的参数，为i2c bus的值

  修改py文件中 `I2C_ADDR` 的值，为用i2cdetect找到的值，默认的值应该是0x18

  

- 根据DFrobot官网的接线图，把stepper接到板子上，然后把py文件中的`id`改成 SA 或者 SB，

  调用`init(id)`初始化stepper

  调用`start(id,angle,speed,dirction)`启动stepper

  调用`stop(id)`来停止stepper