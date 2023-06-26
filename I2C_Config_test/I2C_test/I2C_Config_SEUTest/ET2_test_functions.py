import os
import sys
import time
import winsound


def regAddrSwap(RegAddr):
    ''' 
    Swap high 8-bit register address with low 8-bit (2 bytes in total) register address, since the ET2_test I2C module write the low 8-bit register address first.
    If not this case, just ignore this functiono.

    Arguments:
        RegAddr: a list of the 16-bit register addresses

    Example:
        ::

            import ET2_test_functions

            RegAddr = [0x8000, 0x8001, 0x8002]

            RegAddr_new = ET2_test_functions.regAddrSwap(RegAddr)

            print(RegAddr_new)
            
            > [0x0080, 0x0180, 0x0280]
    '''
    # Reg_Addr_high = []
    # Reg_Addr_low = []
    RegAddr_new = []
    if(len(RegAddr) > 0):
        for i in range(len(RegAddr)):
            # Reg_Addr_low += [Reg_Addr[i] & 0xFF]
            # Reg_Addr_high += [(Reg_Addr[i] >> 8) & 0xFF]
            RegAddr_new += [((RegAddr[i] & 0xFF) << 8) | ((RegAddr[i] >> 8) & 0xFF)]
    else:
        print('The input arg is empty.')

    return RegAddr_new




def valueCompare(RegAddr, RegVal, readBackValue):
    '''
    Compare the read-back data with the desired (default/write-in) data.

    Arguments:
        RegAddr: A list of the addresses corresponding to the compared data.

        RegVal: A list of the desired data as the compared reference.

        readBackValue: A list of the read-back from the addresss list of RegAddr.

    Example:
         ::

            import ET2_test_functions

            RegAddr = [0x8000, 0x8001, 0x8002]

            RegVal = [0x00, 0x01, 0x02]

            readBackValue = [0x00, 0x01, 0x02]

            print(ET2_test_functions.valueCompare(RegAddr, RegVal, readBackValue))

            > 1
    '''
    # print('------------------------Comparison Action------------------------')
    MatchOrNot = 11001100       # Comparison flag, if equal, 1; else 0.
    if RegVal == readBackValue:
        # print("Read back data matched with the desired (default/write-in) data!")
        MatchOrNot = 1                                     # if read back data matched with write in data, speaker will make a sound three times
        winsound.Beep(1000, 1000)
    else:
        MatchOrNot = 0
        print("!!!Read back data didn't match with the desired (default/write-in) data!!!")        #print reg_add, write data, read back data
        print("Reg_Addr Reg_Val Reg_Read_Val")
        for i in range(5):                                      # if read back data matched with write in data, speaker will make a sound three times
            winsound.Beep(1000, 50)
            # time.sleep(0.01)

        for i in range(len(RegAddr)):
            if RegVal[i] != readBackValue[i]:
                print(hex(RegAddr[i]), hex(RegVal[i]), hex(readBackValue[i]))

    return MatchOrNot