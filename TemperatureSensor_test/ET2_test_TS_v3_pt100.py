import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyparsing import line
import pt100_Resist_to_Temp as pt100

'''
https://pythonbasics.org/read-excel/
Read Excel files (extensions:.xlsx, .xls) with Python Pandas. To read an excel file as a DataFrame, use the pandas read_excel() method.
You can specify the sheet to read with the argument sheet_name. Specify by number (starting at 0). Or Specify by sheet name.
It is also possible to specify a list in the argumentsheet_name. It is OK even if it is a number of 0 starting or the sheet name.
'''

excel_data = pd.read_excel('ET2_test_TemperatureSensor_test2.xlsx', sheet_name='Sheet2')
# print(excel_data)

TempSetting = excel_data['TempSetting']
Res_pt100_1 = excel_data['PT100_1']
Res_pt100_2 = excel_data['PT100_2']
Res_pt100_3 = excel_data['PT100_3']

tempReal_1 = []
for i in range(len(TempSetting)):
    tempReal_1 += [pt100.interp_resist_to_temp_naive(Res_pt100_1[i])]

tempReal_2 = []
for i in range(len(TempSetting)):
    tempReal_2 += [pt100.interp_resist_to_temp_naive(Res_pt100_2[i])]

tempReal_3 = []
for i in range(len(TempSetting)):
    tempReal_3 += [pt100.interp_resist_to_temp_naive(Res_pt100_3[i])]

# Create figure
fig = plt.figure()
# Add subplot to figure
ax = fig.add_subplot(111)

# Plot data
ax.plot(TempSetting, tempReal_1, linestyle = '--', marker='1', c='orange', label = 'Temp measured by pt100')
ax.plot(TempSetting, tempReal_2, linestyle = '-.', marker='1', c='blue', label = 'Temp measured by pt100')
ax.plot(TempSetting, tempReal_3, linestyle = ':', marker='1', c='red', label = 'Temp measured by pt100')

ax.yaxis.get_ticklocs(minor=True)
ax.minorticks_on()

# Set axises
# ax.set_xlim(-45, 55)
# ax.set_ylim(0.475, 0.775)

# Set axis labels
ax.set_xlabel('Temp setting [$^o$C]')
ax.set_ylabel('Temp measured by pt100 [$^o$C]')

# Add legend
ax.legend()
# Add legend - loc is a tuple specifying the bottom left corner
# ax.legend(loc=(1.02, 0.65))

ax.grid(True)

fig.savefig('ET2_test_Temp_pt100_v3.png', transparent = True)

# Show plot
plt.show()




