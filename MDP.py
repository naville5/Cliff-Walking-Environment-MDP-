import csv
import sys

Trans = {}
re = {}


if len(sys.argv)>1:
    gamma = float(sys.argv[1])
else:
    gamma = 1

if len(sys.argv)>2:
    epsilon = float(sys.argv[2])
else:
    epsilon = 0.001

def read_file():
    with open('Trans.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] in Trans:
                if row[1] in Trans[row[0]]:
                    Trans[row[0]][row[1]].append((float(row[3]), row[2]))
                else:
                    Trans[row[0]][row[1]] = [(float(row[3]), row[2])]
            else:
                Trans[row[0]] = {row[1]:[(float(row[3]),row[2])]}

   
    with open('res.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            re[row[0]] = float(row[1]) if row[1] != 'None' else None

read_file()

class MarkovDecisionProcess:

  
    def _init_(self, transition={}, re={}, gamma=.9):
   
        self.states = transition.keys()

        self.transition = transition
       
        self.re = re

        self.gamma = gamma

    def R(self, state):
        
        return self.re[state]

    def actions(self, state):
      
        return self.transition[state].keys()

    def T(self, state, action):
      
        return self.transition[state][action]


mdp = MarkovDecisionProcess(transition=Trans, re=re)

def value_iteration():
  
    states = mdp.states
    actions = mdp.actions
    T = mdp.T
    R = mdp.R


    V1 = {s: 0 for s in states}
    while True:
        V = V1.copy()
        delta = 0
        for s in states:

            V1[s] = R(s) + gamma * max([ sum([p * V[s1] for (p, s1) in T(s, a)]) for a in actions(s)])
           
            delta = max(delta, abs(V1[s] - V[s]))

        if delta < epsilon * (1 - gamma) / gamma:
            return V


def best_policy(V):
   
    states = mdp.states
    actions = mdp.actions
    pi = {}
    for s in states:
        pi[s] = max(actions(s), key=lambda a: expected_utility(a, s, V))
    return pi


def expected_utility(a, s, V):
    
    T = mdp.T
    return sum([p * V[s1] for (p, s1) in mdp.T(s, a)])



V = value_iteration()
print ('State - Value')
for s in V:
    print (s, ' - ' , V[s])
pi = best_policy(V)
print ('\nOptimal policy is \nState - Action')
for s in pi:
    print (s, ' - ' , pi[s])