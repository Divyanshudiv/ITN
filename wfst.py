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

    def process(self, input_sequence): 
        current_output = ''
        current_weight = 0
        next_states = []
        for state in self.states:
                values = list(self.states[state].values())
                print('values:', values)
                next_state = 0
                output_symbol = ''
                weight = 10**10
                for itr in values:
                    print(itr)
                    for (buffer_next_state, buffer_output_symbol, buffer_weight) in itr:
                        if weight >= buffer_weight:
                            next_state = buffer_next_state
                            output_symbol = buffer_output_symbol
                            weight = buffer_weight
                next_states.append((next_state, current_output + output_symbol, current_weight + weight))
                current_output += output_symbol
                current_weight += weight

        print(next_states)
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
                if input in other.states[s1]:
                    for (next_state, output_symbol, weight) in other.states[s1][input]:
                        result.add_transition(i, i + 1, input, output_symbol, weight)
                elif '' in other.states[s1]:
                    for (next_state, output_symbol, weight) in other.states[s1]['']:
                        result.add_transition(i, i + 1, '', output_symbol, weight)
                        break
            i += 1

        result.add_final_state(i - 1)
        print(result.states)
        return result

class CompositeWFST:
    def __init__(self):
        self.wfsts = {}
    
    def add_wfst(self, key, wfst):
        self.wfsts[key] = wfst
    
    def process(self, input_sequence):
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

        #composed_wfst = self.wfsts.get(graph_input_category.get(input_sequence[0]))
        if not composed_wfst:
            return []

        for symbol in input_sequence[1:]:
            next_wfst = self.wfsts.get(graph_input_category.get(symbol))
            if next_wfst:
                composed_wfst = composed_wfst.compose(next_wfst, symbol)
            else:
                return []

        return composed_wfst.process(input_sequence)

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
tens_wfst.add_epsilon_transition(1, 2, '0', 0.1)

# Hundreds WFST
hundreds_wfst = WFST('hundreds')
hundreds_wfst.set_start_state(0)
hundreds_wfst.add_final_state(2)
hundreds_wfst.add_transition(0, 1, 'hundred', '0', 0.1)
hundreds_wfst.add_epsilon_transition(1, 2, '0', 0.1)

# Thousands WFST
thousands_wfst = WFST('thousands')
thousands_wfst.set_start_state(0)
thousands_wfst.add_final_state(3)
thousands_wfst.add_transition(0, 1, 'thousand', '0', 0.1)
thousands_wfst.add_epsilon_transition(1, 2, '0', 0.1)
thousands_wfst.add_epsilon_transition(2, 3, '0', 0.1)

# Millions WFST
millions_wfst = WFST('millions')
millions_wfst.set_start_state(0)
millions_wfst.add_final_state(6)
millions_wfst.add_transition(0, 1, 'million', '0', 0.1)
millions_wfst.add_epsilon_transition(1, 2, '0', 0.1)
millions_wfst.add_epsilon_transition(2, 3, '0', 0.1)
millions_wfst.add_epsilon_transition(3, 4, '0', 0.1)
millions_wfst.add_epsilon_transition(4, 5, '0', 0.1)
millions_wfst.add_epsilon_transition(5, 6, '0', 0.1)

# Billions WFST
billions_wfst = WFST('billions')
billions_wfst.set_start_state(0)
billions_wfst.add_final_state(9)
billions_wfst.add_transition(0, 1, 'billion', '0', 0.1)
billions_wfst.add_epsilon_transition(1, 2, '0', 0.1)
billions_wfst.add_epsilon_transition(2, 3, '0', 0.1)
billions_wfst.add_epsilon_transition(3, 4, '0', 0.1)
billions_wfst.add_epsilon_transition(4, 5, '0', 0.1)
billions_wfst.add_epsilon_transition(5, 6, '0', 0.1)
billions_wfst.add_epsilon_transition(6, 7, '0', 0.1)
billions_wfst.add_epsilon_transition(7, 8, '0', 0.1)
billions_wfst.add_epsilon_transition(8, 9, '0', 0.1)

# Trillions WFST
trillions_wfst = WFST('trillions')
trillions_wfst.set_start_state(0)
trillions_wfst.add_final_state(12)
trillions_wfst.add_transition(0, 1, 'trillion', '0', 0.1)
trillions_wfst.add_epsilon_transition(1, 2, '0', 0.1)
trillions_wfst.add_epsilon_transition(2, 3, '0', 0.1)
trillions_wfst.add_epsilon_transition(3, 4, '0', 0.1)
trillions_wfst.add_epsilon_transition(4, 5, '0', 0.1)
trillions_wfst.add_epsilon_transition(5, 6, '0', 0.1)
trillions_wfst.add_epsilon_transition(6, 7, '0', 0.1)
trillions_wfst.add_epsilon_transition(7, 8, '0', 0.1)
trillions_wfst.add_epsilon_transition(8, 9, '0', 0.1)
trillions_wfst.add_epsilon_transition(9, 10, '0', 0.1)
trillions_wfst.add_epsilon_transition(10, 11, '0', 0.1)
trillions_wfst.add_epsilon_transition(11, 12, '0', 0.1)

# Composite WFST
composite_wfst = CompositeWFST()
composite_wfst.add_wfst('units', units_wfst)
composite_wfst.add_wfst('tens', tens_wfst)
composite_wfst.add_wfst('hundreds', hundreds_wfst)
composite_wfst.add_wfst('thousands', thousands_wfst)
composite_wfst.add_wfst('millions', millions_wfst)
composite_wfst.add_wfst('billions', billions_wfst)
composite_wfst.add_wfst('trillions', trillions_wfst)

import nltk
from nltk import word_tokenize, pos_tag
from typing import List, Tuple

# Download necessary NLTK data (run this once)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def tokenize_and_tag(sentence: str) -> List[Tuple[str, str]]:
    tokens = word_tokenize(sentence.lower())
    return pos_tag(tokens)

def identify_number_phrases(tagged_tokens: List[Tuple[str, str]]) -> List[Tuple[int, int]]:
    number_words = set([
        'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
        'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen',
        'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety',
        'hundred', 'thousand', 'million', 'billion', 'trillion'
    ])
    
    phrases = []
    start = -1
    for i, (token, pos) in enumerate(tagged_tokens):
        if token in number_words or pos == 'CD':  # CD is the POS tag for cardinal numbers
            if start == -1:
                start = i
        elif start != -1:
            phrases.append((start, i))
            start = -1
    
    if start != -1:
        phrases.append((start, len(tagged_tokens)))
    
    return phrases

def process_sentence(sentence: str, composite_wfst: CompositeWFST) -> str:
    tagged_tokens = tokenize_and_tag(sentence)
    number_phrases = identify_number_phrases(tagged_tokens)
    
    tokens = [token for token, _ in tagged_tokens]
    
    for start, end in reversed(number_phrases):
        number_words = tokens[start:end]
        normalized = composite_wfst.process(number_words)
        if normalized:
            tokens[start:end] = [normalized[1]]  # Replace with normalized number
    
    return ' '.join(tokens)

# Example usage
sentence = "The shoes cost three hundred dollars and fifty cents"
result = process_sentence(sentence, composite_wfst)
print(result)