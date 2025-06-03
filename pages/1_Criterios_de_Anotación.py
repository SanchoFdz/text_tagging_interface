import streamlit as st

st.title("Should Uber Hire Me? (please)")

options = st.multiselect(
    "Select your answer(s):",
    ["Yes", "No", "Maybe"]
)

if options:
    st.write("You selected:", ", ".join(options))
else:
    st.write("Please make a selection.")
