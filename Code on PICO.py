# Import relavent modules
import machine
import time
import MPU6050
import math
import uos

# Set up the serial Comms
uart = machine.UART(0, baudrate=115200, bits = 8,parity = None,stop = 1 ,tx = machine.Pin(0),rx = machine.Pin(1))
uart.init(115200, bits=8, parity=None, stop=1, tx=machine.Pin(0), rx=machine.Pin(1))
uos.dupterm(uart)

# Set up the I2C interface
i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3), freq=400000)
led = machine.Pin("LED", machine.Pin.OUT)
flex_1 = machine.ADC(machine.Pin(26))
flex_2 = machine.ADC(machine.Pin(27))

# Checking I2C conncetions
devices = i2c.scan()
print(i2c.scan())
device_count = len(devices)
if device_count == 0:
    print('No i2c device found.')
    led.on()
else:
    print(device_count, 'devices found.')
    led.off()
    
# Set up the MPU6050 class 
mpu = MPU6050.MPU6050(i2c)

# wake up the MPU6050 from sleep
mpu.wake()
   
# Initialise variables
pGy = 0
rGy = 0
pAc = 0
rAc = 0
pClr = 0
rClr = 0
tLoop = 0


# continuously print the data
# code for the flex sensors
# code for the MPU6050, pitch roll and yaw
while True:
    tStart = time.ticks_ms()
    f1 = flex_1.read_u16()
    f2 = flex_2.read_u16()
    
    Gyro = mpu.read_gyro_data()
    xGyro = Gyro[0]
    yGyro = -Gyro[1]
    zGyro = Gyro[2]
    
    Accel = mpu.read_accel_data()
    xAccel = Accel[0]
    yAccel = Accel[1]
    zAccel = Accel[2]
    
    pGy += xGyro * tLoop
    rGy += yGyro * tLoop
    yaw += zGyro * tLoop
    pAc = math.atan(yAccel/zAccel)/(2*math.pi)*360
    rAc = math.atan(xAccel/zAccel)/(2*math.pi)*360
    
    pClr = 0.0025*pAc + 0.9975*(pClr + xGyro * tLoop) 
    rClr = 0.0025*rAc + 0.9975*(rClr + yGyro * tLoop) 
    
    errP += (pAc-pClr)*tLoop
    errR += (rAc-rClr)*tLoop
    
    print(yaw,pClr,rClr,f1,f2)
        
    tStop = time.ticks_ms()
    tLoop = (tStop - tStart) * 0.001
    
 
