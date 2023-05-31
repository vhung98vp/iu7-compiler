class CFG:
  def __init__(self, cfg_file=None):
    if cfg_file:
      self.build_from_file(cfg_file)
    else:
      self.terminal = set()
      self.non_terminal = set()
      self.production = dict()
      self.start = str()

  def build_from_file(self, cfg_file):
    with open(cfg_file, 'r') as f:
      lines = f.readlines()

    n_non_terminal = int(lines[0])
    self.non_terminal = set(lines[1].rstrip('\n').split(' '))
    assert len(self.non_terminal) == n_non_terminal

    n_terminal = int(lines[2])
    self.terminal = set(lines[3].rstrip('\n').split(' '))
    assert len(self.terminal) == n_terminal

    n_production = int(lines[4])
    self.production = dict()
    for i in range(n_production):
      rule = lines[i + 5].rstrip('\n').replace(' ', '').split('->')
      options = rule[1].split('|')

      if rule[0] in self.production:
        self.production[rule[0]] = self.production[rule[0]].union(options)
      else:
        self.production[rule[0]] = set(options)

    self.start = lines[-1].rstrip('\n')[0]

  def update_production(self, non_terminal, rule, new_rules):
    self.production[non_terminal].discard(rule)
    self.production[non_terminal] = self.production[non_terminal].union(new_rules)

  def export_to_file(self, file):
    with open(file, 'w', encoding='utf-8') as f:
      f.write(f'{len(self.non_terminal)}\n')
      f.write(' '.join(self.non_terminal) + '\n')
      f.write(f'{len(self.terminal)}\n')
      f.write(' '.join(self.terminal) + '\n')
      f.write(f'{len(self.production)}\n')
      for (key, vals) in self.production.items():
        f.write(f'{key} -> {" | ".join(vals)}\n')
      f.write(self.start)


def eliminate_left_recursion(cfg_file):
  cfg = CFG(cfg_file)
  grammar = CFG()
  grammar.terminal = cfg.terminal
  grammar.non_terminal = cfg.non_terminal
  grammar.start = cfg.start

  non_terminals = list(cfg.non_terminal)
  for i in range(len(non_terminals)):
    non_terminal = non_terminals[i]
    rules = cfg.production[non_terminal]

    # 1. Replace left non terminal
    for j in range(i):
      prev_non_terminal = non_terminals[j]
      prev_rules = cfg.production[prev_non_terminal]

      for rule in rules.copy():
        if rule.startswith(prev_non_terminal):
          new_rules = set([prev_rule + rule[len(prev_non_terminal):]
                              for prev_rule in prev_rules])

          cfg.update_production(non_terminal, rule, new_rules)

    # 2. Eliminate immediate left recursion among productions
    non_terminal = non_terminals[i]
    rules = cfg.production[non_terminal]

    if any(rule.startswith(non_terminal) for rule in rules):  # Left-recursion
      alpha = set([rule for rule in rules if rule.startswith(non_terminal)])
      beta = rules.difference(alpha)

      new_symbol = non_terminal + "'"

      if beta:
        beta_rules = set([c + new_symbol for c in beta])
      else:
        beta_rules = set([new_symbol])

      alpha_rules = set([c[len(non_terminal):] + new_symbol for c in alpha])
      alpha_rules.add('ε')

      grammar.non_terminal.add(new_symbol)
      grammar.production.update({non_terminal: beta_rules})
      grammar.production.update({new_symbol: alpha_rules})
      cfg.production[non_terminal] = beta_rules
    else:
      grammar.production.update({non_terminal: rules})

  return grammar

def remove_inaccessible(cfg_file):

  def get_Vi(cfg):
    V0 = set(cfg.start)

    while True:
      Vi = set()

      for X in cfg.non_terminal.union(cfg.terminal):
        for A in V0:
          if A not in cfg.production.keys(): continue
          if any(X in val for val in cfg.production[A]):
            Vi = Vi.union(X)
            break

      Vi = Vi.union(V0)
      if Vi == V0:
        break
      V0 = Vi
    return Vi

  cfg = CFG(cfg_file)

  Vi = get_Vi(cfg)
  grammar = CFG()
  grammar.non_terminal = cfg.non_terminal.intersection(Vi)
  grammar.terminal = cfg.terminal.intersection(Vi)
  for (key, vals) in cfg.production.items():
    if key not in Vi: continue
    new_vals = set([val for val in vals if val in Vi])
    grammar.production.update({key: new_vals})
  grammar.start = cfg.start

  return grammar


