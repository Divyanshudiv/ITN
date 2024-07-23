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

def tokenize(input_sequence):
    input_sequence_list = []
    buffer = []
    num_states = 0
    for itr in reversed(input_sequence):
        wfst = (composite_wfst.wfsts.get(graph_input_category.get(itr))).states
        if len(wfst) >= num_states and buffer != []:
            num_states = len(wfst)
            input_sequence_list.insert(0, buffer)
            buffer = []
            buffer.insert(0, itr)
        else:
            if buffer == []:
                num_states = len(wfst)
            buffer.insert(0, itr)
    input_sequence_list.insert(0, buffer)
    return input_sequence_list

input = tokenize(result_list)
#print(input)

wfst_sequence = []
for itr in input:
    wfst = composite_wfst.compose(itr)
    #print('itr      :', wfst.states)
    wfst_sequence.append(wfst)

#print('')
composed_wfst = wfst_sequence[0]
for i in range(1, len(wfst_sequence)):
    composed_wfst = composed_wfst.compose_alt(wfst_sequence[i])
result = composed_wfst.process(result_list)

#print(result1)
# Submit button
if st.button("Submit"):
    # Display the user input
    st.write("You entered:", result[1])
