import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyparsing import line
import pt100_lookuptable as pt100

'''
https://pythonbasics.org/read-excel/
Read Excel files (extensions:.xlsx, .xls) with Python Pandas. To read an excel file as a DataFrame, use the pandas read_excel() method.
You can specify the sheet to read with the argument sheet_name. Specify by number (starting at 0). Or Specify by sheet name.
It is also possible to specify a list in the argumentsheet_name. It is OK even if it is a number of 0 starting or the sheet name.
'''

excel_data = pd.read_excel('ET2_test_TemperatureSensor_test2.xlsx', sheet_name='Sheet2')
# print(excel_data)

TempSetting = excel_data['TempSetting']

TS_testOut4_1 = excel_data['TS_testOUT4_1']
TS_Out4_1 = excel_data['TS_OUT4_1']
TS_testOut4_2 = excel_data['TS_testOUT4_2']
TS_Out4_2 = excel_data['TS_OUT4_2']
TS_testOut4_3 = excel_data['TS_testOUT4_3']
TS_Out4_3 = excel_data['TS_OUT4_3']

TS_testOut5_1 = excel_data['TS_testOUT5_1']
TS_Out5_1 = excel_data['TS_OUT5_1']
TS_testOut5_2 = excel_data['TS_testOUT5_2']
TS_Out5_2 = excel_data['TS_OUT5_2']
TS_testOut5_3 = excel_data['TS_testOUT5_3']
TS_Out5_3 = excel_data['TS_OUT5_3']

TS_testOut6_1 = excel_data['TS_testOUT6_1']
TS_Out6_1 = excel_data['TS_OUT6_1']
TS_testOut6_2 = excel_data['TS_testOUT6_2']
TS_Out6_2 = excel_data['TS_OUT6_2']
TS_testOut6_3 = excel_data['TS_testOUT6_3']
TS_Out6_3 = excel_data['TS_OUT6_3']

TS_testOut7_1 = excel_data['TS_testOUT7_1']
TS_Out7_1 = excel_data['TS_OUT7_1']
TS_testOut7_2 = excel_data['TS_testOUT7_2']
TS_Out7_2 = excel_data['TS_OUT7_2']
TS_testOut7_3 = excel_data['TS_testOUT7_3']
TS_Out7_3 = excel_data['TS_OUT7_3']

TS_testOut8_1 = excel_data['TS_testOUT8_1']
TS_Out8_1 = excel_data['TS_OUT8_1']
TS_testOut8_2 = excel_data['TS_testOUT8_2']
TS_Out8_2 = excel_data['TS_OUT8_2']
TS_testOut8_3 = excel_data['TS_testOUT8_3']
TS_Out8_3 = excel_data['TS_OUT8_3']

# Data processing
# tempReal = []
# for i in range(len(Res_pt100)):
#     tempReal += [pt100.interp_resist_to_temp_naive(Res_pt100[i])]

# Create figure
fig = plt.figure()
# Add subplot to figure
ax = fig.add_subplot(111)

TS_Measure = 1
if (TS_Measure == 1):
    # Plot data
    ax.plot(TempSetting, TS_testOut4_1, linestyle = '--', marker='1', c='blue', label = 'B4 ET2_test TS_testOUT')
    ax.plot(TempSetting, TS_Out4_1, linestyle = '-', marker='1', c='blue', label = 'B4 ET2_test TS_OUT')

    ax.plot(TempSetting, TS_testOut5_1, linestyle = '--', marker='*', c='green', label = 'B5 ET2_test TS_testOUT')
    ax.plot(TempSetting, TS_Out5_1, linestyle = '-', marker='*', c='green', label = 'B5 ET2_test TS_OUT')

    ax.plot(TempSetting, TS_testOut6_1, linestyle = '--', marker='o', c='cyan', label = 'B6 ET2_test TS_testOUT')
    ax.plot(TempSetting, TS_Out6_1, linestyle = '-', marker='o', c='cyan', label = 'B6 ET2_test TS_OUT')

    ax.plot(TempSetting, TS_testOut7_1, linestyle = '--', marker='>', c='magenta', label = 'B7 ET2_test TS_testOUT')
    ax.plot(TempSetting, TS_Out7_1, linestyle = '-', marker='>', c='magenta', label = 'B7 ET2_test TS_OUT')

    ax.plot(TempSetting, TS_testOut8_1, linestyle = '--', marker='s', c='brown', label = 'B8 ET2_test TS_testOUT')
    ax.plot(TempSetting, TS_Out8_1, linestyle = '-', marker='s', c='brown', label = 'B8 ET2_test TS_OUT')
else:
    if (TS_Measure == 2):
        ax.plot(TempSetting, TS_testOut4_2, linestyle = '--', marker='1', c='blue', label = 'B4 ET2_test TS_testOUT')
        ax.plot(TempSetting, TS_Out4_2, linestyle = '-', marker='1', c='blue', label = 'B4 ET2_test TS_OUT')

        ax.plot(TempSetting, TS_testOut5_2, linestyle = '--', marker='*', c='green', label = 'B5 ET2_test TS_testOUT')
        ax.plot(TempSetting, TS_Out5_2, linestyle = '-', marker='*', c='green', label = 'B5 ET2_test TS_OUT')

        ax.plot(TempSetting, TS_testOut6_2, linestyle = '--', marker='o', c='cyan', label = 'B6 ET2_test TS_testOUT')
        ax.plot(TempSetting, TS_Out6_2, linestyle = '-', marker='o', c='cyan', label = 'B6 ET2_test TS_OUT')

        ax.plot(TempSetting, TS_testOut7_2, linestyle = '--', marker='>', c='magenta', label = 'B7 ET2_test TS_testOUT')
        ax.plot(TempSetting, TS_Out7_2, linestyle = '-', marker='>', c='magenta', label = 'B7 ET2_test TS_OUT')

        ax.plot(TempSetting, TS_testOut8_2, linestyle = '--', marker='s', c='brown', label = 'B8 ET2_test TS_testOUT')
        ax.plot(TempSetting, TS_Out8_2, linestyle = '-', marker='s', c='brown', label = 'B8 ET2_test TS_OUT_2')
    else:
        if (TS_Measure == 3):
            ax.plot(TempSetting, TS_testOut4_3, linestyle = '--', marker='1', c='blue', label = 'B4 ET2_test TS_testOUT')
            ax.plot(TempSetting, TS_Out4_3, linestyle = '-', marker='1', c='blue', label = 'B4 ET2_test TS_OUT')

            ax.plot(TempSetting, TS_testOut5_3, linestyle = '--', marker='*', c='green', label = 'B5 ET2_test TS_testOUT')
            ax.plot(TempSetting, TS_Out5_3, linestyle = '-', marker='*', c='green', label = 'B5 ET2_test TS_OUT')

            ax.plot(TempSetting, TS_testOut6_3, linestyle = '--', marker='o', c='cyan', label = 'B6 ET2_test TS_testOUT')
            ax.plot(TempSetting, TS_Out6_3, linestyle = '-', marker='o', c='cyan', label = 'B6 ET2_test TS_OUT')

            ax.plot(TempSetting, TS_testOut7_3, linestyle = '--', marker='>', c='magenta', label = 'B7 ET2_test TS_testOUT')
            ax.plot(TempSetting, TS_Out7_3, linestyle = '-', marker='>', c='magenta', label = 'B7 ET2_test TS_OUT')

            ax.plot(TempSetting, TS_testOut8_3, linestyle = '--', marker='s', c='brown', label = 'B8 ET2_test TS_testOUT')
            ax.plot(TempSetting, TS_Out8_3, linestyle = '-', marker='s', c='brown', label = 'B8 ET2_test TS_OUT_3')        


ax.yaxis.get_ticklocs(minor=True)
ax.minorticks_on()

# Set axises
ax.set_xlim(-45, 55)
ax.set_ylim(0.475, 0.775)

# Set axis labels
ax.set_xlabel('Temp setting [$^o$C]')
ax.set_ylabel('Voltage [V]')

# Add legend
ax.legend()
# Add legend - loc is a tuple specifying the bottom left corner
# ax.legend(loc=(1.02, 0.65))

# Grid on setting
ax.grid(True)

# Save as fig
fig.savefig('ET2_test_Temp_v3.png', transparent = True)

# Show plot
plt.show()




