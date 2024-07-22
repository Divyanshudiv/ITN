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
        i = 0
        next_states = []
        for j in range(len(self.states) - 1):
            if i < len(input_sequence):
                symbol = input_sequence[i]
            else:
                symbol = None
            if symbol and symbol in self.states[j]:
                for (next_state, output_symbol, weight) in self.states[j][symbol]:
                    next_states.append((next_state, current_output + output_symbol, current_weight + weight))
                    current_output += output_symbol
                    current_weight += weight
                    i += 1
                    break
            elif '' in self.states[j]:
                for (next_state, output_symbol, weight) in self.states[j]['']:
                    next_states.append((next_state, current_output + output_symbol, current_weight + weight))
                    current_output += output_symbol
                    current_weight += weight
                    break
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

composite_wfst = CompositeWFST()
composite_wfst.add_wfst('units', units_wfst)
composite_wfst.add_wfst('tens', tens_wfst)
composite_wfst.add_wfst('hundreds', hundreds_wfst)

input_sequence1 = ['twenty', 'two']
result1 = composite_wfst.process(input_sequence1)

#print(result1[1])