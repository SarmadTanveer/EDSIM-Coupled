import streamlit as st
import pandas as pd
import EDSIM_BackEnd.ED_Model3 as model

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
            docs = st.number_input('Number of Doctors', 1, 20, 2, help="Min=381, Max=5000")
        with col2:
            nurse = st.number_input('Number of Nurses', 1, 20, 5, help="Min=381, Max=5000")
        with col3:
            beds = st.number_input('Number of Beds', 1, 40, 10, help="Min=381, Max=5000")
        with col4:     
            resbeds = st.number_input('Number of Resuscitation Beds', 1, 20, 5, help="Min=381, Max=5000")
    
        st.header('Simulation parameters')
        col5, colnull, col6, colnull, col7 = st.columns([2,1,2,1,2])
        with col5: 
            simPar_duration = st.number_input('Duration (mins)', 1440,525600, 1440, help="Min=1440, Max=525600")
        with col6: 
            simPar_iterations = st.number_input('Iterations', 1, 40, 18, help="Min=381, Max=5000")
        with col7: 
            simPar_warmUp = st.number_input('Warm Up Period', 1, 120, 10, help="Min=381, Max=5000")
        
        submit_button = st.form_submit_button('Run Simulation')
    
    if submit_button: 
        if 'scenarioList' not in st.session_state:
            st.error('Simulation can not be run without scenario')
        else:
            scenarioList = st.session_state['scenarioList']
            if (not scenarioList): 
                st.error('Please create a scenario first')
            else:
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
                selectedScenario['warmUp'] = simPar_warmUp
                selectedScenario['length'] = simPar_duration
                del scenarioList        

                with st.spinner('Thanks for waiting, our engine is computing your simulation results...'):
                    patientData,snapshotData = model.runSim(simParameters=selectedScenario)
                    st.session_state['patientData'] = patientData
                    st.session_state['snapshotData'] = snapshotData 
                    st.session_state['selectedScenarioName'] = selectedScenario['name']
                

                
                


    
    @st.cache
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')
    if ('patientData' in st.session_state) and ('snapshotData' in st.session_state):
        st.success('Your result files are ready to download')
        patientDataCsv = convert_df(st.session_state['patientData'])
        snapshotDataCsv = convert_df(st.session_state['snapshotData'])
        name = st.session_state['selectedScenarioName']
        st.download_button(label='Download Patient Data', data=patientDataCsv,file_name=f'{name}_PatientData',mime='text/csv')
        st.download_button(label='Download Snapshot Data', data=snapshotDataCsv,file_name=f'{name}_SnapshotData',mime='text/csv')
            