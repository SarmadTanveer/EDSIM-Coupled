import streamlit as st


import EDSIM_BackEnd.ED_Model3 as Model
from multiapp import MultiApp
from EDSIM_FrontEnd import CreateScenario, Home, GTResults, HelpPage, FAQ

st.set_page_config(layout="wide")

app = MultiApp()
app.add_page("Welcome", HelpPage.app)
app.add_page("Help Page", FAQ.app)
app.add_page("Create Scenario", CreateScenario.app)
app.add_page("Run Created Scenario", Home.app)
app.add_page("Graph and Table Results", GTResults.app)

app.run()
# 






