# This multiapp is a streamlit function used to essentially create another app inside an app
# to create other pages as streamlit does not have that function. I am referencing the Git below
# that was used to do so!
# https://github.com/dataprofessor/multi-page-app

"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self):
        self.pages = []

    def add_page(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.pages.append({
            "title": title,
            "function": func
        })

    def run(self):
        page = st.sidebar.selectbox(
            'Navigation',
            self.pages,
            format_func=lambda page: page['title'])

        page['function']()