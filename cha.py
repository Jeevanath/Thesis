import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans




class Phase:
	def __init__(self, name):
		self.name = name
		self.CurrentList = df[name].tolist()








# def find_Energy(Dct):
	















#OPENING THE INPUT FILE IN READ MODE
f = open('new.asc', 'r')

opf = "C:/Users/uiv06493/OneDrive - Vitesco Technologies/Desktop/char/list.csv"   #FILE LOCATION

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



print(df)


fDate = []
for i in df["Date"]:
	dd = i[:2]
	mm = i[3:5]
	yy = i[6:10]

	fDate.append(yy +"-" + mm + "-" +  dd)

fDate = pd.to_datetime(fDate)
df["Date"] = fDate


df["dayofweek"] = df["Date"].dt.day_name()

print(df)



# EM1_L1_list = df['EM1_L1'].tolist()
# EM1_L2_list = df['EM1_L2'].tolist()
# EM1_L3_list = df['EM1_L3'].tolist()


# EM3_L1_list = df['EM3_L1'].tolist()
# EM3_L2_list = df['EM3_L2'].tolist()
# EM3_L3_list = df['EM3_L3'].tolist()

# EM4_L1_list = df['EM4_L1'].tolist()
# EM4_L2_list = df['EM4_L2'].tolist()
# EM4_L3_list = df['EM4_L3'].tolist()




phase_list = ["EM1_L1", "EM1_L2", "EM1_L3", "EM3_L1", "EM3_L2", "EM3_L3", "EM4_L1", "EM4_L2", "EM4_L3" ]


phase_objs = []

for i in phase_list:
	phase_objs.append(Phase(i))







NDF = pd.DataFrame()

for n in phase_objs:

	tmp_df = pd.DataFrame()
	Energy = 0
	Ts = 300
	Voltage = 220
	CurrentList = n.CurrentList
	for i in range(len(CurrentList)):
		current = CurrentList[i]
		current  = int(current.replace(',', ''))
		if current != 0:
			if Energy == 0:
				start_time = df.at[i+1,"Time"]
				Date = df.at[i+1,"Date"]
			Energy = Energy + (Ts * Voltage * current )
		elif Energy > 0:
			end_time = df.loc[i+1,"Time"]
			tmp_df = pd.DataFrame([n.name, start_time, end_time, Energy, Date])
			print(tmp_df)
			pd.concat([NDF, tmp_df])
			Energy = 0




print(NDF)


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






















#Session   Date   hrs   start time endtime power energy 