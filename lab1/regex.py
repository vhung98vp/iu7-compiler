class GrammarToRegex:
  """class for building regex from grammar"""

  def __init__(self, grammar):
    self.epsilon = 'e'
    self.grammar = grammar
    self.rules = dict()
    self.buildRules()

  def buildRules(self):
    grammar_str = self.grammar.split('\n')
    for rule in grammar_str:
      rule = rule.split(' -> ')
      self.rules[rule[0]] = rule[1].split(' | ')

  def getEquations(self):
    eqs = [' = '.join([k, ' + '.join(v)]) for k, v in self.rules.items()]
    return eqs

  def getRegexSystem(self):
    keys = list(self.rules.keys())
    n = len(keys)
  
    def get_star(key, vals):
      has, not_has = [], []
      # Find key in vals
      for val in vals:
        if key not in val:
          not_has.append(val)
        else:
          has.append(val[:-1])

      res = []
      if len(has) > 0:
        has_str = f'({"+".join(has)})*' if len(has) > 1 else f'{has[0]}*'
        if len(not_has) > 0:
          # Add star to vals
          for nh in not_has:
            res.append(has_str+nh) if nh != self.epsilon else res.append(has_str)  
        else:
          res = [has_str]
      else:
        res = [f'{"+".join(not_has)}']
      return res
      
    def replace_key(key_f, val_f, key_t, val_t):
      #print(key_f, val_f, '->' , key_t, val_t)
      res = []
      for s in val_t:
        if key_f in s:
          res += [s.replace(key_f, vf) for vf in val_f]
        else:
          res.append(s)
      return res

    def merge_left(vals):
      left = vals[0]
      for sol in vals[1:]:
        if len(left) > len(sol):
          left = left[:len(sol)]
        for j in range(len(left)):
          if sol[j] != left[j]:
            left = left[:j]
            break
      res = []
      for sol in vals:
        res.append(sol[len(left):] if sol != left else self.epsilon)
      return left + f'({ "+".join(res) })'

    solutions = self.rules.copy()

    for i in range(n):
      kf = keys[i]
      solutions[kf] = get_star(kf, solutions[kf])
      for j in range(i+1, n):
        kt = keys[j]
        solutions[kt] = replace_key(kf, solutions[kf], kt, solutions[kt])
    
    #print('\nEnd of replace:', solutions)

    for i in range(n-1, -1, -1):
      kf = keys[i]
      for j in range(i-1, -1, -1):
        kt = keys[j]
        solutions[kt] = replace_key(kf, solutions[kf], kt, solutions[kt])
      
      solutions[kf] = merge_left(solutions[kf]) if len(solutions[kf]) > 1 else solutions[kf][0]

    return solutions
