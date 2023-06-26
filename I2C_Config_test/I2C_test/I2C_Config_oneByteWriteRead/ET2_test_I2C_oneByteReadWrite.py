import pandas as pd
import os
import sys
import time
import winsound
from usb_iss import UsbIss, defs

'''
@author: Xing Huang
@date: Jan. 7, 2021
This script as a generic I2C cofniguration software to configure I2C slave. The I2C reg configuration data is read into a xxx.dat file.
The UsbIss as I2C master deivce is used to write and read I2C slave register.
'''


#-----------------------------------------------------------------------------------#
freqency = 1000
duration = 200
#-----------------------------------------------------------------------------------#
def main():
    user_config_filename = "ET2_test_user_config.txt"    # need to change by users
    #register_filename = "QTIA_register_config.txt"   # need to change by users

    COM_Port = "COM5"

    I2C_Addr = 0x05

    Reg_Addr = 0x8FFf

    Reg_Val = 0xf0 


    # set usb-iss iic master device
    iss = UsbIss()
    iss.open(COM_Port)
    iss.setup_i2c(clock_khz=100)

    print(iss.i2c.test(I2C_Addr))

    if(iss.i2c.test(I2C_Addr)):
        print("Successful communication with the target via I2C!")

        # Swap high 8-bit register address with low 8-bit (2 bytes) register address
        # Since the ET2_test I2C module write the low 8-bit register address first
        Reg_Addr_new = ((Reg_Addr & 0xFF) << 8) | ((Reg_Addr >> 8) & 0xFF)
        # print(hex(Reg_Addr_new[i]))

        iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new, [Reg_Val])

        read_data = iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new, 1)
        print("Read back data：")        #print reg_add, write data, read back data
        print(hex(Reg_Addr), hex(read_data[0]))

        
        if read_data == [Reg_Val]:
            print("Read back data matched with write in data")
            for i in range(2):                                      # if read back data matched with write in data, speaker will make a sound three times
                winsound.Beep(freqency, duration)
                time.sleep(0.01)
        else:
            print("Read back data didn't match with write in data") 
        

        print("--------------------------This is the END!----------------------------")


    else:
        print("Unsuccessful communication with the target via I2C!")
        for i in range(4):                                      # if read back data matched with write in data, speaker will make a sound three times
            winsound.Beep(freqency, duration)
            time.sleep(0.01)

#-----------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()