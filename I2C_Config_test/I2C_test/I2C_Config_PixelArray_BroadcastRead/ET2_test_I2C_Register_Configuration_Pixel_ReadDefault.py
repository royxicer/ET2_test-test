# import pandas as pdc
import os
import sys
import time
import winsound
from usb_iss import UsbIss, defs

import numpy as np

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
    user_config_filename = "I2C_Config_pixel_Configuration_Default_RW_Broadcast.txt"    # need to change by users
    #register_filename = "QTIA_register_config.txt"   # need to change by users

    COM_Port = "COM5"

    Reg_Addr = []
    Reg_Val = [] 
    Reg_Val_Broadcast = [] 
    with open(user_config_filename, 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            if len(line.split()) == 1:
                #print(len(line.split()))                          # read I2C address
                I2C_Addr = int(line.split()[0], 16)
            else:                                               # read register address and value
                Reg_Addr += [int(line.split()[0], 16)]
                Reg_Val += [int(line.split()[1], 16)]
                Reg_Val_Broadcast += [int(line.split()[2], 16)]

    # Reg_Val_Default_hex =[]
    # for i in range(len(Reg_Addr)):
    #     Reg_Val_Default_hex += [hex(Reg_Val[i])]
    # # print(Reg_Val_Default_hex)


    Reg_Val_Broadcast_hex =[]
    for i in range(len(Reg_Addr)):
        Reg_Val_Broadcast_hex += [hex(Reg_Val_Broadcast[i])]
    print(Reg_Val_Broadcast_hex)

    # set usb-iss iic master device
    iss = UsbIss()
    iss.open(COM_Port)
    iss.setup_i2c(clock_khz=100)

    # Check whether a device responds at the specified I2C address.
    if(iss.i2c.test(I2C_Addr)):
        print("Successful communication with the target via I2C!")
        winsound.PlaySound("SystemExit", winsound.MB_OK)

        # Swap high 8-bit register address with low 8-bit (2 bytes) register address
        # Since the ET2_test I2C module write the low 8-bit register address first
        # Reg_Addr_high = []
        # Reg_Addr_low = []
        Reg_Addr_new = []
        for i in range(len(Reg_Addr)):
            # Reg_Addr_low += [Reg_Addr[i] & 0xFF]
            # Reg_Addr_high += [(Reg_Addr[i] >> 8) & 0xFF]
            Reg_Addr_new += [((Reg_Addr[i] & 0xFF) << 8) | ((Reg_Addr[i] >> 8) & 0xFF)]

        read_data = []
        for i in range(len(Reg_Addr)):                              # read data from i2c slave
            read_data += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1)

        # read_data = iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[0], len(Reg_Addr_new))

        Reg_Val_Read_hex =[]
        for i in range(len(Reg_Addr)):
            Reg_Val_Read_hex += [hex(read_data[i])]
        # print(Reg_Val_Read_hex)

        ## compare write in data with read back data
        if read_data == Reg_Val_Broadcast:
            print("Read back data matched with broadcast data, pixel array of ET2 test chip")
            for i in range(2):                                      # if read back data matched with write in data, speaker will make a sound three times
                winsound.Beep(freqency, duration)
                time.sleep(0.01)
        else:
            print("Read back data didn't match with broadcast data, pixel array of ET2 test chip")        #print reg_add, write data, read back data
            print("No. Reg_Addr Reg_Read_Val")
            for i in range(len(Reg_Addr)):
                if read_data[i] != Reg_Val_Broadcast[i]:
                    print(i, hex(Reg_Addr[i]), hex(read_data[i]))
        print("Ok!")

    else:
        print("Unsuccessful communication with the target via I2C!")
        for i in range(4):                                 
            winsound.Beep(freqency, duration)
            time.sleep(0.01)

#-----------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()