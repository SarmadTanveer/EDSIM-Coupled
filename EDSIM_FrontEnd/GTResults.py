import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, BoxAnnotation
from bokeh.palettes import Set1_5, Set1_3, Set1_4
from bokeh.models import ColumnDataSource
import EDSIM_BackEnd.Statistics as stats
import json


def plotLOS(df):
    
    # Get los means by ctas
    losData = stats.getLOS(df)

    
    # chart labels for x axis
    ctasLevels = ['CTAS 1','CTAS 2','CTAS 3','CTAS 4','CTAS 5']   

    TOOLTIPS = [("Level", "$x"), ("LOS", "$y")] 

    p = figure(x_range = ctasLevels)
    p.vbar(x=ctasLevels,  top=losData, width=0.5,color=Set1_5,legend_group="x")
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center" 


    return p

def plotCTAS(df):
    ctasData = stats.getTimetoCTAS(df)
    
    # chart labels for x axis
    ctasLevels = ['CTAS 3','CTAS 4','CTAS 5']   

    TOOLTIPS = [("Level", "$x"), ("LOS", "$y")] 

    p = figure(x_range = ctasLevels)
    p.vbar(x=ctasLevels,  top=ctasData, width=0.5,color=Set1_3,legend_group="x")
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center" 

    return p

def plotBedAssignment(df):
    bedAssData = stats.getTimeToBedAssignment(df)
    
    # chart labels for x axis
    ctasLevels = ['CTAS 2','CTAS 3','CTAS 4','CTAS 5']   

    TOOLTIPS = [("Level", "$x"), ("LOS", "$y")] 

    p = figure(x_range = ctasLevels)
    p.vbar(x=ctasLevels,  top=bedAssData, width=0.5,color=Set1_4,legend_group="x")
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center" 

    return p

def plotTreatment(df):
    treatmentData = stats.getTimeToTreatment(df)
    
    # chart labels for x axis
    ctasLevels = ['CTAS 2','CTAS 3','CTAS 4','CTAS 5']   

    TOOLTIPS = [("Level", "$x"), ("LOS", "$y")] 

    p = figure(x_range = ctasLevels)
    p.vbar(x=ctasLevels,  top=treatmentData, width=0.5,color=Set1_4,legend_group="x")
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center" 

    return p

def writeSummary(summary_dict):
    colSummary1, colSummary2, colSummary3, colSummary4 = st.columns([1,1,1,1])
    colSummary1.subheader('General Statistics')
    colSummary2.subheader('Average Patients By CTAS')
    colSummary3.subheader('Average Resource Queuing Times')
    colSummary4.subheader('Bottleneck')

def getScatterForPeriodicData(df, col): 
    dfR = df[['Time Stamp', col]].copy()
    dfR = dfR.groupby('Time Stamp').mean()

    p = figure(x_axis_label = 'Simulation Time in mins', y_axis_label = col)
    p.line(dfR.index,dfR[col].values, line_width = 2)

    return p


def ctas1Rrqueue(df): 
    dfR = df[['Run ID','Patient ID','CTAS','Arrival Time Stamp','Resuscitation Bed']].copy()
    dfR = dfR.loc[dfR['CTAS']==1]
    dfR = dfR.loc[dfR['Resuscitation Bed']>0]

    p = figure(x_axis_label = 'Arrival Time in Mins', y_axis_label = 'Waiting time for resuscitation bed in mins')
    p.circle(dfR['Arrival Time Stamp'], dfR['Resuscitation Bed'], size=15)

    return p

def ctas1bins(df): 
    dfR = df[['CTAS','Resuscitation Bed']].copy()
    dfR = dfR.loc[dfR['CTAS'] ==1]
    dfR = dfR.loc[dfR['Resuscitation Bed']>0]

    bins = pd.cut(x=dfR['Resuscitation Bed'], bins=4, include_lowest=True, precision=2)

    ser = bins.value_counts()

    binLabels = []
    for interval in ser.index: 
        binLabels.append(interval.__str__())

    values = (ser.values / sum(ser.values))*100

    p = figure(x_axis_label = 'Resuscitation Bed Queuing Time Intervals', y_axis_label='Probability', x_range= binLabels)
    p.vbar(x=binLabels,  top=values, width=0.5)

    return p

def process_file(file):
    df = pd.read_csv(file)
    return df

def app():
    st.title('Results Page')

    patientDataFile = st.file_uploader('Upload <YourScenarioName>_PatientData.csv to view patient level statistics')
    snapShotDataFile = st.file_uploader('Upload <YourScenarioName>_SnapshotData.csv to view crowding and resource usage statistics')
    summary = None 
    if patientDataFile is not None: 
        results_df = process_file(patientDataFile)

        # Shows the graphs
        st.header('ED KPI Results')

        #Show LOS graph
        los = plotLOS(results_df)
        st.header('Average total Length of Stay in the emergency department  for each CTAS level')
        st.bokeh_chart(los, use_container_width=True)
        
        #Time from Entry to CTASAssessment 
        ctas = plotCTAS(results_df)
        st.header('Average time from entry to CTAS Assessment for each CTAS 3,4,5')
        st.bokeh_chart(ctas, use_container_width=True)

        #Time from triage to Bed Assignemnt 
        bedAss = plotBedAssignment(results_df)
        st.header('Average time from CTAS Assessment to Bed Assignment for each CTAS 2,3,4,5')
        st.bokeh_chart(bedAss, use_container_width=True)

        #Time from triage to Treatment 
        treatment = plotTreatment(results_df)
        st.header('Average time from CTAS Assessment to Treatment for each CTAS 2,3,4,5')
        st.bokeh_chart(treatment, use_container_width=True)

        #Waiting time for resuscitation bed 
        rbedWait = ctas1Rrqueue(results_df)
        st.header('CTAS 1 wait times for resuscitation bed')
        st.bokeh_chart(rbedWait, use_container_width=True)

        #ctas 1 patients binned according to 4 equal intervals 
        rbedBins = ctas1bins(results_df)
        st.header('Probabilty of a CTAS 1 patient waiting a for a resuscitation bed for a specific time interval')
        st.bokeh_chart(rbedBins,use_container_width=True)

        summary = stats.calculateSummary(results_df)


        # Raw data frame
        st.title('Patient Data')
        AgGrid(results_df)
    else: 
        st.error("Upload Patient data to view kpi results")

    
    #display ed state results  
    if snapShotDataFile is not None: 
        spdf = process_file(snapShotDataFile)

        st.header("ED State Results")

        nurseQueue = getScatterForPeriodicData(spdf, 'Nurse Queue Length')
        st.header('Nurse Queue length')
        st.bokeh_chart(nurseQueue, use_container_width=True)

        doctorQueue= getScatterForPeriodicData(spdf, 'Doctor Queue Length')
        st.header('Doctor Queue length')
        st.bokeh_chart(doctorQueue, use_container_width=True)

        bedQueue = getScatterForPeriodicData(spdf, 'Regular Bed Queue Length')
        st.header('Bed Queue length ')
        st.bokeh_chart(bedQueue, use_container_width=True)

        rbedQueue= getScatterForPeriodicData(spdf, 'Resuscitation Bed Queue Length')
        st.header('Resuscitation Bed Queue Length')
        st.bokeh_chart(rbedQueue, use_container_width=True)

        WRCrowding= getScatterForPeriodicData(spdf, 'Patients in waiting room')
        st.header('Crowding in the waiting room prior to registration')
        st.bokeh_chart(WRCrowding, use_container_width=True)

        EDCrowding= getScatterForPeriodicData(spdf, 'Patients in the ED')
        st.header('Crowding in the emergency department')
        st.bokeh_chart(EDCrowding, use_container_width=True)
         
        st.title('SnapShot Data')
        AgGrid(spdf)
    
    else: 
        st.error("Upload Snapshot Data to view emergency department state and resource usage results")

    if summary is not None: 
        st.title('Simulation Summary')

        colSummary1,colSummary2,colSummary3,colSummary4 = st.columns([1,1,1,1])
        colSummary2.subheader('Avge Number of Patients by CTAS Level per Run')
        summary_dict = stats.calculateSummary(results_df)
        with colSummary1:
            st.write('Average Patients per Run: ' + str(round(summary_dict['Avg Patients per Run'], 4)))
            st.write('Average Length of Stay: ' + str(round(summary_dict['Avg LOS'], 4)))
        with colSummary2:
            st.write('CTAS 1: ' + str(round(summary_dict['AVG Patients By CTAS'][1], 4)))
            st.write('CTAS 2: ' + str(round(summary_dict['AVG Patients By CTAS'][2], 4)))
            st.write('CTAS 3: ' + str(round(summary_dict['AVG Patients By CTAS'][3], 4)))
            st.write('CTAS 4: ' + str(round(summary_dict['AVG Patients By CTAS'][4], 4)))
            st.write('CTAS 5: ' + str(round(summary_dict['AVG Patients By CTAS'][5], 4)))
        with colSummary3:
            st.write('Bed: ' + str(round(summary_dict['Avg Resource Queuing Times']['Bed'], 4)))
            st.write('Resuscitation Bed: ' + str(round(summary_dict['Avg Resource Queuing Times']['Resuscitation Bed'], 4)))
        with colSummary4:
            st.write('Process: ' + str(summary_dict['BottleNeck']['Process']))
            st.write('Average Time: ' + str(round(summary_dict['BottleNeck']['Avg Time'],4)))

        colSummary5, colSummary6, colSummary7, colSummary8, colSummary9, colSummary10 = st.columns([1,1,1,1,1,1])
        colSummary5.subheader('Priority Assessment Queue Time')
        colSummary6.subheader('CTAS Assessment Queue Time')
        colSummary7.subheader('Registration Queue Time')
        colSummary8.subheader('Bed Assignment Queue Time')
        colSummary9.subheader('Initial Assessment Queue Time')
        colSummary10.subheader('Treatment Queue Time')

        with colSummary5:
            st.write('CTAS 1: ' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][1], 4)))
            st.write('CTAS 2: ' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][2], 4)))
            st.write('CTAS 3: ' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][3], 4)))
            st.write('CTAS 4: ' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][4], 4)))
            st.write('CTAS 5: ' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][5], 4)))
        with colSummary6:
            st.write('CTAS 1: ' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][1], 4)))
            st.write('CTAS 2: ' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][2], 4)))
            st.write('CTAS 3: ' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][3], 4)))
            st.write('CTAS 4: ' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][4], 4)))
            st.write('CTAS 5: ' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][5], 4)))
        with colSummary7:
            st.write('CTAS 1: ' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][1], 4)))
            st.write('CTAS 2: ' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][2], 4)))
            st.write('CTAS 3: ' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][3], 4)))
            st.write('CTAS 4: ' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][4], 4)))
            st.write('CTAS 5: ' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][5], 4)))
        with colSummary8:
            st.write('CTAS 1: ' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][1], 4)))
            st.write('CTAS 2: ' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][2], 4)))
            st.write('CTAS 3: ' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][3], 4)))
            st.write('CTAS 4: ' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][4], 4)))
            st.write('CTAS 5: ' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][5], 4)))
        with colSummary9:
            st.write('CTAS 1: ' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][1], 4)))
            st.write('CTAS 2: ' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][2], 4)))
            st.write('CTAS 3: ' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][3], 4)))
            st.write('CTAS 4: ' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][4], 4)))
            st.write('CTAS 5: ' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][5], 4)))
        with colSummary10:
            st.write('CTAS 1: ' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][1], 4)))
            st.write('CTAS 2: ' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][2], 4)))
            st.write('CTAS 3: ' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][3], 4)))
            st.write('CTAS 4: ' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][4], 4)))
            st.write('CTAS 5: ' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][5], 4)))

        summaryText = json.dumps(summary)
        st.download_button('Download Summary in Text Format', summaryText, file_name='Summary.txt')

            


    