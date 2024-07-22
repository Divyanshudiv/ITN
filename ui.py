import streamlit as st
from wfst import WFST, CompositeWFST, composite_wfst

# Title of the app
st.title("Text Input and Display App")

# Text input
user_input = st.text_input("Enter some text:")

split_strings = user_input.split()

# Initialize a list and add the split strings to it
result_list = []
result_list.extend(split_strings)

result1 = composite_wfst.process(result_list)

#print(result1)
# Submit button
if st.button("Submit"):
    # Display the user input
    st.write("You entered:", result1[1])
