import streamlit as st
import pandas as pd

def app():
    #Title at the top of page
    st.title('Emergency Department Simulation')

    #Inputting Fields/ Sliders for each category 

    with st.form('simulationParameters'):
        st.header('Scenario to run')
        if 'scenarioList' not in st.session_state:
            st.write('Please create a scenario first before running this simulation')
        else: 
            scenarioList = st.session_state['scenarioList']
            if (not scenarioList):
                st.write('Please create a scenario first')
            else: 
                scenarioNames = []
                for scenario in scenarioList: 
                    scenarioNames.append(scenario['name'])
                option = st.selectbox('Choose scenario you would like to run', scenarioNames)
                del scenarioList
            

  
        st.header('Resource allocation parameters')
        col1, col2, col3,col4 = st.columns(4)
        with col1:
            docs = st.number_input('Number of Doctors', 1, 5, 2, help="Min=381, Max=5000")
        with col2:
            nurse = st.number_input('Number of Nurses', 1, 5, 2, help="Min=381, Max=5000")
        with col3:
            beds = st.number_input('Number of Beds', 1, 5, 2, help="Min=381, Max=5000")
        with col4:     
            resbeds = st.number_input('Number of Resuscitation Beds', 1, 5, 2, help="Min=381, Max=5000")
    
        st.header('Simulation parameters')
        col5, colnull, col6, colnull, col7 = st.columns([2,1,2,1,2])
        with col5: 
            simPar_duration = st.number_input('Duration (mins)', 1, 30, 10, help="Min=381, Max=5000")
        with col6: 
            simPar_iterations = st.number_input('Iterations', 5, 40, 18, help="Min=381, Max=5000")
        with col7: 
            simPar_warmUp = st.number_input('Warm Up Period', 1, 30, 10, help="Min=381, Max=5000")
        
        submit_button = st.form_submit_button('Run Simulation')
    
    if submit_button: 
        resCapacity = {
        'doctor': docs,
        'nurse': nurse,
        'beds': beds,
        'rBeds': resbeds,}


        scenarioList = st.session_state['scenarioList']
        for scenario in scenarioList: 
            if scenario['name'] == option:
                selectedScenario = scenario
                break 

        selectedScenario['resCapacity'] = resCapacity
        selectedScenario['iter'] = simPar_iterations
        selectedScenario['warmup'] = simPar_warmUp
        selectedScenario['length'] = simPar_duration
        del scenarioList        
        st.write(selectedScenario)
    