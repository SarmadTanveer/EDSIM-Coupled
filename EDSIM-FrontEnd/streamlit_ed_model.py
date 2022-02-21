# from numpy.lib.arraysetops import ediff1d
import sys
sys.path.insert(0, '..\EDSIM-Coupled\EDSIM-BackEnd')

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import pandas_bokeh
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
import ED_Model2 as Model
import Statistics as s

#Title at the top 
st.title('Emergency Department Simulation')

# File Upload/Processing
file = st.file_uploader('Upload .csv file with data')
def process_file(file):
    st.write(file)
    df = pd.read_csv(file)
    st.write(df)
if st.button('Process file'):
    process_file(file)

#Inputting Fields/ Sliders for each category 
col1, col2, col3 = st.columns(3)
col2.subheader('Resource Allocation')
col3.subheader('Patient Inter-Arrival Times (mins)')
col1.subheader('Process Service Times (mins)')
with col2:
    docs = st.number_input('Number of Doctors', 1, 5, 2)
    nurse = st.number_input('Number of Nurses', 1, 5, 2)
    beds = st.number_input('Number of Beds', 1, 5, 2)
    resbeds = st.number_input('Number of Resuscitation Beds', 1, 5, 2)
with col3:
    walkInP = st.number_input('Walk-In Patients', 1, 1000, 478)
    AmbulanceP = st.number_input('Ambulance Patients', 1, 50, 9)
with col1:
    CTASass = st.number_input('CTAS Assessment', 1, 50, 42)
    Priorityass = st.number_input('Priority Assessment', 1, 50, 23)
    Initialass = st.number_input('Initial Assessment', 1, 50, 42)
    Dischargeass = st.number_input('Discharge Assessment', 1, 50, 23)
    Treatment = st.number_input('Treatments', 1, 50, 20)
    Bedass = st.number_input('Bed Assignment', 1, 50, 32)
    Resus = st.number_input('Resuscitations', 1, 50, 19)
    Registration = st.number_input('Registrations', 1, 50, 49)
st.header('Simulation Parameters')
simPar_duration = st.number_input('Duration (mins)', 1, 30, 10)
simPar_iterations = st.number_input('Iterations', 5, 40, 18)
simPar_warmUp = st.number_input('Warm Up Period', 1, 30, 10)

simParameters = {
    'resCapacity': {
        'doctor':docs, 
        'nurse':nurse,
        'beds':beds,
        'rBeds':resbeds, 

    }, 
    'pInterArrival':{
        'ambulance':walkInP, 
        'walkIn': AmbulanceP

    }, 
    'serTimes':{
        'priorAssessment': Priorityass, 
        'ctasAssessment':CTASass, 
        'registration':Registration, 
        'bedAssignment':Bedass,
        'initialAssessment':Initialass,
        'treatment':Treatment, 
        'discharge':Dischargeass,
        'resuscitation':Resus 
    }, 
    'ctasDist':{
        'ambulance': {
             1:0.5, 
             2:0.2, 
             3:0.3, 
             4:0.1, 
             5:0
            
        }, 
        'walkIn':{
             1:0.3, 
             2:0.2, 
             3:0.1, 
             4:0.1, 
             5:0.1
        }

    }, 
    'iter':simPar_iterations,
    'warmUp':simPar_warmUp, 
    'length':simPar_duration
}

# Having issues with bokeh and GroupBy pandas data frames.
def plots(df):
        #Group dataframe by Run ID and CTAS Level
        means = s.meanByGroup(df)

        #Mean LOS of grouped dataframe
        meanLOS = s.meanParByCTASperRun(means,'los')

        #Creates ColumnDataSource for Bokeh input
        source_grouped = ColumnDataSource(meanLOS)
        source_df = ColumnDataSource(df)

        p = figure()
        p.title.text = 'Click on legend entries to hide the corresponding lines'

        #p.line(x='Run ID_CTAS', y='los', legend_label='Mean LoS', source=source_grouped)
        p.line(x='Run ID', y='los', source=source_df)
        p.legend.location = "top_left"
        p.legend.click_policy="hide"

        return p

        #fig, axs = plt.subplots(5,figsize=(10,17))
        
        # Subplot for each CTAS level
        # axs[0].plot(meanLOSforCTAS1, 'C0')
        # axs[0].set_xlabel('Run ID')
        # axs[0].set_ylabel('Mean length of stay (min)')
        # axs[0].set_title('Mean Patient Length of Stay per Run ID (CTAS 1-5)')

        # axs[1].plot(meanLOSforCTAS2, 'C1')
        # axs[1].set_xlabel('Run ID')
        # axs[1].set_ylabel('Mean length of stay (min)')

        # axs[2].plot(meanLOSforCTAS3, 'C2')
        # axs[2].set_xlabel('Run ID')
        # axs[2].set_ylabel('Mean length of stay (min)')

        # axs[3].plot(meanLOSforCTAS4, 'C3')
        # axs[3].set_xlabel('Run ID')
        # axs[3].set_ylabel('Mean length of stay (min)')

        # axs[4].plot(meanLOSforCTAS5, 'C4')
        # axs[4].set_xlabel('Run ID')
        # axs[4].set_ylabel('Mean length of stay (min)')

        



#The graphs being displayed/modeled

if st.button('Run Simulation'):
    # Gets results
    results_df = Model.runSim(simParameters)
    # Gets plots
    plots = plots(results_df)
    # Shows the graphs
    st.bokeh_chart(plots, use_container_width=True)
    # Display the results (text)
    summary = s.calculateSummary(results_df)
    #for t in text:
    st.write(0)

# Download .txt file 

#IMPLEMENT HEREEEEEEEEEEEEEEEe



