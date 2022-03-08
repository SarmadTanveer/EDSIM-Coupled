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


#Page configurations
st.set_page_config(
     page_title="Emergency Department Simulation",
     layout="wide",
     initial_sidebar_state='auto',
     menu_items={
         'About': "Ryerson Engineering Capstone Project created by: Gurvir, Mike, Renato, Sarmad"
     }
 )
#Side Bar Section
add_selectbox = st.sidebar.selectbox(
    "TEST SIDEBARD",
    ("Graphs", "Tables", "Help!")
)

#Title at the top of page
st.title('Emergency Department Simulation')

# File Upload/Processing
file = st.file_uploader('Upload .csv file with data')


def process_file(file):
    st.write(file)
    df = pd.read_csv(file)
    st.write(df)


if st.button('Process file'):
    process_file(file)

# Inputting Fields/ Sliders for each category
st.header('Process Service Times (mins)')
col01, colnull, col02, colnull, col03, colnull, col04 = st.columns([2,0.5,2,0.5,2,0.5,2])
with col01:
    CTASass = st.number_input('CTAS Assessment (STD)', 1, 50, 42)
    Priorityass = st.number_input('Priority Assessment (STD)', 1, 50, 23)
    Initialass = st.number_input('Initial Assessment (STD)', 1, 50, 42)
    Dischargeass = st.number_input('Discharge (STD)', 1, 50, 23)
with col02:
    CTASass = st.number_input('CTAS Assessment (Mean)', 1, 50, 42)
    Priorityass = st.number_input('Priority Assessment (Mean)', 1, 50, 23)
    Initialass = st.number_input('Initial Assessment (Mean)', 1, 50, 42)
    Dischargeass = st.number_input('Discharge (Mean)', 1, 50, 23)
with col03:
    Treatment = st.number_input('Treatments (STD)', 1, 50, 20)
    Bedass = st.number_input('Bed Assignment (STD)', 1, 50, 32)
    Resus = st.number_input('Resuscitations (STD)', 1, 50, 19)
    Registration = st.number_input('Registrations (STD)', 1, 50, 49)
with col04:
    Treatment = st.number_input('Treatments (Mean)', 1, 50, 20)
    Bedass = st.number_input('Bed Assignment (Mean)', 1, 50, 32)
    Resus = st.number_input('Resuscitations (Mean)', 1, 50, 19)
    Registration = st.number_input('Registrations (Mean)', 1, 50, 49)

col2, colnull, col3, colnull, col4 = st.columns([2,1,2.5,1,2])
col2.subheader('Resource Allocation')
col3.subheader('Inter-Arrival Times (mins)')
col4.subheader('CTAS Distribution')

with col2:
    docs = st.number_input('Number of Doctors', 1, 5, 2, help="Min=381, Max=5000")
    nurse = st.number_input('Number of Nurses', 1, 5, 2, help="Min=381, Max=5000")
    beds = st.number_input('Number of Beds', 1, 5, 2, help="Min=381, Max=5000")
    resbeds = st.number_input('Number of Resuscitation Beds', 1, 5, 2, help="Min=381, Max=5000")
with col3:
    walkInP = st.number_input('Walk-In Patients', 1, 1000, 478, help="Min=381, Max=5000")
    AmbulanceP = st.number_input('Ambulance Patients', 1, 50, 9, help="Min=381, Max=5000")
with col4:
    CTASwalkInP = st.number_input('CTAS Walk-In Patients', 1, 1000, 478, help="Min=381, Max=5000")
    CTASAmbulanceP = st.number_input('CTAS Ambulance Patients', 1, 50, 9, help="Min=381, Max=5000")

st.header('Simulation Parameters')

col5, colnull, col6, colnull, col7 = st.columns([2,1,2,1,2])
with col5: 
    simPar_duration = st.number_input('Duration (mins)', 1, 30, 10, help="Min=381, Max=5000")
with col6: 
    simPar_iterations = st.number_input('Iterations', 5, 40, 18, help="Min=381, Max=5000")
with col7: 
    simPar_warmUp = st.number_input('Warm Up Period', 1, 30, 10, help="Min=381, Max=5000")

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
    # fig, axs = plt.subplots(5,figsize=(10,17))

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


# The graphs being displayed/modeled

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
    
    # Display the results (text)
    
    
    st.title('Summary of Results')
    #summary = s.calculateSummary(results_df)
    #summary = pd.DataFrame.from_dict(summary, orient='index', columns=[''])
    #summary = summary.astype(str)
    #st.dataframe(summary)
    # Raw data frame
    st.title('Raw Simulation Resulting Data')
    AgGrid(results_df)

    # Download button for results csv file
    st.download_button(
        label="Download the Results as .CSV file",
        data=results_df.to_csv().encode('utf-8'),
        file_name='Simulation_Results.csv',
        mime='text/csv')