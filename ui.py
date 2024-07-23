import streamlit as st
from wfst import WFST, CompositeWFST, composite_wfst, tokenize, extract_numerical_data

# Title of the app
st.title("Text Input and Display App")

# Text input
user_input = st.text_input("Enter some text:")

# Initialize an empty result list
result = []
final_result = []

# Ensure user_input is not empty before processing
if user_input:
    try:
        classified_text = extract_numerical_data(user_input)
        print(classified_text)
        if classified_text and len(classified_text) > 0 and len(classified_text[0]) > 0:
            for j in range(len(classified_text)):
                split_strings = classified_text[j][0].split()
                
                # Initialize a list and add the split strings to it
                result_list = []
                result_list.extend(split_strings)

                input = tokenize(result_list)

                wfst_sequence = []
                for itr in input:
                    wfst = composite_wfst.compose(itr)
                    wfst_sequence.append(wfst)

                composed_wfst = wfst_sequence[0]
                for i in range(1, len(wfst_sequence)):
                    composed_wfst = composed_wfst.compose_alt(wfst_sequence[i])
                result = composed_wfst.process(result_list)
                final_result.append(result)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Submit button
if st.button("Submit"):
    if result:
        # Display the user input
        for res in final_result:
            st.write(res[1])
    else:
        st.write("No numerical data found.")
