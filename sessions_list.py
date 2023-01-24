import pandas as pd 
import matplotlib.pyplot as plt
import datetime
import numpy as np
from numpy.fft import fft, ifft





class Phase:
	def __init__(self, name):
		self.name = name
		self.CurrentList = df[name].tolist()




#-------------------------------OPENING THE INPUT FILE IN READ MODE----------------------------------------------
f = open('new.asc', 'r')

   #FILE LOCATION

df = pd.DataFrame()
data = []
for i in f:
	# REPLACING ASCII CHARS WITH SPACES
	tmp = i.split("\t")
	tmp[-1] = tmp[-1].replace("\n", "")
	data.append(tmp)


#CREATING DATAFRAME WITH NEW COLUMN NAMES
tmp_df = pd.DataFrame(data, columns = ["Date", "Time", "EM1_L1","EM1_L2", "EM1_L3", "EM3_L1","EM3_L2", "EM3_L3", "EM4_L1","EM4_L2", "EM4_L3"])
tmp_df = tmp_df.drop(index = 0)

#rEPLACING 0.1 VALUES WITH 0.0
df = tmp_df.replace("0,1", "0,0")


#------------------REMOVING THE ROWS WITH 0.0 IN ALL CURRENTS--------------------------------------------------


# indexcurrent = df[ (df['EM1_L1'] == '0,0') & (df['EM1_L2'] == '0,0') & (df['EM1_L3'] == '0,0') & (df['EM3_L1'] == '0,0') & (df['EM3_L2'] == '0,0') & (df['EM3_L3'] == '0,0') & (df['EM4_L1'] == '0,0') & (df['EM4_L2'] == '0,0') & (df['EM4_L3'] == '0,0') ].index
# df.drop(indexcurrent , inplace=True)

#GETTING UNIQUE DATES FROM THE DATAFRAME

print("Total number of days charging stations used : " ,len(df.Date.unique()))
Session_Date_List = df.Date.unique()

print(Session_Date_List)






fDate = []
for i in df["Date"]:
	dd = i[:2]
	mm = i[3:5]
	yy = i[6:10]

	fDate.append(yy +"-" + mm + "-" +  dd)

fDate = pd.to_datetime(fDate)
df["Date"] = fDate


df["dayofweek"] = df["Date"].dt.day_name()

#------------------REMOVING THE COMMA IN ALL CURRENT COLUMNS---------------------------------------------------


df['EM1_L1'] = df['EM1_L1'].replace(',', '', regex=True).astype(int).div(10)
df['EM1_L2'] = df['EM1_L2'].replace(',', '', regex=True).astype(int).div(10)
df['EM1_L3'] = df['EM1_L3'].replace(',', '', regex=True).astype(int).div(10)

df['EM3_L1'] = df['EM3_L1'].replace(',', '', regex=True).astype(int).div(10)
df['EM3_L2'] = df['EM3_L2'].replace(',', '', regex=True).astype(int).div(10)
df['EM3_L3'] = df['EM3_L3'].replace(',', '', regex=True).astype(int).div(10)

df['EM4_L1'] = df['EM4_L1'].replace(',', '', regex=True).astype(int).div(10)
df['EM4_L2'] = df['EM4_L2'].replace(',', '', regex=True).astype(int).div(10)
df['EM4_L3'] = df['EM4_L3'].replace(',', '', regex=True).astype(int).div(10)




#--------------------CALCULATION OF INSTANTANEOUS POWER------------------------------



VOLTAGE = 220
PF = 1.0

df['EM1_L1_Pwr'] = df['EM1_L1'] * VOLTAGE * PF * 1.732 
df['EM1_L2_Pwr'] = df['EM1_L2'] * VOLTAGE * PF * 1.732 
df['EM1_L3_Pwr'] = df['EM1_L3'] * VOLTAGE * PF * 1.732 

df['EM3_L1_Pwr'] = df['EM3_L1'] * VOLTAGE * PF * 1.732 
df['EM3_L2_Pwr'] = df['EM3_L2'] * VOLTAGE * PF * 1.732 
df['EM3_L3_Pwr'] = df['EM3_L3'] * VOLTAGE * PF * 1.732 

df['EM4_L1_Pwr'] = df['EM4_L1'] * VOLTAGE * PF * 1.732 
df['EM4_L2_Pwr'] = df['EM4_L2'] * VOLTAGE * PF * 1.732 
df['EM4_L3_Pwr'] = df['EM4_L3'] * VOLTAGE * PF * 1.732 




TDF = pd.DataFrame()
DF_list = []


flag =0


for index, row in df.iterrows():

	if row['EM1_L1'] > 0 or row['EM1_L2'] > 0 or row['EM1_L3'] > 0 or row['EM3_L1'] > 0  or row['EM3_L2'] > 0  or row['EM3_L3'] > 0  or row['EM4_L1'] > 0  or row['EM4_L2'] > 0  or row['EM4_L3'] > 0 :
		if flag == 0:
			start = index
			flag = 1
	else:
		if flag == 1:
			end = index
			TDF = df.iloc[start-2:end]
			DF_list.append(TDF)
			TDF = pd.DataFrame()
			flag = 0
		
		
#------------------ Plotting the data of ALL chargers per session --------------------------------------------

# fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
# ndf.plot("Time", ["EM1_L1","EM1_L2", "EM1_L3"], ax = ax1, ylabel = "Current", xlabel = "Time", title = "EM1")
# ndf.plot("Time", ["EM3_L1","EM3_L2", "EM3_L3"], ax = ax2, ylabel = "Current", xlabel = "Time", title = "EM3")
# ndf.plot("Time", ["EM4_L1","EM4_L2", "EM4_L3"], ax = ax3, ylabel = "Current", xlabel = "Time", title = "EM4")
# plt.show()






def Calc_FFT(A, B, C):

	EM1_FFT = [fft(A[0]), fft(A[1]), fft(A[2])]
	EM3_FFT = [fft(B[0]), fft(B[1]), fft(B[2])]
	EM4_FFT = [fft(C[0]), fft(C[1]), fft(C[2])]

	N = len(EM3_FFT[0])
	sr = 10             #SAMPLING RATE 
	n = np.arange(N)
	T_fft = N/sr


	freq = n/T_fft





	fig, axs = plt.subplots(3, 3)

	#	PLOTS FOR PHASE EM1
	axs[0, 0].stem(freq, np.abs(EM1_FFT[0]), 'b', markerfmt = " ", basefmt = "-b")
	axs[0, 0].set_title('EM1_L1')


	axs[0, 1].stem(freq, np.abs(EM1_FFT[1]), 'b', markerfmt = " ", basefmt = "-b")
	axs[0, 1].set_title('EM1_L2')

	axs[0, 2].stem(freq, np.abs(EM1_FFT[2]), 'b', markerfmt = " ", basefmt = "-b")
	axs[0, 2].set_title('EM1_L3')


	# #	PLOTS FOR PHASE EM3
	axs[1, 0].stem(freq, np.abs(EM3_FFT[0]), 'b', markerfmt = " ", basefmt = "-b")
	axs[1, 0].set_title('EM3_L1')


	axs[1, 1].stem(freq, np.abs(EM3_FFT[1]), 'b', markerfmt = " ", basefmt = "-b")
	axs[1, 1].set_title('EM3_L2')

	axs[1, 2].stem(freq, np.abs(EM3_FFT[2]), 'b', markerfmt = " ", basefmt = "-b")
	axs[1, 2].set_title('EM3_L3')

	# #  PLOTS FOR PHASE EM4

	axs[2, 0].stem(freq, np.abs(EM4_FFT[0]), 'b', markerfmt = " ", basefmt = "-b")
	axs[2, 0].set_title('EM4_L1')


	axs[2, 1].stem(freq, np.abs(EM4_FFT[1]), 'b', markerfmt = " ", basefmt = "-b")
	axs[2, 1].set_title('EM4_L2')

	axs[2, 2].stem(freq, np.abs(EM4_FFT[2]), 'b', markerfmt = " ", basefmt = "-b")
	axs[2, 2].set_title('EM4_L3')

	for ax in axs.flat:
   	 ax.set(xlabel=' Frequency in Hz', ylabel='Amplitude')

	# Hide x labels and tick labels for top plots and y ticks for right plots.
	for ax in axs.flat:
   	 ax.label_outer()
	plt.suptitle("Frequency characteristics using FFT")
	plt.show()







# -------------------------------FUNCTION FOR PLOTTING-----------------------------------------------------------

def Plot_Spectogram(EM1, EM3, EM4 ):
	
	fig, axs = plt.subplots(3, 3)

	#	PLOTS FOR PHASE EM1
	axs[0, 0].specgram(EM1[0])
	axs[0, 0].set_title('EM1_L1')

	axs[0, 1].specgram(EM1[1])
	axs[0, 1].set_title('EM1_L2')

	axs[0, 2].specgram(EM1[2])
	axs[0, 2].set_title('EM1_L3')


	#	PLOTS FOR PHASE EM3
	axs[1, 0].specgram(EM3[0])
	axs[1, 0].set_title('EM3_L1')

	axs[1, 1].specgram(EM3[1])
	axs[1, 1].set_title('EM3_L2')

	axs[1, 2].specgram(EM3[2])
	axs[1, 2].set_title('EM3_L3')

	#  PLOTS FOR PHASE EM4

	axs[2, 0].specgram(EM4[0])
	axs[2, 0].set_title('EM4_L1')

	axs[2, 1].specgram(EM4[1])
	axs[2, 1].set_title('EM4_L2')

	axs[2, 2].specgram(EM4[2])
	axs[2, 2].set_title('EM4_L3')

	for ax in axs.flat:
   	 ax.set(xlabel='', ylabel='')

	# Hide x labels and tick labels for top plots and y ticks for right plots.
	for ax in axs.flat:
   	 ax.label_outer()
	plt.suptitle("Spectogram ")
	plt.show()









#-----------------------------------------FFT AND SPECTOGRAM------------------------------------------------------------------



def FFT_Plots(charger, item, date, time):



	EM1 = [item["EM1_L1"].to_numpy(), item["EM1_L2"].to_numpy(), item["EM1_L3"].to_numpy()]
	EM3 = [item["EM3_L1"].to_numpy(), item["EM3_L2"].to_numpy(), item["EM3_L3"].to_numpy()]
	EM4 = [item["EM4_L1"].to_numpy(), item["EM4_L2"].to_numpy(), item["EM4_L3"].to_numpy()]


	T = item["Time"].to_numpy()


	T = np.arange(0,len(T)*5,5)







	# plt.specgram(EM3[0] )
	# plt.show()


	fig, axs = plt.subplots(3, 3)

	#	PLOTS FOR PHASE EM1
	axs[0, 0].plot(T, EM1[0], 'tab:red')
	axs[0, 0].set_title('EM1_L1')

	axs[0, 1].plot(T, EM1[1], 'tab:red')
	axs[0, 1].set_title('EM1_L2')

	axs[0, 2].plot(T, EM1[2], 'tab:red')
	axs[0, 2].set_title('EM1_L3')


	#	PLOTS FOR PHASE EM3
	axs[1, 0].plot(T, EM3[0], 'tab:olive')
	axs[1, 0].set_title('EM3_L1')

	axs[1, 1].plot(T, EM3[1], 'tab:olive')
	axs[1, 1].set_title('EM3_L2')

	axs[1, 2].plot(T, EM3[2], 'tab:olive')
	axs[1, 2].set_title('EM3_L3')

	#  PLOTS FOR PHASE EM4

	axs[2, 0].plot(T, EM4[0], 'tab:blue')
	axs[2, 0].set_title('EM4_L1')

	axs[2, 1].plot(T, EM4[1], 'tab:blue')
	axs[2, 1].set_title('EM4_L2')

	axs[2, 2].plot(T, EM4[2], 'tab:blue')
	axs[2, 2].set_title('EM4_L3')

	for ax in axs.flat:
   	 ax.set(xlabel='Time in Min', ylabel='Current in [A]')

	# Hide x labels and tick labels for top plots and y ticks for right plots.
	for ax in axs.flat:
   	 ax.label_outer()
	plt.suptitle("Date : " + date + "  |  Time : "+ time)
	# plt.show()


	Calc_FFT(EM1, EM3, EM4)
	Plot_Spectogram(EM1, EM3, EM4)









#----------------------------PLOTTING INDIVIDUAL POWER LINES IN 3X3 GRAPHS-----------------------------------

	# fig, axs = plt.subplots(3, 3)
	# axs[0, 0].plot(T, EM1[0], 'tab:red')
	# axs[0, 0].set_title('EM1_L1')

	# axs[0, 1].plot(T, EM1[1], 'tab:red')
	# axs[0, 1].set_title('EM1_L2')

	# axs[0, 2].plot(T, EM1[2], 'tab:red')
	# axs[0, 2].set_title('EM1_L3')

	# axs[1, 0].plot(T, EM3[0])
	# axs[1, 0].set_title('EM3_L1')

	# axs[1, 1].plot(T, EM3[1])
	# axs[1, 1].set_title('EM3_L2')

	# axs[1, 2].plot(T, EM3[2])
	# axs[1, 2].set_title('EM3_L3')

	# axs[2, 0].plot(T, EM4[0])
	# axs[2, 0].set_title('EM4_L1')

	# axs[2, 1].plot(T, EM4[1])
	# axs[2, 1].set_title('EM4_L2')

	# axs[2, 2].plot(T, EM4[2])
	# axs[2, 2].set_title('EM4_L3')

	# for ax in axs.flat:
   # 	 ax.set(xlabel='Time in Min', ylabel='Current in [A]')

	# # Hide x labels and tick labels for top plots and y ticks for right plots.
	# for ax in axs.flat:
   # 	 ax.label_outer()
	# plt.suptitle("Date : " + date + "  |  Time : "+ time)
	# plt.show()



#------------------ Plotting the data of ONE charger per session with power and FFT--------------------------------------------

#GET USER INPUT INSTEAD---------------------------------
#																		 -
#
User_Charger = "EM4"
User_Date = "2022-04-25"

#---------------------------------------------------------


for item in DF_list:
	Session_Date = item["Date"].iloc[0]
	Session_Date = (str(Session_Date)[:10])
	start_time = item["Time"].iloc[0]

	
	if Session_Date == User_Date:
		FFT_Plots(User_Charger, item, Session_Date, start_time)
		#PLOTS


# fig, (ax1, ax2) = plt.subplots(2, 1)
# ndf.plot("Time", [Charger+"_L1", Charger+"_L2", Charger+"_L3"], ax = ax1, ylabel = "Current", xlabel = "Time", title = "EM1")
# ndf.plot("Time", [Charger+"_L1_Pwr",Charger+"_L2_Pwr", Charger+"_L3_Pwr"], ax = ax2, ylabel = "Power", xlabel = "Time", title = "Watts")
# plt.show()





	


