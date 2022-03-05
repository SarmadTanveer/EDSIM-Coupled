# from numpy.lib.arraysetops import ediff1d
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, BoxAnnotation
from bokeh.palettes import Set1_5
from bokeh.models import ColumnDataSource

from st_aggrid import AgGrid
import EDSIM_BackEnd.ED_Model2 as Model
import EDSIM_BackEnd.Statistics as s

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

#Inputting Fields/ Sliders for each category 
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
def plots(df,losRange=(1000,1500)):
        #Group dataframe by Run ID and CTAS Level
        means = s.meanByGroup(df)

        #Mean LOS of grouped dataframe
        meanLOS = s.meanParByCTASperRun(means,'los')
        
        CTAS1Data = s.getDataByCTASLevel(meanLOS,1)
        CTAS2Data = s.getDataByCTASLevel(meanLOS,2)
        CTAS3Data = s.getDataByCTASLevel(meanLOS,3)
        CTAS4Data = s.getDataByCTASLevel(meanLOS,4)
        CTAS5Data = s.getDataByCTASLevel(meanLOS,5)

        mid_box = BoxAnnotation(bottom=losRange[0], top=losRange[1], fill_alpha=0.2, fill_color='#0072B2')
        
        losCTASData = [CTAS1Data,CTAS2Data,CTAS3Data,CTAS4Data,CTAS5Data]
        graphNames = ['CTAS 1', 'CTAS 2', 'CTAS 3', 'CTAS 4', 'CTAS 5']

        p = figure(x_axis_label = 'RUN ID', y_axis_label = 'MINUTES')
        p.title.text = 'Click on legend entries to hide the corresponding lines'

        for data,name,color in zip(losCTASData,graphNames,Set1_5):
            p.line(data['los'].keys(),data['los'], line_width=2, color=color, alpha=0.8, legend_label=name)

            p.legend.location = "top_left"
            p.legend.click_policy="hide"

        #Creates ColumnDataSource for Bokeh input
        #source_grouped = ColumnDataSource(meanLOS)
        #source_df = ColumnDataSource(df)

        #p = figure()
        #p.title.text = 'Click on legend entries to hide the corresponding lines'

        #p.line(x='Run ID_CTAS', y='los', legend_label='Mean LoS', source=source_grouped)
        #p.line(x='Run ID', y='los', legend_label='LoS', source=source_df)
        p.legend.location = "top_left"
        p.legend.click_policy="hide"

        p.add_layout(mid_box)

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

if st.button('Run the Simulation'):
    # Gets results
    results_df = Model.runSim(simParameters)
    # Gets plots

    
    # Shows the graphs
    st.title('Interactive Plots')
    plot = plots(results_df)
    st.bokeh_chart(plot, use_container_width=True)
    # Display the results (text)
    st.title('Summary of Results')
    summary = s.calculateSummary(results_df)
    summary = pd.DataFrame.from_dict(summary, orient='index', columns=[''])
    summary = summary.astype(str)
    st.dataframe(summary)
    # Raw data frame
    st.title('Raw Simulation Resulting Data')
    AgGrid(results_df)
    
    # Download button for results csv file
    st.download_button(
        label="Download the Results as .CSV file", 
        data=results_df.to_csv().encode('utf-8'), 
        file_name='Simulation_Results.csv', 
        mime='text/csv')




