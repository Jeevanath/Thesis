import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import datetime





class Phase:
	def __init__(self, name):
		self.name = name
		self.CurrentList = df[name].tolist()








# def find_Energy(Dct):
	















#OPENING THE INPUT FILE IN READ MODE
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


#REMOVING THE ROWS WITH 0.0 IN ALL CURRENTS
# indexcurrent = df[ (df['EM1_L1'] == '0,0') & (df['EM1_L2'] == '0,0') & (df['EM1_L3'] == '0,0') & (df['EM3_L1'] == '0,0') & (df['EM3_L2'] == '0,0') & (df['EM3_L3'] == '0,0') & (df['EM4_L1'] == '0,0') & (df['EM4_L2'] == '0,0') & (df['EM4_L3'] == '0,0') ].index
# df.drop(indexcurrent , inplace=True)

#GETTING UNIQUE DATES FROM THE DATAFRAME

print("Total number of days charging station used : " ,len(df.Date.unique()))




fDate = []
for i in df["Date"]:
	dd = i[:2]
	mm = i[3:5]
	yy = i[6:10]

	fDate.append(yy +"-" + mm + "-" +  dd)

fDate = pd.to_datetime(fDate)
df["Date"] = fDate


df["dayofweek"] = df["Date"].dt.day_name()

phase_list = ["EM1_L1", "EM1_L2", "EM1_L3", "EM3_L1", "EM3_L2", "EM3_L3", "EM4_L1", "EM4_L2", "EM4_L3" ]


phase_objs = []

for i in phase_list:
	phase_objs.append(Phase(i))




tmp_df = []
Energy = 0
Imax = 0


def find_dur(StartTime, EndTime):
        H1 = int(StartTime[:2])
        M1 = int(StartTime[3:5])
        S1 = int(StartTime[6:8])

        T1 = (H1*60*60) + (M1 * 60) + S1

        H2 = int(EndTime[:2])
        M2 = int(EndTime[3:5])
        S2 = int(EndTime[6:8])

        T2 = (H2*60*60) + (M2 * 60) + S2

        Duration = str(datetime.timedelta(seconds=T2-T1))

        return Duration, (T2 - T1)
	



for n in phase_objs:

	Ts = 300
	Voltage = 230
	CurrentList = n.CurrentList



	for i in range(len(CurrentList)):


		current = CurrentList[i]
		current  = int(current.replace(',', ''))/10
		if current != 0:
			if Energy == 0:
				# print("Init ", CurrentList[i])
				start_time = df.at[i+1,"Time"]
				Date = df.at[i+1,"Date"]
				Day = df.at[i+1,"dayofweek"]
			Energy = Energy + (Ts * Voltage * current )
			if Imax < current:
				Imax = current
			# print("current", CurrentList[i])

		if i == (len(CurrentList)-1) and current != 0:
			# print("List end ", CurrentList[i])
			end_time = df.loc[i+1,"Time"]
			Duration_str,Duration_Sec  = find_dur(start_time, end_time)
			tmp_df.append([n.name, start_time, end_time ,Date, Energy, Imax, Duration_str, Duration_Sec])
			Energy = 0
			Imax = 0
	

		if current == 0 and Energy > 0:
			# print("session end ", CurrentList[i])
			end_time = df.loc[i+1,"Time"]
			Duration_str,Duration_Sec  = find_dur(start_time, end_time)
			tmp_df.append([n.name, start_time, end_time,Date,Day, Energy, Imax, Duration_str, Duration_Sec])
			Energy = 0
			Imax = 0






NDF  = pd.DataFrame(tmp_df, columns = ["Name", "Start Time", "End Time", "Date","Day","Energy", "Imax", "Duration_str", "Duration_Sec"])


NDF['Energy'] = NDF['Energy'].div(1000).round(2)

NDF_sorted_Date = NDF.sort_values(['Date', "Start Time"], ascending=[True,  True])
NDF_sorted_Energy = NDF.sort_values(by='Energy', ascending=True)







# NDF_sorted_Date["Duration"] = NDF_sorted_Date["End Time"] - NDF_sorted_Date["Start Time"]

print(NDF_sorted_Date)
NDF_sorted_Date.to_csv("data_new.csv")



#UNSUPERVISED LEARNING 

# df_no_time_no_date = df.drop(columns = ["Time", "Date"])
# print(df_no_time_no_date)


# df_new = pd.get_dummies(df_no_time_no_date)


# print(df_new)
# kmeans = KMeans(n_clusters = 4).fit(df_new)
# centroids = kmeans.cluster_centers_
# print(centroids)


# plt.scatter(df['dayofweek'], df['EM3_L2'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
# plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
# plt.show()





# PHP database extract
#extract data from database and script to convert into plot

#graph for individual session with three currents and energy in Kwh
















#Session   Date   hrs   start time endtime power energy 