import pandas as pd
import os
import sys
import time
import winsound
from usb_iss import UsbIss, defs

'''
@author: Xing Huang
@date: JanJan. 7, 2021
This script as a generic I2C cofniguration software to configure I2C slave. The I2C reg configuration data is read into a xxx.dat file.
The UsbIss as I2C master deivce is used to write and read I2C slave register.
'''


#-----------------------------------------------------------------------------------#
freqency = 1000
duration = 200
#-----------------------------------------------------------------------------------#
def main():
    # user_config_filename = "ET2_test_user_config.txt"    # need to change by users
    #register_filename = "QTIA_register_config.txt"   # need to change by users

    COM_Port = "COM5"

    I2C_Addr = 0x05

    # Reg_Addr = []


    efMode = 0b01                   # 0b10 read mode, 0b01 write mode
    tsPD = 0b0
    dataOut_disBias = 0b0
    dataOut_AmpSel = 0b111
    dataOut_Sel = 0b1

    efTckhp = 0b0100                # 4'b0100 ~ 5 us
    efStart = 0b0                   # start = 1
    efClkSel = 0b0
    efClkEn = 0b1
    efRstN = 0b1

    efProg_preDef = 0x0000_0002     #32'h0001

    Reg6 = (efMode << 6) + (tsPD << 5) +(dataOut_disBias << 4) +(dataOut_AmpSel <<1) + (dataOut_Sel)
    Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
    Reg8 = efProg_preDef & 0xff
    Reg9 = (efProg_preDef >> 8) & 0xff
    RegA = (efProg_preDef >> 16) & 0xff
    RegB = (efProg_preDef >> 24) & 0xff


    # Registers' addresses, values of eFuse configuration
    Reg_Val = [Reg6, Reg7, Reg8, Reg9, RegA, RegB]
    Reg_Addr = [0x0006, 0x0007, 0x0008, 0x0009, 0x000A, 0x000B]

    Reg_Addr_efuse = [0x0100, 0x0101, 0x0102, 0x0103]

    # set usb-iss iic master device
    iss = UsbIss()
    iss.open(COM_Port)
    iss.setup_i2c(clock_khz=400)

    print(iss.i2c.test(I2C_Addr))

    if(iss.i2c.test(I2C_Addr)):
        print("Successful communication with the target via I2C!")
        winsound.PlaySound("SystemExit", winsound.MB_OK)

        Reg_Addr_new = []
        for i in range(len(Reg_Addr)):
            Reg_Addr_new += [((Reg_Addr[i] & 0xFF) << 8) | ((Reg_Addr[i] >> 8) & 0xFF)]

        Reg_Addr_efuse_new = []
        for i in range(len(Reg_Addr_efuse)):
            Reg_Addr_efuse_new += [((Reg_Addr_efuse[i] & 0xFF) << 8) | ((Reg_Addr_efuse[i] >> 8) & 0xFF)]

    #0. Write the initialization of eFuse configuration registers
        iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new[0], Reg_Val)
        read_data = iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[0], 6)
        # print("Read back efuse configurations：")        #print reg_add, write data, read back data
        # for i in range(len(Reg_Addr)):
            # print(hex(Reg_Addr[i]), hex(Reg_Val[i]), hex(read_data[i]))


    #1. Reset the eFuse after the power up.
        efRstN = 0b1
        Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
        iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new[1], [Reg7]) # reset = 1
        # read_data_reg7 = iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[1], 1)
        # print(hex(Reg_Addr[1]), hex(int(read_data_reg7[0])))
        time.sleep(0.1)

        efRstN = 0b0
        Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
        iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new[1], [Reg7]) # reset = 0
        # read_data_reg7 = iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[1], 1)
        # print(hex(Reg_Addr[1]), hex(int(read_data_reg7[0])))
        time.sleep(0.1)

        efRstN = 0b1
        Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
        iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new[1], [Reg7]) # reset = 1
        # read_data_reg7 = iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[1], 1)
        # print(hex(Reg_Addr[1]), hex(int(read_data_reg7[0])))
        time.sleep(0.1)


    #2. Write start a pulse to generate the falling edge.
        efStart = 0b0
        Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
        iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new[1], [Reg7]) # start = 0
        # read_data_reg7 = iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[1], 1)
        # print(hex(Reg_Addr[1]), hex(int(read_data_reg7[0])))
        time.sleep(0.1)

        efStart = 0b1
        Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
        iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new[1], [Reg7]) # start = 1
        # read_data_reg7 = iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[1], 1)
        # print(hex(Reg_Addr[1]), hex(int(read_data_reg7[0])))
        time.sleep(0.1)

        efStart = 0b0
        Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
        iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new[1], [Reg7]) # start = 0
        # read_data_reg7 = iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[1], 1)
        # print(hex(Reg_Addr[1]), hex(int(read_data_reg7[0])))
        time.sleep(0.1)


    #3. After writing the eFuse, read back the values of eFuse.
    # Registers' address if 0x0100, 0x0101, 0x0102, 0x0103.
        # read_data_efuse_afterWrite = iss.i2c.read_ad2(I2C_Addr, Reg_Addr_efuse_new[0], 4)
        # print("Read back efuse values：")        #print reg_add, write data, read back data
        # for i in range(len(Reg_Addr_efuse)):
            # print(hex(Reg_Addr_efuse[i]), hex(read_data_efuse_afterWrite[i]))      


    else:
         for i in range(4):                                      # if read back data matched with write in data, speaker will make a sound three times
            winsound.Beep(freqency, duration)
            time.sleep(0.01)

#-----------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()