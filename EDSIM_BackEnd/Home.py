import streamlit as st
import pandas as pd

def app():
    #Title at the top of page
    st.title('Emergency Department Simulation')

    #Inputting Fields/ Sliders for each category 

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