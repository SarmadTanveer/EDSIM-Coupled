
import pandas as pd
import matplotlib.pyplot as plt


def read_csv(): 
    df = pd.read_csv('PatientData.csv')
    return df

def calculateSummary(dataframe): 

    avgNumPatientsPerRun = dataframe.groupby(['Run ID']).size().mean()
    groupedByRunCTAS = meanByGroup(dataframe)

    #compute means by ctas for all runs
    meanDataLevel1 =getDataByCTASLevel(groupedByRunCTAS,1).mean()
    meanDataLevel2 =getDataByCTASLevel(groupedByRunCTAS,2).mean()
    meanDataLevel3 =getDataByCTASLevel(groupedByRunCTAS,3).mean()
    meanDataLevel4 =getDataByCTASLevel(groupedByRunCTAS,4).mean()
    meanDataLevel5 =getDataByCTASLevel(groupedByRunCTAS,5).mean()

    groupSizeByRunCTAS = sizeByGroup(dataframe)
    print(groupSizeByRunCTAS) 

    bottleneckProcess,bottleneckTime = calcBottleNeck(dataframe)

    summary = {'Avg Patients per Run':avgNumPatientsPerRun,
                'AVG Patients By CTAS':{
                    1:getDataByCTASLevel(groupSizeByRunCTAS,1).mean(),
                    2:getDataByCTASLevel(groupSizeByRunCTAS,2).mean(),
                    3:getDataByCTASLevel(groupSizeByRunCTAS,3).mean(),
                    4:getDataByCTASLevel(groupSizeByRunCTAS,4).mean(),
                    5:getDataByCTASLevel(groupSizeByRunCTAS,5).mean()
                }, 
                'Avg LOS': meanParAllData(dataframe,'LOS'), 
                'Avg Process Queuing Times': { 
                    'Priority Assessment': {
                    1:meanDataLevel1['Priority Assessment Queue Time'],
                    2:meanDataLevel2['Priority Assessment Queue Time'],
                    3:meanDataLevel3['Priority Assessment Queue Time'],
                    4:meanDataLevel4['Priority Assessment Queue Time'],
                    5:meanDataLevel5['Priority Assessment Queue Time']
                },
                    'CTAS Assessment': {
                    1:meanDataLevel1['CTAS Assessment Queue Time'],
                    2:meanDataLevel2['CTAS Assessment Queue Time'],
                    3:meanDataLevel3['CTAS Assessment Queue Time'],
                    4:meanDataLevel4['CTAS Assessment Queue Time'],
                    5:meanDataLevel5['CTAS Assessment Queue Time']
                },
                    'Registration':{
                    1:meanDataLevel1['Registration Queue Time'],
                    2:meanDataLevel2['Registration Queue Time'],
                    3:meanDataLevel3['Registration Queue Time'],
                    4:meanDataLevel4['Registration Queue Time'],
                    5:meanDataLevel5['Registration Queue Time']
                },
                    'Bed Assignment':{
                    1:meanDataLevel1['Bed Assignment Queue Time'],
                    2:meanDataLevel2['Bed Assignment Queue Time'],
                    3:meanDataLevel3['Bed Assignment Queue Time'],
                    4:meanDataLevel4['Bed Assignment Queue Time'],
                    5:meanDataLevel5['Bed Assignment Queue Time']
                }, 
                    'Initial Assessment':{
                    1:meanDataLevel1['Initial Assessment Queue Time'],
                    2:meanDataLevel2['Initial Assessment Queue Time'],
                    3:meanDataLevel3['Initial Assessment Queue Time'],
                    4:meanDataLevel4['Initial Assessment Queue Time'],
                    5:meanDataLevel5['Initial Assessment Queue Time']
                },
                    'Treatment':{
                    1:meanDataLevel1['Treatment Queue Time'],
                    2:meanDataLevel2['Treatment Queue Time'],
                    3:meanDataLevel3['Treatment Queue Time'],
                    4:meanDataLevel4['Treatment Queue Time'],
                    5:meanDataLevel5['Treatment Queue Time']
                },
                    'Discharge Decision':{
                    1:meanDataLevel1['Discharge Time Stamp'],
                    2:meanDataLevel2['Discharge Time Stamp'],
                    3:meanDataLevel3['Discharge Time Stamp'],
                    4:meanDataLevel4['Discharge Time Stamp'],
                    5:meanDataLevel5['Discharge Time Stamp']
                }, 
                    'Resuscitation': {
                    1:meanDataLevel1['Resuscitation Queue Time'],
                    },
                },
                'Avg Resource Queuing Times':{
                        'Nurse': 1, 
                        'Doctor': 2, 
                        'Bed': 3, 
                        'Resuscitation Bed': 4,  

                }, 
                'BottleNeck': {
                    'Process': bottleneckProcess, 
                    'Avg Time' : bottleneckTime
                }
                }
    return summary

#get LOS data for all ctas levels
def getLOS(data): 
    df = data[['Run ID', 'CTAS', 'LOS']].copy()
    df = df.groupby(['Run ID', 'CTAS']).mean()
    df = df.unstack(0)
    df = df.mean(axis=1)
    return df

#get time patient takes to get to CTAS Assessment
def getTimetoCTAS(data): 
    df = data[['Run ID', 'CTAS', 'Time to CTAS Assessment']].copy()
    df = df.groupby(['Run ID','CTAS']).mean()
    df = df.unstack(0)
   
    df = df.mean(axis=1)
    df = df.drop(index=[1,2],axis=0)
    return df

def getTimeToBedAssignment(data):
    df = data[['Run ID', 'CTAS', 'Time to Bed Assignment']].copy()
    df = df.groupby(['Run ID','CTAS']).mean()
    df = df.unstack(0)
   
    df = df.mean(axis=1)
    df = df.drop(index=[1],axis=0)
    return df

def getTimeToTreatment(data):
    df = data[['Run ID', 'CTAS', 'Time to Treatment']].copy()
    df = df.groupby(['Run ID','CTAS']).mean()
    df = df.unstack(0)
   
    df = df.mean(axis=1)
    df = df.drop(index=[1],axis=0)
    return df

#Calculate process that takes the longest 
def calcBottleNeck(Data): 
    df = meanByGroup(Data, ['Run ID']).drop(columns=['Patient ID', 'Arrival Time Stamp', 'LOS', 'CTAS'])
    max = df.max().max()
    idx = df.max().idxmax()       
    return (idx,max)     

#get all parameter data grouped by run id and CTAS
def meanByGroup(DataFrame,groupLabels = ['Run ID', 'CTAS']): 
    groupedDf = DataFrame.groupby(groupLabels)
    groupMeans = groupedDf.mean()

    return groupMeans
def sizeByGroup(DataFrame,groupLabels = ['Run ID', 'CTAS']): 
    groupedDf = DataFrame.groupby(groupLabels)
    groupMeans = groupedDf.size()

    return groupMeans

#get one parameter data grouped by run id and CTAS
def meanParByCTASperRun(groupMeans,col): 
    means = groupMeans.get([col])

    return means

#after grouping, get data only for specific CTAS Level, returns a series
def getDataByCTASLevel(data, CTASLevel):

    levelDataFrame = data.xs(CTASLevel,level='CTAS')
    return levelDataFrame

#get mean data for one parameter using the entire dataset
def meanParAllData(dataframe,col): 
    return dataframe[col].mean()



#example usage. get avg priority assessment queue time for ctas level 1 per run
#data = read_csv()

# print(calculateSummary(data))

# means = meanByGroup(data)
# #name of col must match exactly to df. use mean.keys() to verify
# meanPriorAssess = meanParByCTASperRun(means,'Priority Assessment Queue Time ')
# print(meanPriorAssess)
# meanPriorAssessforCTAS1 = getDataByCTASLevel(meanPriorAssess, 1)
# print(meanPriorAssessforCTAS1.dtypes)
# print(type(meanPriorAssessforCTAS1)) 
#print(getLOS(data))
# plt.plot(meanPriorAssessforCTAS1)
# plt.show()
