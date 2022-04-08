import streamlit as st

def app():
    st.title('Emegency Department Simulator')
    st.header('What is this tool?')
    st.markdown('<p style="font-size:14pt"><em>This tool is used to simulate an emergency department in a hospital using the Monte-Carlo model. Through the use of this tool, doctors and hospital staff will be able to make better insights and help with the development at their local hospitals with the given inputted policies and data.', unsafe_allow_html=True)
    st.header('How do I use it?')
    st.markdown('<p style="font-size:14pt"><em>Please feel free to use the navigation tab on the left and go through each tab one at a time. If you have any questions about the differernt variables, feel free to click on the "Help Page" tab.', unsafe_allow_html=True)
    st.header('Who created this?')
    st.markdown('<p style="font-size:14pt"><em>This tool was created as a Capstone Design Project by the Graduating class of 2022 from Ryersons Computer Engineering program. The group members consist of Sarmad Tanveer, Gurvir Parmar, Michael Kobty & Renato Ramos.', unsafe_allow_html=True)