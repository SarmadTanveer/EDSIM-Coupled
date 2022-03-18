import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, BoxAnnotation
from bokeh.palettes import Set1_5, Set1_3, Set1_4
from bokeh.models import ColumnDataSource

from st_aggrid import AgGrid
import EDSIM_BackEnd.ED_Model3 as Model
import EDSIM_BackEnd.Statistics as stats


from multiapp import MultiApp
from EDSIM_BackEnd import Home, ExtraVariables, GTResults, HelpPage

#Page configurations
st.set_page_config(layout="wide")
#Side Bar Section
#add_selectbox = st.sidebar.selectbox(
    #"App Navigation",
    #("Home", "Data Input", "Graph Display", "Table Display", "Help!")
#)

# File Upload/Processing
file = st.file_uploader('Upload .csv file with data')


def process_file(file):
    st.write(file)
    df = pd.read_csv(file)
    st.write(df)

simParameters = {
    'resCapacity': {
        'doctor': docs,
        'nurse': nurse,
        'beds': beds,
        'rBeds': resbeds,

    },
    'pInterArrival': {
        'ambulance': walkInP,
        'walkIn': AmbulanceP

    },
    'serTimes': {
        'priorAssessment': Priorityass,
        'ctasAssessment': CTASass,
        'registration': Registration,
        'bedAssignment': Bedass,
        'initialAssessment': Initialass,
        'treatment': Treatment,
        'discharge': Dischargeass,
        'resuscitation': Resus
    },
    'stdDeviations': {
        'priorAssessment_Deviation': Priorityass_std_dev,
        'ctasAssessment_Deviation': CTASass_std_dev,
        'registration_Deviation': Registration_std_dev,
        'bedAssignment_Deviation': Bedass_std_dev,
        'initialAssessment_Deviation': Initialass_std_dev,
        'treatment_Deviation': Treatment_std_dev,
        'discharge_Deviation': Dischargeass_std_dev,
        'resuscitation_Deviation': Resus_std_dev
        },
    'ctasDist': {
        'ambulance': {
            1: 0.5,
            2: 0.2,
            3: 0.3,
            4: 0.1,
            5: 0

        },
        'walkIn': {
            1: 0.3,
            2: 0.2,
            3: 0.1,
            4: 0.1,
            5: 0.1
        }

    },
    'iter': simPar_iterations,
    'warmUp': simPar_warmUp,
    'length': simPar_duration
}

if st.button('Process file'):
   process_file(file)

app = MultiApp()
app.add_app("Home", Home.app)
app.add_app("Extra Inputs", ExtraVariables.app)
app.add_app("Graph and Table Results", GTResults.app)
app.add_app("Help Page", HelpPage.app)
app.run()
# 
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

    with colSummary1:
        st.markdown('**Average Patients per Run**: ' + str(round(summary_dict['Avg Patients per Run'], 4)))
        st.markdown('**Average Length of Stay**: ' + str(round(summary_dict['Avg LOS'], 4)))
    with colSummary2:
        st.markdown('**CTAS 1**: ' + str(round(summary_dict['AVG Patients By CTAS'][1], 4)))
        st.markdown('**CTAS 2**: ' + str(round(summary_dict['AVG Patients By CTAS'][2], 4)))
        st.markdown('**CTAS 3**: ' + str(round(summary_dict['AVG Patients By CTAS'][3], 4)))
        st.markdown('**CTAS 4**: ' + str(round(summary_dict['AVG Patients By CTAS'][4], 4)))
        st.markdown('**CTAS 5**: ' + str(round(summary_dict['AVG Patients By CTAS'][5], 4)))
    with colSummary3:
        st.markdown('**Nurse**: ' + str(round(summary_dict['Avg Resource Queuing Times']['Nurse'], 4)))
        st.markdown('**Doctor**: ' + str(round(summary_dict['Avg Resource Queuing Times']['Doctor'], 4)))
        st.markdown('**Bed**: ' + str(round(summary_dict['Avg Resource Queuing Times']['Bed'], 4)))
        st.markdown('**Resuscitation Bed**: ' + str(round(summary_dict['Avg Resource Queuing Times']['Resuscitation Bed'], 4)))
    with colSummary4:
        st.markdown('**Process**: ' + str(summary_dict['BottleNeck']['Process']))
        st.markdown('**Average Time**: ' + str(summary_dict['BottleNeck']['Avg Time']))

    colSummary5, colSummary6, colSummary7, colSummary8, colSummary9, colSummary10, colSummary11 = st.columns([1,1,1,1,1,1,1])
    colSummary5.subheader('Priority Assessment Queue Time')
    colSummary6.subheader('CTAS Assessment Queue Time')
    colSummary7.subheader('Registration Queue Time')
    colSummary8.subheader('Bed Assignment Queue Time')
    colSummary9.subheader('Initial Assessment Queue Time')
    colSummary10.subheader('Treatment Queue Time')
    colSummary11.subheader('Discharge Time')

    with colSummary5:
        st.markdown('**CTAS 1**: ' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][1], 4)))
        st.markdown('**CTAS 2**: ' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][2], 4)))
        st.markdown('**CTAS 3**: ' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][3], 4)))
        st.markdown('**CTAS 4**: ' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][4], 4)))
        st.markdown('**CTAS 5**: ' + str(round(summary_dict['Avg Process Queuing Times']['Priority Assessment'][5], 4)))
    with colSummary6:
        st.markdown('**CTAS 1**: ' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][1], 4)))
        st.markdown('**CTAS 2**: ' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][2], 4)))
        st.markdown('**CTAS 3**: ' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][3], 4)))
        st.markdown('**CTAS 4**: ' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][4], 4)))
        st.markdown('**CTAS 5**: ' + str(round(summary_dict['Avg Process Queuing Times']['CTAS Assessment'][5], 4)))
    with colSummary7:
        st.markdown('**CTAS 1**: ' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][1], 4)))
        st.markdown('**CTAS 2**: ' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][2], 4)))
        st.markdown('**CTAS 3**: ' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][3], 4)))
        st.markdown('**CTAS 4**: ' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][4], 4)))
        st.markdown('**CTAS 5**: ' + str(round(summary_dict['Avg Process Queuing Times']['Registration'][5], 4)))
    with colSummary8:
        st.markdown('**CTAS 1**: ' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][1], 4)))
        st.markdown('**CTAS 2**: ' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][2], 4)))
        st.markdown('**CTAS 3**: ' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][3], 4)))
        st.markdown('**CTAS 4**: ' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][4], 4)))
        st.markdown('**CTAS 5**: ' + str(round(summary_dict['Avg Process Queuing Times']['Bed Assignment'][5], 4)))
    with colSummary9:
        st.markdown('**CTAS 1**: ' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][1], 4)))
        st.markdown('**CTAS 2**: ' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][2], 4)))
        st.markdown('**CTAS 3**: ' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][3], 4)))
        st.markdown('**CTAS 4**: ' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][4], 4)))
        st.markdown('**CTAS 5**: ' + str(round(summary_dict['Avg Process Queuing Times']['Initial Assessment'][5], 4)))
    with colSummary10:
        st.markdown('**CTAS 1**: ' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][1], 4)))
        st.markdown('**CTAS 2**: ' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][2], 4)))
        st.markdown('**CTAS 3**: ' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][3], 4)))
        st.markdown('**CTAS 4**: ' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][4], 4)))
        st.markdown('**CTAS 5**: ' + str(round(summary_dict['Avg Process Queuing Times']['Treatment'][5], 4)))
    with colSummary11:
        st.markdown('**CTAS 1**: ' + str(round(summary_dict['Avg Process Queuing Times']['Discharge Decision'][1], 4)))
        st.markdown('**CTAS 2**: ' + str(round(summary_dict['Avg Process Queuing Times']['Discharge Decision'][2], 4)))
        st.markdown('**CTAS 3**: ' + str(round(summary_dict['Avg Process Queuing Times']['Discharge Decision'][3], 4)))
        st.markdown('**CTAS 4**: ' + str(round(summary_dict['Avg Process Queuing Times']['Discharge Decision'][4], 4)))
        st.markdown('**CTAS 5**: ' + str(round(summary_dict['Avg Process Queuing Times']['Discharge Decision'][5], 4)))


if st.button('Run the Simulation'):
    # Gets results
    results_df = Model.runSim(simParameters)
    # Gets plots

    # Shows the graphs
    st.title('Results')

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
    st.title('Summary of Results')
    st.write('Note: All time values in minutes.')
    summary = stats.calculateSummary(results_df)
    writeSummary(summary)




    # Raw data frame
    st.title('Raw Simulation Resulting Data')
    AgGrid(results_df)

    # Download button for results csv file
    st.download_button(
        label="Download the Results as .CSV file",
        data=results_df.to_csv().encode('utf-8'),
        file_name='Simulation_Results.csv',
        mime='text/csv')