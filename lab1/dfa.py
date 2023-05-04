from automata import Automata

class NFAToDFA:
  """class for building dfa from e-nfa"""

  def __init__(self, nfa):
    self.buildDFA(nfa)

  def getDFA(self):
    return self.dfa

  def buildDFA(self, nfa):
    all_states = dict()
    e_close = dict()
    count = 1
    state1 = nfa.get_epsilon_close(nfa.start_state)
    e_close[nfa.start_state] = state1
    dfa = Automata(nfa.language)
    dfa.set_start_state(count)
    states = [[state1, count]]
    all_states[count] = state1
    count +=  1
    while len(states) != 0:
      [state, from_index] = states.pop()
      for char in dfa.language:
        dst_states = nfa.get_transitions(state, char)
        for s in list(dst_states)[:]:
          if s not in e_close:
            e_close[s] = nfa.get_epsilon_close(s)
          dst_states = dst_states.union(e_close[s])
        if len(dst_states) != 0:
          if dst_states not in all_states.values():
            states.append([dst_states, count])
            all_states[count] = dst_states
            to_index = count
            count +=  1
          else:
            to_index = [k for k, v in all_states.items() if v == dst_states][0]
          dfa.add_transition(from_index, to_index, char)
    for value, state in all_states.items():
      if nfa.final_states[0] in state:
        dfa.add_final_states(value)
    self.dfa = dfa