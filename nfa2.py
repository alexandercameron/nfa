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



def findtransitions(stateid, stateslist, nfa ):

    sl = stateslist
    curr = stateslist[stateid]
    e = True
    epsilonT = {}
    for x in nfa.E:
        epsilonT[x] = []

    s= curr.states

    hold = []
    statesfromepsilon = []
    while e is True:
        for x in s:
            try:
                for z in nfa.Q[int(x)].transitions['e']:
                    statesfromepsilon.append(z)
            except:
                pass

        e = False

        print statesfromepsilon

        if len(statesfromepsilon) is not 0:
            for y in statesfromepsilon:
                for x in nfa.Q[int(y)].transitions:
                    if x is 'e':
                        e  = True
                        hold.append(y)
            s = statesfromepsilon
        '''
        if len(statesfromepsilon) is not 0:
            for y in statesfromepsilon:
                for x in nfa.Q[int(y)].transitions:
                    if x is 'e':
                        e = True
                        hold.append(statesfromepsilon)

            s = statesfromepsilon
            '''

    for x in hold:
        print "hold", x
        statesfromepsilon = statesfromepsilon + x


    if statesfromepsilon is not None:
        for y in statesfromepsilon:
            for x in nfa.Q[int(y)].transitions:
                if x is 'e':
                    pass
                else:
                    for l in nfa.Q[int(y)].transitions[x]:
                        epsilonT[x].append(l)

    nextstates = {}
    for x in nfa.E:
        for y in curr.states:
            nextstates[x] = []
            for k in epsilonT[x]:
                nextstates[x].append(k)
            try:
                for a in nfa.Q[int(y)].transitions[x]:
                    print y, x, a
                    nextstates[x].append(int(a))
            except:
                nextstates[x].append(0)

    for y in nfa.E:
        if len(nextstates[y]) is 0:
            nextstates[y].append(0)


    list = []
    for x in range(1, sl.__len__() + 1):
        list.append(sl[x])

    newstates = {}

    for symbol in nfa.E:
        # check if the new state is going to be a duplicate
        id = len(list) + 1
        # start by checking length of new state with prev states
        duplicate = 0
        for z in list:
            try:
                if len(z.states) is len(nextstates[symbol]):
                    # check if each element in x has counterpart in y
                    counterpart = 0
                    for x in nextstates[symbol]:
                        for y in z.states:
                            if int(x) is int(y):
                                counterpart = counterpart + 1
                    if counterpart is len(z.states):
                        duplicate = 1
                        id = z.stateid

                else:
                    pass
            except:
                pass

        curr.settransition(symbol, id)
        if duplicate is 0:
            tmp = DFAState(nextstates[symbol], id, nfa.F)
            list.append(tmp)
            newstates[id] = tmp
            id = id + 1

    for a in stateslist:
        newstates[a] = stateslist[a]
    newstates[stateid] = curr
    return newstates


def main(filename):
    nfa = NFA(readfile(filename))

    generatedstates = {}
    currentstate = DFAState(nfa.currentState, 1, nfa.F)
    generatedstates[1] = currentstate

    states = findtransitions(1, generatedstates, nfa)
    # Here, I could run a check that all states in generatedstates have transition


    notransition = checkalltransitions(states, nfa)
    while notransition is not -1:
        states = findtransitions(notransition, states, nfa)
        notransition = checkalltransitions(states, nfa)

    for x in states:
        for y in nfa.E:
            print states[x].states, x, y, states[states[x].transitions[y]].states


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