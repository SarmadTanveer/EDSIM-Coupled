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

    if dfR.empty: 
        raise Exception("DataFrame Empty")
    else:
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
        
        st.header('Average total Length of Stay in the emergency department  for each CTAS level')
        try: 
            #Show LOS graph
            los = plotLOS(results_df)
            st.bokeh_chart(los, use_container_width=True)
        except:  
            st.error("Not enough data to generate this graph")      

        st.header('Average time from entry to CTAS Assessment for each CTAS 3,4,5')    
        try: 
            #Time from Entry to CTASAssessment 
            ctas = plotCTAS(results_df)
            st.bokeh_chart(ctas, use_container_width=True)
        except: 
            st.error("Not enough data to generate this graph")

        st.header('Average time from CTAS Assessment to Bed Assignment for each CTAS 2,3,4,5')
        try:
            #Time from triage to Bed Assignemnt 
            bedAss = plotBedAssignment(results_df)
            
            st.bokeh_chart(bedAss, use_container_width=True)
        except: 
            st.error("Not enough data to generate this graph")

        st.header('Average time from CTAS Assessment to Treatment for each CTAS 2,3,4,5')
        try: 
            #Time from triage to Treatment 
            treatment = plotTreatment(results_df)
            
            st.bokeh_chart(treatment, use_container_width=True)
        except: 
            st.error("Not enough data to generate this graph")

        st.header('CTAS 1 wait times for resuscitation bed')
        try:     
            #Waiting time for resuscitation bed 
            rbedWait = ctas1Rrqueue(results_df)
            
            st.bokeh_chart(rbedWait, use_container_width=True)
        except: 
            st.error("Not enough data to generate this graph")

        st.header('Probabilty of a CTAS 1 patient waiting a for a resuscitation bed for a specific time interval')
        try: 
            #ctas 1 patients binned according to 4 equal intervals 
            rbedBins = ctas1bins(results_df)
            st.bokeh_chart(rbedBins,use_container_width=True)
        except: 
            st.error("Not enough data to generate this graph")

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

        st.header('Nurse Queue length')
        try:
            nurseQueue = getScatterForPeriodicData(spdf, 'Nurse Queue Length')
            
            st.bokeh_chart(nurseQueue, use_container_width=True)
        except:
            st.error("Not enough data to generate this graph")
             
        st.header('Doctor Queue length')
        try:     
            doctorQueue= getScatterForPeriodicData(spdf, 'Doctor Queue Length')
        
            st.bokeh_chart(doctorQueue, use_container_width=True)
        except: 
            st.error("Not enough data to generate this graph")

        st.header('Bed Queue length ')
        try: 
            bedQueue = getScatterForPeriodicData(spdf, 'Regular Bed Queue Length')
            st.bokeh_chart(bedQueue, use_container_width=True)
        except: 
            st.error("Not enough data to generate this graph")

        st.header('Resuscitation Bed Queue Length')
        try: 
            rbedQueue= getScatterForPeriodicData(spdf, 'Resuscitation Bed Queue Length')
            st.bokeh_chart(rbedQueue, use_container_width=True)
        except: 
            st.error("Not enough data to generate this graph")

        st.header('Crowding in the waiting room prior to registration')
        try:     
            WRCrowding= getScatterForPeriodicData(spdf, 'Patients in waiting room')
            st.bokeh_chart(WRCrowding, use_container_width=True)
        except: 
            st.error("Not enough data to generate this graph")

        st.header('Crowding in the emergency department')
        try: 
            EDCrowding= getScatterForPeriodicData(spdf, 'Patients in the ED')
            st.bokeh_chart(EDCrowding, use_container_width=True)
        except: 
            st.error("Not enough data to generate this graph")

        st.title('SnapShot Data')
        AgGrid(spdf)
    
    else: 
        st.error("Upload Snapshot Data to view emergency department state and resource usage results")

    if summary is not None: 
        summary_dict = stats.calculateSummary(results_df)
        st.title('Simulation Summary')
        st.markdown('<b>Note:</b> All time values in minutes.', unsafe_allow_html=True)

        colSummary1,colSummary2 = st.columns([1,1])
        with colSummary1:
            st.markdown('<h2><b><ins>General Statistics</ins></b></h2>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Average Patients per Run:</b> <em>' + str(round(summary_dict['Avg Patients per Run'], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Average Length of Stay:</b> <em>' + str(round(summary_dict['Avg LOS'], 2)), unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Average Bed Queue Times:</b> <em>' + str(round(summary_dict['Avg Resource Queuing Times']['Bed'], 2)), unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Average Resuscitation Bed Queue Times:</b> <em>' + str(round(summary_dict['Avg Resource Queuing Times']['Resuscitation Bed'], 2)), unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Bottleneck Process and Avg Time:</b> <em>' + str(summary_dict['BottleNeck']['Process']) + ' - ' + str(round(summary_dict['BottleNeck']['Avg Time'], 2)), unsafe_allow_html=True)
        with colSummary2:
            st.markdown('<h2><b><ins>Average Patients by CTAS Level</ins></b></h2>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>CTAS 1:</b> <em>' + str(round(summary_dict['AVG Patients By CTAS'][1], 2)) + ' patients/run</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>CTAS 2:</b> <em>' + str(round(summary_dict['AVG Patients By CTAS'][2], 2)) + ' patients/run</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>CTAS 3:</b> <em>' + str(round(summary_dict['AVG Patients By CTAS'][3], 2)) + ' patients/run</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>CTAS 4:</b> <em>' + str(round(summary_dict['AVG Patients By CTAS'][4], 2)) + ' patients/run</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>CTAS 5:</b> <em>' + str(round(summary_dict['AVG Patients By CTAS'][5], 2)) + ' patients/run</em>', unsafe_allow_html=True)

        st.markdown('<h2><b><ins>Average Process Queuing Times</ins></b></h2>', unsafe_allow_html=True)

        colSummary6, colSummary7, colSummary8, colSummary9, colSummary10 = st.columns([1,1,1,1,1])
        with colSummary6:
            st.markdown('<h3><b><ins>CTAS 1</ins></b></h3>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Priority Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][1], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>CTAS Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][1], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Registration:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][1], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Bed Assignment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][1], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Initial Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][1], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Treatment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][1], 2)) + '</em>', unsafe_allow_html=True)
        with colSummary7:
            st.markdown('<h3><b><ins>CTAS 2</ins></b></h3>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Priority Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][2], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>CTAS Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][2], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Registration:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][2], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Bed Assignment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][2], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Initial Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][2], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Treatment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][2], 2)) + '</em>', unsafe_allow_html=True)
        with colSummary8:
            st.markdown('<h3><b><ins>CTAS 3</ins></b></h3>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Priority Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][3], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>CTAS Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][3], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Registration:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][3], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Bed Assignment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][3], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Initial Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][3], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Treatment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][3], 2)) + '</em>', unsafe_allow_html=True)
        with colSummary9:
            st.markdown('<h3><b><ins>CTAS 4</ins></b></h3>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Priority Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][4], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>CTAS Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][4], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Registration:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][4], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Bed Assignment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][4], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Initial Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][4], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Treatment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][4], 2)) + '</em>', unsafe_allow_html=True)
        with colSummary10:
            st.markdown('<h3><b><ins>CTAS 5</ins></b></h3>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Priority Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][5], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>CTAS Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][5], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Registration:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][5], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Bed Assignment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][5], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Initial Assessment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][5], 2)) + '</em>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:20px;"><b>Treatment:</b> <em>' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][5], 2)) + '</em>', unsafe_allow_html=True)

        summaryText = json.dumps(summary)
        st.download_button('Download Summary in Text Format', summaryText, file_name='Summary.txt')

            


    