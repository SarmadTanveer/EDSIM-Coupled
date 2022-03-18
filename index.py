import streamlit as st


import EDSIM_BackEnd.ED_Model3 as Model
from multiapp import MultiApp
from EDSIM_FrontEnd import CreateScenario, Home, GTResults, HelpPage

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
    
# simParameters = {
#     'resCapacity': {
#         'doctor': docs,
#         'nurse': nurse,
#         'beds': beds,
#         'rBeds': resbeds,

#     },
#     'pInterArrival': {
#         'ambulance': walkInP,
#         'walkIn': AmbulanceP

#     },
#     'serTimes': {
#         'priorAssessment': Priorityass,
#         'ctasAssessment': CTASass,
#         'registration': Registration,
#         'bedAssignment': Bedass,
#         'initialAssessment': Initialass,
#         'treatment': Treatment,
#         'discharge': Dischargeass,
#         'resuscitation': Resus
#     },
#     'stdDeviations': {
#         'priorAssessment_Deviation': Priorityass_std_dev,
#         'ctasAssessment_Deviation': CTASass_std_dev,
#         'registration_Deviation': Registration_std_dev,
#         'bedAssignment_Deviation': Bedass_std_dev,
#         'initialAssessment_Deviation': Initialass_std_dev,
#         'treatment_Deviation': Treatment_std_dev,
#         'discharge_Deviation': Dischargeass_std_dev,
#         'resuscitation_Deviation': Resus_std_dev
#         },
#     'ctasDist': {
#         'ambulance': {
#             1: 0.5,
#             2: 0.2,
#             3: 0.3,
#             4: 0.1,
#             5: 0

#         },
#         'walkIn': {
#             1: 0.3,
#             2: 0.2,
#             3: 0.1,
#             4: 0.1,
#             5: 0.1
#         }

#     },
#     'iter': simPar_iterations,
#     'warmUp': simPar_warmUp,
#     'length': simPar_duration
# }

if st.button('Process file'):
   process_file(file)

app = MultiApp()
app.add_page("Home", Home.app)
app.add_page("Create Scenario", CreateScenario.app)
app.add_page("Graph and Table Results", GTResults.app)
app.add_page("Help Page", HelpPage.app)
app.run()
# 






