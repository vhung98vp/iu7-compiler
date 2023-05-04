import graphviz

class Automata:
    """class to represent an Automata"""

    def __init__(self, language = set(['0', '1'])):
        self.states = set()
        self.start_state = None
        self.final_states = []
        self.transitions = dict()
        self.language = language

    @staticmethod
    def epsilon():
        return ":e:"

    def set_start_state(self, state):
        self.start_state = state
        self.states.add(state)

    def add_final_states(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.final_states:
                self.final_states.append(s)

    def add_transition(self, from_state, to_state, key):
        if isinstance(key, str):
            key = set([key])
        self.states.add(from_state)
        self.states.add(to_state)
        if from_state in self.transitions:
            if to_state in self.transitions[from_state]:
                self.transitions[from_state][to_state] = self.transitions[from_state][to_state].union(key)
            else:
                self.transitions[from_state][to_state] = key
        else:
            self.transitions[from_state] = {to_state : key}

    def add_transition_dict(self, transitions):
        for from_state, to_states in transitions.items():
            for state in to_states:
                self.add_transition(from_state, state, to_states[state])

    def get_transitions(self, state, key):
        if isinstance(state, int):
            state = [state]
        states = set()
        for st in state:
            if st in self.transitions:
                for to_st in self.transitions[st]:
                    if key in self.transitions[st][to_st]:
                        states.add(to_st)
        return states

    def get_epsilon_close(self, find_state):
        all_states = set()
        states = set([find_state])
        while len(states)!= 0:
            state = states.pop()
            all_states.add(state)
            if state in self.transitions:
                for to_st in self.transitions[state]:
                    if Automata.epsilon() in self.transitions[state][to_st] and to_st not in all_states:
                        states.add(to_st)
        return all_states

    def display(self):
        print("states:", self.states)
        print("start state: ", self.start_state)
        print("final states:", self.final_states)
        print("transitions:")
        for from_state, to_states in self.transitions.items():
            for state in to_states:
                for char in to_states[state]:
                    print ("  ",from_state, "->", state, "on '"+char+"'")
            print

    def rebuild_from_number(self, start_num):
        translations = {}
        for i in list(self.states):
            translations[i] = start_num
            start_num += 1
        rebuild = Automata(self.language)
        rebuild.set_start_state(translations[self.start_state])
        rebuild.add_final_states(translations[self.final_states[0]])
        for from_state, to_states in self.transitions.items():
            for state in to_states:
                rebuild.add_transition(translations[from_state], translations[state], to_states[state])
        return [rebuild, start_num]

    def drawGraph(self, path):
        dot = graphviz.Digraph(graph_attr={'rankdir': 'LR', 'root': 's1'})

        if self.states:
            dot.node('start', '', shape='point')
            dot.edge('start', f's{self.start_state}')

        for state in self.states:
            if state in self.final_states:
                dot.node(f's{state}', f's{state}', shape='doublecircle')
            else:
                dot.node(f's{state}', f's{state}', shape='circle')
        
        for from_state, to_states in self.transitions.items():
            for to_state in to_states:
                for label in to_states[to_state]:
                    dot.edge(f's{from_state}', f's{to_state}', label)    

        dot.render(path)

class BuildAutomata:
    """class for building e-nfa basic structures"""

    @staticmethod
    def basic_struct(inp):
        state1 = 1
        state2 = 2
        basic = Automata()
        basic.set_start_state(state1)
        basic.add_final_states(state2)
        basic.add_transition(state1, state2, inp)
        return basic

    @staticmethod
    def plus_struct(a, b):
        [a, m1] = a.rebuild_from_number(2)
        [b, m2] = b.rebuild_from_number(m1)
        state1 = 1
        state2 = m2
        plus = Automata()
        plus.set_start_state(state1)
        plus.add_final_states(state2)
        plus.add_transition(plus.start_state, a.start_state, Automata.epsilon())
        plus.add_transition(plus.start_state, b.start_state, Automata.epsilon())
        plus.add_transition(a.final_states[0], plus.final_states[0], Automata.epsilon())
        plus.add_transition(b.final_states[0], plus.final_states[0], Automata.epsilon())
        plus.add_transition_dict(a.transitions)
        plus.add_transition_dict(b.transitions)
        return plus

    @staticmethod
    def dot_struct(a, b):
        [a, m1] = a.rebuild_from_number(1)
        [b, m2] = b.rebuild_from_number(m1)
        state1 = 1
        state2 = m2-1
        dot = Automata()
        dot.set_start_state(state1)
        dot.add_final_states(state2)
        dot.add_transition(a.final_states[0], b.start_state, Automata.epsilon())
        dot.add_transition_dict(a.transitions)
        dot.add_transition_dict(b.transitions)
        return dot

    @staticmethod
    def star_struct(a):
        [a, m1] = a.rebuild_from_number(2)
        state1 = 1
        state2 = m1
        star = Automata()
        star.set_start_state(state1)
        star.add_final_states(state2)
        star.add_transition(star.start_state, a.start_state, Automata.epsilon())
        star.add_transition(star.start_state, star.final_states[0], Automata.epsilon())
        star.add_transition(a.final_states[0], star.final_states[0], Automata.epsilon())
        star.add_transition(a.final_states[0], a.start_state, Automata.epsilon())
        star.add_transition_dict(a.transitions)
        return star