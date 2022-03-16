import streamlit as st

def app():
    #st.title('Extra Variables')
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

