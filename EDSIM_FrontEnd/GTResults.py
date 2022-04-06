import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, BoxAnnotation
from bokeh.palettes import Set1_5, Set1_3, Set1_4
from bokeh.models import ColumnDataSource
import EDSIM_BackEnd.Statistics as stats


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

def ctas1Rrqueue(df): 
    return df

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
        st.write('Nurse: ' + str(round(summary_dict['Avg Resource Queuing Times']['Nurse'], 4)))
        st.write('Doctor: ' + str(round(summary_dict['Avg Resource Queuing Times']['Doctor'], 4)))
        st.write('Bed: ' + str(round(summary_dict['Avg Resource Queuing Times']['Bed'], 4)))
        st.write('Resuscitation Bed: ' + str(round(summary_dict['Avg Resource Queuing Times']['Resuscitation Bed'], 4)))
    with colSummary4:
        st.write('Process: ' + str(summary_dict['BottleNeck']['Process']))
        st.write('Average Time: ' + str(summary_dict['BottleNeck']['Avg Time']))

    colSummary5, colSummary6, colSummary7, colSummary8, colSummary9, colSummary10, colSummary11 = st.columns([1,1,1,1,1,1,1])
    colSummary5.subheader('Priority Assessment Queue Time')
    colSummary6.subheader('CTAS Assessment Queue Time')
    colSummary7.subheader('Registration Queue Time')
    colSummary8.subheader('Bed Assignment Queue Time')
    colSummary9.subheader('Initial Assessment Queue Time')
    colSummary10.subheader('Treatment Queue Time')
    colSummary11.subheader('Discharge Time')

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
    with colSummary11:
        st.write('CTAS 1: ' + str(round(summary_dict['Avg Process Queuing Times']['Discharge Decision'][1], 4)))
        st.write('CTAS 2: ' + str(round(summary_dict['Avg Process Queuing Times']['Discharge Decision'][2], 4)))
        st.write('CTAS 3: ' + str(round(summary_dict['Avg Process Queuing Times']['Discharge Decision'][3], 4)))
        st.write('CTAS 4: ' + str(round(summary_dict['Avg Process Queuing Times']['Discharge Decision'][4], 4)))
        st.write('CTAS 5: ' + str(round(summary_dict['Avg Process Queuing Times']['Discharge Decision'][5], 4)))

def process_file(file):
    df = pd.read_csv(file)
    return df

def app():
    st.title('Results Page')

    patientDataFile = st.file_uploader('Upload <YourScenarioName>_PatientData.csv to view patient level statistics')
    snapShotDataFile = st.file_uploader('Upload <YourScenarioName>_SnapshotData.csv to view crowding and resource usage statistics')

    if patientDataFile is not None: 
        results_df = process_file(patientDataFile)



        # Shows the graphs
        st.header('Results')

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
        bedAss = plotTreatment(results_df)
        st.header('Average time from CTAS Assessment to Treatment for each CTAS 2,3,4,5')
        st.bokeh_chart(bedAss, use_container_width=True)
        
        # Display the summary results (text)
        # st.title('Summary of Results')
        # st.write('Note: All time values in minutes.')
        # summary = stats.calculateSummary(results_df)
        # writeSummary(summary)




        # Raw data frame
        st.title('Raw Simulation Resulting Data')
        AgGrid(results_df)

        # Download button for results csv file
        st.download_button(
            label="Download the Results as .CSV file",
            data=results_df.to_csv().encode('utf-8'),
            file_name='Simulation_Results.csv',
            mime='text/csv')