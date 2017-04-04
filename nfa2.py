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
    newstates = states

    #find the NFA states we can epsilon transition to, for each state in curr
    epsilons = []
    hold = []


    for x in curr.states:
        try:
            for z in nfa.Q[int(x)].transitions['e']:
                epsilons.append(int(z))
                hold.append(int(z))
        except:
            pass

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
            trans[symbol].append('0')


    #make some DFA state objects


    newstates[curr.stateid] = curr
    newid = 0
    '''
    this is where we check for duplicates
    
    trans is a dictionary that holds a list of states keyed to a symbol
    for each symbol, we need to check if the list in trans keyed to that symbol is the same as a saved state
    to do this:
        look at each saved state, s
        check if element in trans is equal to element in s
            if it is, add to counterpart
        if counterpart is the length of the state list (ie, it is a dup)
            set transition to the id of s
        else   
            make a new state with id of len(newstates + 1)
    '''

    for symbol in nfa.E:
        dup = 0
        for s in newstates:
            counterpart = 0
            #we have to check if trans[symbol] == newstates[s].states
            if len(trans[symbol]) is len(newstates[s].states):
                for onestate in trans[symbol]:
                    for correspondingstate in newstates[s].states:
                        if int(onestate) is int(correspondingstate):
                            counterpart = counterpart + 1

                if counterpart is len(trans[symbol]):
                    newid = s
                    dup = 1
        if dup is 0:
            newid = len(newstates) + 1
            tmp = DFAState(trans[symbol], newid, nfa.F)
            newstates[newid] = tmp

        curr.settransition(symbol, newid)

    return newstates

def checkalltransitions(statelist, nfa):
    for x in statelist:
        for y in nfa.E:
            try:
                statelist[x].transitions[y]
            except:
                return x

    return -1

def main(filename, outname):
    nfa = NFA(readfile(filename))

    generatedstates = {}
    currentstate = DFAState(nfa.currentState, 1, nfa.F)
    generatedstates[1] = currentstate


    states = settransition(1, generatedstates, nfa)

    # Here, I could run a check that all states in generatedstates have transition

    notransition = checkalltransitions(states, nfa)
    while notransition is not -1:
        states = settransition(notransition, states, nfa)
        notransition = checkalltransitions(states, nfa)

    f = open(outname, "a")
    f.write(str(len(states)))
    f.write("\n")
    for x in nfa.E:
        f.write(x)
    f.write("\n")
    for x in states:
        for symbol in nfa.E:
            f.write(str(x))
            f.write(" '")
            f.write(symbol)
            f.write("' ")
            f.write(str(states[x].transitions[symbol]))
            f.write("\n")
    f.write('1')
    f.write("\n")
    for x in states:
        if states[x].accepts is True:
            f.write(str(x))
            f.write(" ")
    f.write("\n")
    f.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])