import sys


class NFA:
    def __init__(self, NFAlist):
        self.Q = {}
        for x in range(1, NFAlist['Q'] + 1):
            list = []
            list.append(x)
            self.Q[x] = State(list, NFAlist['T'], NFAlist['F'])
        self.E = NFAlist['E']
        self.currentState = []
        self.currentState.append(NFAlist['q0'])
        self.F = NFAlist['F']

class DFAState:
    def __init__(self, states, x, accepts):
        self.states = states
        self.stateid = x
        # the transitions will have transitions to stateid keyed by alphabet
        self.transitions = {}
        self.accepts = False
        for z in states:
            for y in accepts:
                if int(z) is int(y):
                    self.accepts = True

    def settransition(self, symbol, nextstate):
        self.transitions[symbol] = nextstate


class State:
    def __init__(self, state, transitions, accepts):
        self.state = []
        for x in state:
            self.state.append(int(x))
        self.accepts = False
        for x in accepts:
            for y in self.state:
                if int(x) is int(y):
                    self.accepts = True
        self.transitions = {}
        for x in transitions:
            for y in self.state:
                if int(x[0]) is int(y):
                    self.transitions[x[1]] = []
        for x in transitions:
            for y in self.state:
                if int(x[0]) is int(y):
                    self.transitions[x[1]].append(x[2])


def readfile(filename):
    with open(filename, 'r') as x:
        numstates = int(x.readline().rstrip('\n'))
        alphabet = list(x.readline().rstrip('\n'))

        stateTransitions = []
        line = x.readline().rstrip('\n')

        while (line.__len__() != 0):
            splitted = line.split('\'')
            hold = []
            for i in splitted:
                hold.append(i.replace(' ', ''))
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
        x.close()
        return returnlist



def settransition(id, states, nfa):

    curr = states[id] #curr is the DFA state we are setting transitions for

    #find the NFA states we can epsilon transition to, for each state in curr
    epsilons = []
    hold = []
    for x in curr.states:
        try:
            for z in nfa.Q[x].transitions['e']:
                epsilons.append(int(z))
                hold.append(int(z))
        except:
            pass

    print epsilons
    # check if there are more epsilons
    therearemoreepsilons = True

    newe = []
    while therearemoreepsilons is True:
        counter = 0
        for y in epsilons:

            try:
                for z in nfa.Q[int(y)].transitions['e']:
                    hold.append(int(z))
                    newe.append(int(z))

            except:
                pass
                counter = counter + 1

        if counter is len(epsilons):
            therearemoreepsilons = False

        epsilons = newe

    for y in curr.states:
        hold.append(int(y))

    print hold

    #WE CHECK THE TRANSITIONS FOR ALL SYMBOLS
    trans = {}
    for symbol in nfa.E:
        trans[symbol] = []

    for symbol in nfa.E:
        for state in hold:
            try:
                for z in nfa.Q[int(state)].transitions[symbol]:
                    trans[symbol].append(z)
            except:
                pass
    for symbol in nfa.E:
        if len(trans[symbol]) is 0:
            trans[symbol].append(int(0))


    #make some DFA state objects
    newstates = {}

    for symbol in nfa.E:
        for x in trans[symbol]:
            counterpart = 0
            for y in states:
                for z in states[y].states:
                    if int(x) is int(z):
                        counterpart = counterpart + 1
            if len(trans[symbol]) is counterpart:
                id = y.stateid
            else:
                id = len(states) + 1

            tmp = DFAState(trans[symbol], id, nfa.F)
            newstates[id] = tmp

            curr.settransition(symbol, id)

    for x in newstates:
        print x, newstates[x].states
    return newstates


def main(filename):
    nfa = NFA(readfile(filename))

    generatedstates = {}
    currentstate = DFAState(nfa.currentState, 1, nfa.F)
    generatedstates[1] = currentstate

    states = settransition(1, generatedstates, nfa)
    # Here, I could run a check that all states in generatedstates have transition


    notransition = checkalltransitions(states, nfa)


def checkalltransitions(statelist, nfa):
    for x in statelist:
        for y in nfa.E:
            try:
                statelist[x].transitions[y]
            except:
                return x

    return -1

if __name__ == "__main__":
    main(sys.argv[1])