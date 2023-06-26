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
duration = 50
#-----------------------------------------------------------------------------------#
def main():
    user_config_filename = "I2C_Config_pixel_Configuration_Broadcast_RW_FFpixel.txt"    # need to change by users
    #register_filename = "QTIA_register_config.txt"   # need to change by users

    COM_Port = "COM5"

    I2C_Addr = 0x05

    Reg_Addr = []
    Reg_Val = []  
    with open(user_config_filename, 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            if len(line.split()) == 1:
                #print(len(line.split()))                          # read I2C address
                I2C_Addr = int(line.split()[0], 16)
            else:                                               # read register address and value
                Reg_Addr += [int(line.split()[0], 16)]
                Reg_Val += [int(line.split()[1], 16)]


    # set usb-iss iic master device
    iss = UsbIss()
    iss.open(COM_Port)
    iss.setup_i2c(clock_khz=100)

    print(iss.i2c.test(I2C_Addr))

    if(iss.i2c.test(I2C_Addr)):    #Check whether a device responds at the specified I2C addresss.
        print("Successful communication with the target via I2C!")

        # Swap high 8-bit register address with low 8-bit (2 bytes) register address
        # Since the ET2_test I2C module write the low 8-bit register address first
        Reg_Addr_new = []
        for i in range(len(Reg_Addr)):
            # Reg_Addr_low += [Reg_Addr[i] & 0xFF]
            # Reg_Addr_high += [(Reg_Addr[i] >> 8) & 0xFF]
            Reg_Addr_new += [((Reg_Addr[i] & 0xFF) << 8) | ((Reg_Addr[i] >> 8) & 0xFF)]

        # iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new[0], Reg_Val)

        for i in range(len(Reg_Addr)):
            iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new[i], [Reg_Val[i]])

        read_data = []
        for i in range(len(Reg_Addr)):                              # read data from i2c slave
            read_data += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1)
        print("Read back data：")        #print reg_add, write data, read back data

        Reg_Val_Read_hex =[]
        for i in range(len(Reg_Addr)):
            Reg_Val_Read_hex += [hex(read_data[i])]
        print(Reg_Val_Read_hex)

        if read_data == Reg_Val:
            print("Read back data matched with write in data")
            for i in range(2):                                      # if read back data matched with write in data, speaker will make a sound three times
                winsound.Beep(freqency, duration)
                time.sleep(0.01)
        else:
            print("Read back data didn't match with write in data")
            print("No. Reg_Addr Reg_Write_Val Reg_Read_Val")
            for i in range(len(Reg_Addr)):
                if read_data[i] != Reg_Val[i]:
                    print(i, hex(Reg_Addr[i]), hex(Reg_Val[i]), hex(read_data[i])) 
        

        print("--------------------------This is the END!----------------------------")


    else:
        print("Unsuccessful communication with the target via I2C!")
        for i in range(4):                                      # if read back data matched with write in data, speaker will make a sound three times
            winsound.Beep(freqency, duration)
            time.sleep(0.01)

#-----------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()