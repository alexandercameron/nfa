import sys

class NFA:

    def __init__(self, NFAlist):
        self.Q = {}
        for x in range(1,NFAlist['Q'] + 1):
            list = []
            list.append(x)
            self.Q[x] = State(list, NFAlist['T'], NFAlist['F'])
        self.E = NFAlist['E']
        self.currentState = []
        self.currentState.append(NFAlist['q0'])
        self.F = NFAlist['F']

    def convertToDFA(self):


        count = 1
        currstate = DFAState(self.currentState, count, self.F)
        count = count + 1

        generatedstates = []

        generatedstates.append(currstate)

        condition = True
        while condition is True:

            e = True


            epsilonT = {}  # will be keyed with letter
            for x in self.E:  # x is each letter
                epsilonT[x] = [] #makes each hold a list

            #looks for states we can epsilon transition to from current states, saves in sfe
            s = currstate.states
            hold = []
            while e is True:
                for x in s:
                    statesfromepsilon = self.Q[int(x)].transitions['e']
                e = False
                for y in statesfromepsilon:
                    for x in self.Q[int(y)].transitions:
                        if x is 'e':
                            e = True
                            hold.append(statesfromepsilon)

                s = statesfromepsilon

            for x in hold:
                statesfromepsilon = statesfromepsilon + x


            for y in statesfromepsilon:
                for x in self.Q[int(y)].transitions:
                    if x is 'e':
                        pass
                    else:
                        epsilonT[x] = self.Q[int(y)].transitions[x] + epsilonT[x]





            nextstates = {}
            for x in self.E:
                for y in currstate.states:
                    nextstates[x] = []
                    try:
                        nextstates[x] = self.Q[int(y)].transitions[x] + epsilonT[x]
                    except:
                        nextstates[x] = epsilonT[x]


            #for each symbol in the alphabet
            duplicate = 0
            for symbol in self.E:
                id = count
                #check if the new state is going to be a duplicate

                #start by checking length of new state with prev states
                duplicate = 0
                for state in generatedstates:
                    if len(state.states) is len(nextstates[symbol]):
                        #check if each element in x has counterpart in y
                        counterpart = 0
                        for x in nextstates[symbol]:
                            for y in state.states:
                                if int(x) is int(y):
                                    counterpart = counterpart + 1
                        if counterpart is len(state.states):
                            duplicate = 1
                            id = state.stateid

                    else:
                        pass






                tmp = DFAState(nextstates[symbol], id, self.F)
                currstate.settransition(symbol, id)
                if duplicate is 0:
                    count = count + 1
                    generatedstates.append(tmp)

            for z in generatedstates:
                print z.stateid
                print z.states

            if duplicate is 0:
                condition = False







class DFAState:
    def __init__(self, states, x, accepts):
        self.states = states
        self.stateid = x
        #the transitions will have transitions to stateid keyed by alphabet
        self.transitions = {}
        self.accepts = False
        for x in states:
            for y in accepts:
                if int(x) is int(y):
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
    nfa.convertToDFA()


if __name__ == "__main__":
    main(sys.argv[1])