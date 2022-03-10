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

from multiapp import MultiApp
from EDSIM_BackEnd import Home, ExtraVariables

#Page configurations
# st.set_page_config(
#      page_title="Emergency Department Simulation",
#      layout="wide",
#      initial_sidebar_state='auto',
#      menu_items={
#          'About': "Ryerson Engineering Capstone Project created by: Gurvir, Mike, Renato, Sarmad"
#      }
#  )
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
    if st.button('Process file'):
        process_file(file)

app = MultiApp()
app.add_app("Home", Home.app)
app.add_app("Extra Inputs", ExtraVariables.app)
app.run()

# simParameters = {
#     'resCapacity': {
#         'doctor':docs, 
#         'nurse':nurse,
#         'beds':beds,
#         'rBeds':resbeds, 

#     }, 
#     'pInterArrival':{
#         'ambulance':walkInP, 
#         'walkIn': AmbulanceP

#     }, 
#     'serTimes':{
#         'priorAssessment': Priorityass, 
#         'ctasAssessment':CTASass, 
#         'registration':Registration, 
#         'bedAssignment':Bedass,
#         'initialAssessment':Initialass,
#         'treatment':Treatment, 
#         'discharge':Dischargeass,
#         'resuscitation':Resus 
#     }, 
#     'ctasDist':{
#         'ambulance': {
#              1:0.5, 
#              2:0.2, 
#              3:0.3, 
#              4:0.1, 
#              5:0
            
#         }, 
#         'walkIn':{
#              1:0.3, 
#              2:0.2, 
#              3:0.1, 
#              4:0.1, 
#              5:0.1
#         }

#     }, 
#     'iter':simPar_iterations,
#     'warmUp':simPar_warmUp, 
#     'length':simPar_duration
# }

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




