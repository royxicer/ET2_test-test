# import pandas as pdc
import os
import sys
import time
import winsound
from usb_iss import UsbIss, defs
import ET2_test_functions

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
    ''' I2C test ''' 

    user_config_filename = "ET2_test_I2C_Config_Configuration_FullRW_V3.txt" 

    COM_Port = "COM5"

    # All of the register addresses, and default values 
    Reg_Addr = []
    Reg_Val_Default = []
    Reg_Val_Write = []
    Reg_Val_Broadcast = []      

    # Read configuraton file, I2C address, 16-bit register addresses, 8-bit register values
    with open(user_config_filename, 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            if len(line.split()) == 1:
                #print(len(line.split()))                          # read I2C address
                I2C_Addr = int(line.split()[0], 16)
            else:                                               # read register address and value
                Reg_Addr += [int(line.split()[0], 16)]
                Reg_Val_Default += [int(line.split()[1], 16)]
                Reg_Val_Write += [int(line.split()[2], 16)]
                Reg_Val_Broadcast += [int(line.split()[3], 16)]

    print('There are', len(Reg_Addr), 'registers in ET2_test chip.')

    # set usb-iss iic master device
    iss = UsbIss()
    iss.open(COM_Port)
    iss.setup_i2c(clock_khz=100)

    # Check whether a device responds at the specified I2C address.
    if(iss.i2c.test(I2C_Addr)):
        # print("Successful communication with the target via I2C!")
        winsound.PlaySound("SystemExit", winsound.MB_OK)
        print('-------------------------I2C Successful Communication---------------------------')


        #Swap all register addresses in ET2_test chip.
        Reg_Addr_new = ET2_test_functions.regAddrSwap(Reg_Addr)

        # All of the pixel and common-circuit configuration and status registers, read back the default values
        Reg_Addr_Read = []
        Reg_Val_Read_Default = []
        read_data = []
        for i in range(len(Reg_Addr)):              # read data from i2c slave
            if ((i < 564) & (i != 544) & (i != 545) & (i != 546)  & (i != 547) & (i != 559)):
                Reg_Addr_Read += [Reg_Addr[i]]
                Reg_Val_Read_Default += [Reg_Val_Default[i]]
                read_data += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1)
        print("STEP 1: Read back all the registers' default values, and compare:")
        defaultMatch = ET2_test_functions.valueCompare(Reg_Addr, Reg_Val_Read_Default, read_data) == 1
        if(defaultMatch == 1):
            print('ET2_test I2C Registers Default Values Read Test Passed!')
        else:
            print('ET2_test I2C Registers Default Values Read Test Failed!')
        print('----------------------------------STEP1 END-------------------------------------')


        # defaultMatch = 0
        # if(defaultMatch == 1):
        if(defaultMatch == 1):
            for i in range(len(Reg_Addr)):
                if((0 <= i <=255) | (512 <= i <= 563)):
                    iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new[i], [Reg_Val_Write[i]])


            # Pixel configuration registers write and read back to compare the write-in and read-back values
            Reg_Addr_pixConfigurable = []
            Reg_Val_Write_pixConfigurable = []              
            read_data_writeTest_pixConfigurable = []
            for i in range(len(Reg_Addr)):
                if ((0 <= i <= 7) | (120 <= i <= 135) | (248 <= i <= 255)):
                    Reg_Addr_pixConfigurable += [Reg_Addr[i]]
                    Reg_Val_Write_pixConfigurable += [Reg_Val_Write[i]]
                    read_data_writeTest_pixConfigurable += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1)
            print("STEP2: Write and Read back the pixel configuration registers' default values, and compare:")
            if (ET2_test_functions.valueCompare(Reg_Addr_pixConfigurable, Reg_Val_Write_pixConfigurable, read_data_writeTest_pixConfigurable) == 1):
                print('Pixel Configurable Registers Write and Read Test Passed!')
            else:
                print('Pixel Configurable Registers Write and Read Test Failed!')
            print('----------------------------------STEP2 END-------------------------------------')


            # Common-circuit configuration registers write and read back to compare the write-in and read-back values
            Reg_Addr_comConfig = []
            Reg_Val_Write_comConfig = []              
            read_data_writeTest_comConfig = []
            for i in range(len(Reg_Addr)):
                if (512 <= i <= 543):
                    Reg_Addr_comConfig += [Reg_Addr[i]]
                    Reg_Val_Write_comConfig += [Reg_Val_Write[i]]
                    read_data_writeTest_comConfig += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1)
                    # print(i, hex(Reg_Addr[i]))
            print("STEP3: Write and Read back the Common-circuit configuration registers' default values, and compare:")
            if (ET2_test_functions.valueCompare(Reg_Addr_comConfig, Reg_Val_Write_comConfig, read_data_writeTest_comConfig) == 1):
                print('Common-circuit Configuration Registers Write and Read Test Passed!')
            else:
                print('Common-circuit Configuration Registers Write and Read Test Failed!')
            print('----------------------------------STEP3 END-------------------------------------')


            # Read back the values common-circuit status registers, compare the read-back values with the default values to confirm they are read-only registers
            Reg_Addr_comSatus = []
            Reg_Val_comStatus_Default = []
            read_data_readOnlyTest_comStatus = []
            for i in range(len(Reg_Addr)):
                if ((544 <= i <= 563) & (i != 544) & (i != 545) & (i != 546)  & (i != 547) & (i != 559)):
                    Reg_Addr_comSatus += [Reg_Addr[i]]
                    Reg_Val_comStatus_Default += [Reg_Val_Default[i]]
                    read_data_readOnlyTest_comStatus += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1)
            print("STEP4: Write the com Status registers, Read back to compare with the default values:")
            if (ET2_test_functions.valueCompare(Reg_Addr_comSatus, Reg_Val_comStatus_Default, read_data_readOnlyTest_comStatus) == 1):
                print('Common-circuit Status Registers Read Only Test Passed!')
            else:
                print('Common-circuit Status Registers Read Only Test Failed!')
            print('----------------------------------STEP4 END-------------------------------------')


            # Write the specified register addresses to broadcast to all the configurable pixel registers
            Reg_Addr_Broadcast = []
            Reg_Val_Broadcast_Write = []
            read_data_BroadcastAddr = []
            Reg_Addr_Broadcast_new = []
            for i in range(len(Reg_Addr)):
                if (564 <= i <= 571):
                    Reg_Addr_Broadcast += [Reg_Addr[i]]
                    Reg_Addr_Broadcast_new += [Reg_Addr_new[i]]
                    Reg_Val_Broadcast_Write += [Reg_Val_Broadcast[i]]

            iss.i2c.write_ad2(I2C_Addr, Reg_Addr_Broadcast_new[0], Reg_Val_Broadcast_Write)
            read_data_BroadcastAddr = iss.i2c.read_ad2(I2C_Addr, Reg_Addr_Broadcast_new[0], len(Reg_Addr_Broadcast))
            print("STEP5.0: Write the specified registers (and Read back) to broadcast:")
            if (ET2_test_functions.valueCompare(Reg_Addr_Broadcast, Reg_Val_Broadcast_Write, read_data_BroadcastAddr) == 1):
                print('Pixel Broadcast Setting Passed!')
            else:
                print('Pixel Broadcast Setting Not Passed!')
            print('---------------------------------STEP5.1 END------------------------------------')


            # Read back the values of all the configurable pixel registers to compare the expected broadcast values
            Reg_Addr_pixBroadcast = []
            Reg_Val_pixBroadcast = []              
            read_data_pixBroadcast = []
            for i in range(len(Reg_Addr)):
                if ((0 <= i <= 7) | (120 <= i <= 135) | (248 <= i <= 255)):
                    Reg_Addr_pixBroadcast += [Reg_Addr[i]]
                    Reg_Val_pixBroadcast += [Reg_Val_Broadcast[i]]
                    read_data_pixBroadcast += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1)
            print("STEP5.1: Read back the pixel configurable registers to compare, verify the broadcast:")
            if (ET2_test_functions.valueCompare(Reg_Addr_pixBroadcast, Reg_Val_pixBroadcast, read_data_pixBroadcast) == 1):
                print('Pixel Configurable Registers Broadcast Test Passed!')
            else:
                print('Pixel Configurable Registers Broadcast Test Failed!')
            print('---------------------------------STEP5.2 END------------------------------------')
        else:
            print('Not Test the Write and Read!')

    else:
        print("Unsuccessful communication with the target via I2C!")
        for i in range(4):                                 
            winsound.Beep(freqency, duration)
            time.sleep(0.01)

#-----------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()