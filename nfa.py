import sys

class NFA:
    def __init__(self, NFAlist):
        self.Q = {}
        for x in range(1,NFAlist['Q'] + 1):
            self.Q[x] = State(x, NFAlist['T'], NFAlist['F'])
        self.E = NFAlist['E']
        self.currentState = NFAlist['q0']

class State:
    def __init__(self, state, transitions, accepts):
        self.state = int(state)
        self.accepts = False
        for x in accepts:
            if int(x) is int(state):
                self.accepts = True
        self.transitions = {}
        for x in transitions:
            if int(x[0]) is int(state):
                self.transitions[x[1]] = x[2]

def readfile(filename):
    with open(filename,'r') as x:
        numstates = int(x.readline().rstrip('\n'))
        alphabet = list(x.readline().rstrip('\n'))

        stateTransitions = []
        line = x.readline().rstrip('\n')

        while(line.__len__() != 0):
            splitted = line.split('\'')
            hold = []
            for i in splitted:
                hold.append(i.replace(' ',''))
            stateTransitions.append(hold)
            line = x.readline().rstrip('\n')

        line = x.readline().rstrip('\n')
        startState = int(line)

        # Reads in the accept states, as a list
        acceptStates = x.readline().rstrip('\n').split(' ')
        for a in acceptStates:
            try:
                a = int(a)
            except:
                acceptStates.remove(a)

        returnlist = {}
        returnlist['Q'] = numstates
        returnlist['E'] = alphabet
        returnlist['T'] = stateTransitions
        returnlist['q0'] = startState
        returnlist['F'] = acceptStates
        return returnlist

def main(filename):
    nfa = NFA(readfile(filename))
    for x in nfa.Q:
        print nfa.Q[x].transitions










if __name__ == "__main__":
    main(sys.argv[1])