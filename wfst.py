import spacy
from spacy.matcher import Matcher

graph_input_category = {}

class WFST:
    def __init__(self, title):
        self.category = title
        self.states = {}
        self.start_state = None
        self.final_state = set()

    def set_start_state(self, state):
        self.start_state = state

    def add_state(self, state):
        if state not in self.states:
            self.states[state] = {}

    def add_final_state(self, state):
        self.final_state.add(state)

    def add_transition(self, from_state, to_state, input_symbol, output_symbol, weight=0):
        self.add_state(from_state)
        self.add_state(to_state)
        keys = list(graph_input_category.keys())
        if input_symbol not in keys:
            graph_input_category[input_symbol] = self.category
        if input_symbol not in self.states[from_state]:
            self.states[from_state][input_symbol] = []
        self.states[from_state][input_symbol].append((to_state, output_symbol, weight))

    def add_epsilon_transition(self, from_state, to_state, output_symbol, weight=0):
        self.add_transition(from_state, to_state, '', output_symbol, weight)

    def insert(self, start_state, num_transitions, output_symbol):
        current_state = start_state
        for i in range(num_transitions):
            new_state = current_state + 1
            self.add_epsilon_transition(current_state, new_state, output_symbol)
            current_state = new_state
        self.add_final_state(current_state)

    def process(self, input_sequence): 
        current_output = ''
        current_weight = 0
        next_states = []
        for state in self.states:
            if state not in self.final_state:
                values = list(self.states[state].values())
                next_state = 0
                output_symbol = ''
                weight = 10**10
                for itr in values:
                    for (buffer_next_state, buffer_output_symbol, buffer_weight) in itr:
                        if weight >= buffer_weight:
                            next_state = buffer_next_state
                            output_symbol = buffer_output_symbol
                            weight = buffer_weight
                next_states.append((next_state, current_output + output_symbol, current_weight + weight))
                current_output += output_symbol
                current_weight += weight

        return next_states[len(next_states) - 1]

    def compose(self, other, input):
        result = WFST(self.category + other.category)
        result.set_start_state(0)
        i = 0
        for s1 in self.states:
            i = s1  
            if s1 not in self.final_state:
                for symbol1 in self.states[s1]:
                    for (n1, o1, w1) in self.states[s1][symbol1]:
                        result.add_transition(i, i + 1, symbol1, o1, w1)
        if len(self.states) > len(other.states):
            i = i - len(other.states) + 1
        for s1 in other.states:
            if s1 not in other.final_state:
                if input == []:
                    symbol = None
                elif isinstance(input, list):
                    symbol = input[0]
                else:
                    symbol = input
                if symbol in other.states[s1]:
                    for (next_state, output_symbol, weight) in other.states[s1][symbol]:
                        result.add_transition(i, i + 1, symbol, output_symbol, weight)
                        if isinstance(input, list):
                            input.pop(0)
                elif '' in other.states[s1]:
                    for (next_state, output_symbol, weight) in other.states[s1]['']:
                        result.add_transition(i, i + 1, '', output_symbol, weight)
                        break
            i += 1

        result.add_final_state(i - 1)
        return result
    
    def compose_alt(self, other):
        result = WFST(self.category + other.category)
        result.set_start_state(0)
        i = 0
        for s1 in self.states:
            i = s1  
            if s1 not in self.final_state:
                for symbol1 in self.states[s1]:
                    for (n1, o1, w1) in self.states[s1][symbol1]:
                        result.add_transition(i, i + 1, symbol1, o1, w1)
        if len(self.states) > len(other.states):
            i = i - len(other.states) + 1
        for s1 in other.states:
            if s1 not in other.final_state:
                for symbol1 in other.states[s1]:
                    for (n1, o1, w1) in other.states[s1][symbol1]:
                        result.add_transition(i, i + 1, symbol1, o1, w1)
            i += 1

        result.add_final_state(i - 1)
        return result
    
    def output(self, wfst, input_sequence):
        if not isinstance(wfst, CompositeWFST):
            composite_wfst = CompositeWFST()
            composite_wfst.add_wfst('name', wfst)
        else:
            composite_wfst = wfst
        
        wfst_sequence = []
        for itr in input_sequence:
            wfst = composite_wfst.compose(itr)
            wfst_sequence.append(wfst)

        composite_wfst = wfst_sequence[0]
        for i in range(1, len(wfst_sequence)):
            composite_wfst= composite_wfst.compose_alt(wfst_sequence[i])
        print(input_sequence)
        result = composite_wfst.process(input_sequence)

        return result


class CompositeWFST:
    def __init__(self):
        self.wfsts = {}
    
    def add_wfst(self, key, wfst):
        self.wfsts[key] = wfst
    
    def compose(self, input_sequence):
        if not input_sequence:
            return []

        wfst = self.wfsts.get(graph_input_category.get(input_sequence[0]))
        composed_wfst = WFST(graph_input_category.get(input_sequence[0]))
        composed_wfst.set_start_state(0)
        for i in range(len(wfst.states) - 1):
            if input_sequence[0] in wfst.states[i]:
                for (next_state, output_symbol, weight) in wfst.states[i][input_sequence[0]]:
                    composed_wfst.add_transition(i, next_state, input_sequence[0], output_symbol, weight)
            elif '' in wfst.states[i]:
                for (next_state, output_symbol, weight) in wfst.states[i]['']:
                    composed_wfst.add_transition(i, next_state, '', output_symbol, weight)
                    break

        if not composed_wfst:
            return []

        for symbol in input_sequence[1:]:
            next_wfst = self.wfsts.get(graph_input_category.get(symbol))
            if next_wfst:
                composed_wfst = composed_wfst.compose(next_wfst, symbol)
            else:
                return []

        return composed_wfst
    
    def output(self, composite_wfst, input_sequence):
        wfst_sequence = []
        for itr in input_sequence:
            wfst = composite_wfst.compose(itr)
            wfst_sequence.append(wfst)

        composite_wfst = wfst_sequence[0]
        for i in range(1, len(wfst_sequence)):
            composite_wfst= composite_wfst.compose_alt(wfst_sequence[i])
        result = composite_wfst.process(input_sequence)

        return result


# Units WFST
units_wfst = WFST('units')
units_wfst.set_start_state(0)
units_wfst.add_final_state(1)
units_wfst.add_transition(0, 1, 'one', '1')
units_wfst.add_transition(0, 1, 'two', '2')
units_wfst.add_transition(0, 1, 'three', '3')
units_wfst.add_transition(0, 1, 'four', '4')
units_wfst.add_transition(0, 1, 'five', '5')
units_wfst.add_transition(0, 1, 'six', '6')
units_wfst.add_transition(0, 1, 'seven', '7')
units_wfst.add_transition(0, 1, 'eight', '8')
units_wfst.add_transition(0, 1, 'nine', '9')

# Tens WFST
tens_wfst = WFST('tens')
tens_wfst.set_start_state(0)
tens_wfst.add_final_state(2)
tens_wfst.add_transition(0, 1, 'ten', '1')
tens_wfst.add_transition(0, 1, 'twenty', '2')
tens_wfst.add_transition(0, 1, 'thirty', '3')
tens_wfst.add_transition(0, 1, 'forty', '4')
tens_wfst.add_transition(0, 1, 'fifty', '5')
tens_wfst.add_transition(0, 1, 'sixty', '6')
tens_wfst.add_transition(0, 1, 'seventy', '7')
tens_wfst.add_transition(0, 1, 'eighty', '8')
tens_wfst.add_transition(0, 1, 'ninety', '9')
tens_wfst.add_epsilon_transition(1, 2, '0', 1)

# Hundreds WFST
hundreds_wfst = WFST('hundreds')
hundreds_wfst.set_start_state(0)
hundreds_wfst.add_transition(0, 1, 'hundred', '0', 1)
hundreds_wfst.insert(1, 1, '0')

# Thousands WFST
thousands_wfst = WFST('thousands')
thousands_wfst.set_start_state(0)
thousands_wfst.add_transition(0, 1, 'thousand', '0', 1)
thousands_wfst.insert(1, 2, '0')

# Millions WFST
millions_wfst = WFST('millions')
millions_wfst.set_start_state(0)
millions_wfst.add_transition(0, 1, 'million', '0', 1)
millions_wfst.insert(1, 5, '0')

# Billions WFST
billions_wfst = WFST('billions')
billions_wfst.set_start_state(0)
billions_wfst.add_transition(0, 1, 'billion', '0', 1)
billions_wfst.insert(1, 8, '0')

# Trillions WFST
trillions_wfst = WFST('trillions')
trillions_wfst.set_start_state(0)
trillions_wfst.add_transition(0, 1, 'trillion', '0', 1)
trillions_wfst.insert(1, 11, '0')
# Composite WFST
composite_wfst = CompositeWFST()
composite_wfst.add_wfst('units', units_wfst)
composite_wfst.add_wfst('tens', tens_wfst)
composite_wfst.add_wfst('hundreds', hundreds_wfst)
composite_wfst.add_wfst('thousands', thousands_wfst)
composite_wfst.add_wfst('millions', millions_wfst)
composite_wfst.add_wfst('billions', billions_wfst)
composite_wfst.add_wfst('trillions', trillions_wfst)


# Load the English model
nlp = spacy.load("en_core_web_sm")

# Initialize the matcher
matcher = Matcher(nlp.vocab)

# Define patterns for numerical words (including multi-word patterns and Indian units)
patterns = [
    [{"LOWER": "one"}], [{"LOWER": "two"}], [{"LOWER": "three"}], [{"LOWER": "four"}],
    [{"LOWER": "five"}], [{"LOWER": "six"}], [{"LOWER": "seven"}], [{"LOWER": "eight"}],
    [{"LOWER": "nine"}], [{"LOWER": "ten"}], [{"LOWER": "eleven"}], [{"LOWER": "twelve"}],
    [{"LOWER": "thirteen"}], [{"LOWER": "fourteen"}], [{"LOWER": "fifteen"}], [{"LOWER": "sixteen"}],
    [{"LOWER": "seventeen"}], [{"LOWER": "eighteen"}], [{"LOWER": "nineteen"}], [{"LOWER": "twenty"}],
    [{"LOWER": "thirty"}], [{"LOWER": "forty"}], [{"LOWER": "fifty"}], [{"LOWER": "sixty"}],
    [{"LOWER": "seventy"}], [{"LOWER": "eighty"}], [{"LOWER": "ninety"}], [{"LOWER": "hundred"}],
    [{"LOWER": "thousand"}], [{"LOWER": "million"}], [{"LOWER": "billion"}],
    [{"LOWER": "lakh"}], [{"LOWER": "crore"}]
]

# Add patterns to the matcher
for pattern in patterns:
    matcher.add("NUMERIC_WORDS", [pattern])

# Define the custom NER function
def extract_numerical_data(text):
    doc = nlp(text)
    matches = matcher(doc)
    spans = [doc[start:end] for match_id, start, end in matches]
    
    # Sort spans by start position
    spans = sorted(spans, key=lambda span: span.start)
    
    # Merge contiguous spans
    merged_spans = []
    current_span = spans[0]
    for span in spans[1:]:
        if span.start <= current_span.end:
            current_span = doc[current_span.start:span.end]
        else:
            merged_spans.append(current_span)
            current_span = span
    merged_spans.append(current_span)
    
    return [(span.text, "NUM") for span in merged_spans]

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