import streamlit as st

def app():
    st.title('Create a Scenario')
    if 'scenarioList' not in st.session_state:
        st.session_state['scenarioList'] = []

    with st.form("CreateScenario"): 
        st.write("Usage: Enter appropriate patient arrival times, CTAS distribution and process service times to create a scenario. If a scenario is not created, default scenario will be used for the simulation. Additionally you can name your scenario and save it")
        
        scenarioName = st.text_input("Scenario Name", value="", max_chars=30, key="name")
        #Patient Inter Arrival Times 
        st.header("Patient Inter Arrival Times in mins")
        col01, col02 = st.columns(2)
        with col01:
            walkInInter = st.number_input('Walk-In Patients', 1.0, 120.0, 10.0, step= 0.1,help="Min=1, Max=120")
        
        with col02:
            ambulanceInter = st.number_input('Ambulance Patients',1.0,120.0,15.0,step=0.1,help="Min=1, Max=120")

        #CTAS Distribution
        st.header("Patient CTAS Distribution as a percentage")
        st.subheader("Walk In Patients")
        col03,col04,col05,col06,col07 = st.columns(5)
        with col03:
            wCtas1 = st.number_input('CTAS Level 1', 0.0,100.0,20.0, key = "w1", step=0.1,help='Min=0, Max=100')
        with col04:
            wCtas2 = st.number_input('CTAS Level 2', 0.0,100.0,20.0, key = "w2",step=0.1,help='Min=0, Max=100')
        with col05:
            wCtas3 = st.number_input('CTAS Level 3', 0.0,100.0,20.0, key = "w3",step=0.1,help='Min=0, Max=100')
        with col06:
            wCtas4 = st.number_input('CTAS Level 4', 0.0,100.0,20.0, key = "w4",step=0.1,help='Min=0, Max=100')
        with col07:
            wCtas5 = st.number_input('CTAS Level 5', 0.0,100.0,20.0, key = "w5",step=0.1,help='Min=0, Max=100')  
        
        st.subheader("Ambulance Patients")
        col08,col09,col10,col11,col12 = st.columns(5)
        with col08:
            aCtas1 = st.number_input('CTAS Level 1', 0.0,100.0,20.0, key = "a1",step=0.1,help='Min=0, Max=100')
        with col09:
            aCtas2 = st.number_input('CTAS Level 2', 0.0,100.0,20.0, key = "a2",step=0.1,help='Min=0, Max=100')
        with col10:
            aCtas3 = st.number_input('CTAS Level 3', 0.0,100.0,20.0, key = "a3",step=0.1,help='Min=0, Max=100')
        with col11:
            aCtas4 = st.number_input('CTAS Level 4', 0.0,100.0,20.0, key = "a4",step=0.1,help='Min=0, Max=100')
        with col12:
            aCtas5 = st.number_input('CTAS Level 5', 0.0,100.0,20.0, key = "a5",step=0.1,help='Min=0, Max=100')  
        
        #Process Service Times 
        st.header('Process Service Times in mins')
        col13,col14,col15,col16 = st.columns(4)
        with col13:
            CTASass_std_dev = st.number_input('CTAS Assessment (STD)', 1.0, 50.0, 42.0,step=0.1)
            Priorityass_std_dev = st.number_input('Priority Assessment (STD)', 1.0, 50.0, 23.0,step=0.1)
            Initialass_std_dev = st.number_input('Initial Assessment (STD)', 1.0, 50.0, 42.0,step=0.1)
            Dischargeass_std_dev = st.number_input('Discharge (STD)', 1.0, 50.0, 23.0,step=0.1)
        with col14:
            CTASass = st.number_input('CTAS Assessment (Mean)', 1.0, 50.0, 42.0,step=0.1,)
            Priorityass = st.number_input('Priority Assessment (Mean)', 1.0, 50.0, 23.0,step=0.1)
            Initialass = st.number_input('Initial Assessment (Mean)', 1.0, 50.0, 42.0,step=0.1)
            Dischargeass = st.number_input('Discharge (Mean)', 1.0, 50.0, 23.0,step=0.1)
        with col15:
            Treatment_std_dev = st.number_input('Treatments (STD)', 1.0, 50.0, 20.0,step=0.1)
            Bedass_std_dev = st.number_input('Bed Assignment (STD)', 1.0, 50.0, 32.0,step=0.1)
            Resus_std_dev = st.number_input('Resuscitations (STD)', 1.0, 50.0, 19.0,step=0.1)
            Registration_std_dev = st.number_input('Registrations (STD)', 1.0, 50.0, 49.0,step=0.1)
        with col16:
            Treatment = st.number_input('Treatments (Mean)', 1.0, 50.0, 20.0,step=0.1)
            Bedass = st.number_input('Bed Assignment (Mean)', 1.0, 50.0, 32.0,step=0.1)
            Resus = st.number_input('Resuscitations (Mean)', 1.0, 50.0, 19.0,step=0.1)
            Registration = st.number_input('Registrations (Mean)', 1.0, 50.0, 49.0,step=0.1)
        
        
        
        submit_button = st.form_submit_button(label="Create Scenario")
    
    if submit_button:
        scenarioDetails = {
        'name': scenarioName,
        'pInterArrival': {
            'ambulance': walkInInter,
            'walkIn': ambulanceInter

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
            'walkin': {
                1: wCtas1/100,
                2: wCtas2/100,
                3: wCtas3/100,
                4: wCtas4/100,
                5: wCtas5/100
            },
            'ambulance': {
                1: aCtas1/100,
                2: aCtas2/100,
                3: aCtas3/100,
                4: aCtas4/100,
                5: aCtas5/100
            }
        } 
        }   

        createScenario(scenarioDetails)
        
        


    
    
    

def createScenario(scenario): 
    if(formValidation(scenario['name'],scenario['ctasDist'])):
        st.write('Validation passed')
        scenarioList = st.session_state['scenarioList']
        scenarioList.append(scenario)
        st.session_state['scenarioList'] = scenarioList
        del scenarioList
        st.write('Scenario created and added to scenario list')

    else: 
        st.write('Please check inputs') 

def formValidation(name,ctasDist):
    walkinSum = sum(ctasDist['walkin'].values())
    ambulanceSum = sum(ctasDist['ambulance'].values())
    scenarioList = st.session_state['scenarioList']
    for scenario in scenarioList:
        if scenario['name'] == name:
            st.write('Duplicate scenario names are not allowed')
            return False
    del scenarioList
            
         
    if(not name):
        st.write('Name cannot be blank')
        return False
    elif (walkinSum != 1):
        st.write('Walkin CTAS distribution doesnot add upto 100')
        return False
    elif(ambulanceSum != 1):
        st.write('Ambulance CTAS distribution doesnot add upto 100')
        return False
    else: 
        return True
       