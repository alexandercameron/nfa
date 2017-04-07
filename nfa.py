'''
All tabs have been converted to spaces. 
'''

'''
A program that reads in an NFA txt file, converts it 
into its equivalent DFA, and writes the DFA to file. 

Authors: Alex Cameron, Eli Grady, Erick Perez
USD, COMP370, Dr. Glick, Spring 2017
'''


import sys

'''
A class that defines an NFA.

@param NFAdict, a dictionary generated when the NFA file is read in

@attribute Q, a dictionary of State objects
@attribute E, a list of symbols in the alphabet
@attribute currentState, a list containing the current state
@attribute F, a list of accept states
'''

class NFA:
    def __init__(self, NFAdict):
        self.Q = {}
        for x in range(1, NFAdict['Q'] + 1):
            list = []
            list.append(x)
            self.Q[x] = State(list, NFAdict['T'], NFA['F'])
        self.E = NFAdict['E']
        self.currentState = []
        self.currentState.append(NFAdict['q0'])
        self.F = NFAdict['F']

'''
A class that represents a State in our NFA.

@param state, a list of states
@param transitions, a list of transitions
@param accepts, a list of accepting states

@attribute state, a list containing the state
@attribute accepts, a boolean flag indicating if a state is an accepting state
@attribute transitions, a dictionary of transitions, keyed by symbols in the alphabet
'''

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


'''
A Class that represents a State in our DFA.

@param states, a list of possible NFA states
@param x, the id of the state
@param accepts, the list of accept states

@attribute states, a list of possible NFA states
@attribute stateid, the id of the state
@attribute transitions, a dicitonary keyed by the symbols in the alphabet
    (transitions are only set with the settransition function)
@attribute accepts, a boolean flag indicating if this state is an accept state
'''
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

    '''
    A function that sets a states' transition on a given symbol to a given next state.
        
    @param symbol, the symbol
    @param nextstate, given the symbol, the current state transitions to this state
    '''
    def settransition(self, symbol, nextstate):
        self.transitions[symbol] = nextstate

'''
A function that takes in the input file, and returns a container with the NFA information.

@param filename the filename

@return a dictionary of NFA information
'''
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

'''
A function that generates a list of NFA states it is possible 
to be in without scanning input (only epsilon transitions).

@param nfa, the nfa
@param curr, the current DFA state

@return a list of possible NFA states
'''
def stateswecanbein(nfa, curr):

    epsilons = []
    hold = []

    for y in curr.states:
        hold.append(int(y))

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

    return hold

'''
A function that finds all of the transitions possible for each symbol.

@param nfa, the nfa
@param curr, the current state

@return a dictionary keyed at each symbol in the alphabet, containing a list of possible NFA state transitions
'''
def alltransitions(nfa, curr):

    # find the NFA states we can epsilon transition to, for each state in curr
    hold = stateswecanbein(nfa, curr)

    # WE CHECK THE TRANSITIONS FOR ALL SYMBOLS
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

        if len(trans[symbol]) is 0:
            trans[symbol].append('0')

    return trans

'''
A function that sets the transitions for a specified DFA state, as well as generates 
DFAState objects on an as-needed basis. 

@param id, the id number of the state to set transitions for
@param states, the dictionary of generated DFAState objects
@param nfa, the nfa

@return an updated dictionary of generated DFA State objects
'''
def settransition(id, states, nfa):

    curr = states[id] #curr is the DFA state we are setting transitions for
    newstates = states

    trans = alltransitions(nfa, curr)

    trans = getridofduplicates(trans, nfa.E)

    for symbol in nfa.E:

        sid = checkifcreated(symbol, newstates, trans)

        if sid is 0:
            sid = len(newstates) + 1
            tmp = DFAState(trans[symbol], sid, nfa.F)
            newstates[sid] = tmp

        curr.settransition(symbol, sid)

    return newstates

'''
A function that takes in a dictionary of lists and returns a dictionary of lists without duplicates.

@param trans, a dictionary keyed to lists of transitions
@E, the list of symbols in the alphabet

@return a dictionary keyed to lists of transitions, without the duplicates
'''
def getridofduplicates(trans, E):

    t = {}
    for symbol in E:
        t[symbol] = []

    for symbol in E:
        for x in trans[symbol]:
            if x not in t[symbol]:
                t[symbol].append(x)

    return t

'''
A function that checks is a DFA state has already been created. 

@param symbol, the symbol to key the dictionary of transitions
@param newstates, the dictionary of created states
@param trans, a dictionary of transitions

@return the id of the duplicate, or 0 if the state has not been created
'''
def checkifcreated(symbol, newstates, trans):

    newid = 0
    for s in newstates:
        counterpart = 0
        # we have to check if trans[symbol] == newstates[s].states
        if len(trans[symbol]) is len(newstates[s].states):
            for onestate in trans[symbol]:
                for correspondingstate in newstates[s].states:
                    if int(onestate) is int(correspondingstate):
                        counterpart = counterpart + 1

        if counterpart is len(trans[symbol]):
            newid = s
    return newid

'''
A function that checks if transitions have been defined for all states.

@param statedict, a dictionary of states
@param nfa, the nfa

@return the stateid that does not have a defined transition, or -1 
'''
def checkalltransitions(statedict, nfa):
    for x in statedict:
        for y in nfa.E:
            try:
                statedict[x].transitions[y]
            except:
                return x

    return -1

'''
A function that writes the DFA to the output file. 

@param outname, the file name of the output file
@param states, the dictionary of generated states
@param nfa, the nfa
'''
def write(outname, states, nfa):

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

'''
The main function: reads in the file, generates the DFA, and writes to file.

@param filename, the name of the input file
@param outname, the name of the output file 

'''
def main(filename, outname):

    nfa = NFA(readfile(filename))

    states = {}
    currentstate = DFAState(nfa.currentState, 1, nfa.F)
    states[1] = currentstate


    states = settransition(1, states, nfa)

    # Here, I could run a check that all states in generatedstates have transition

    notransition = checkalltransitions(states, nfa)
    while notransition is not -1:

        states = settransition(notransition, states, nfa)
        notransition = checkalltransitions(states, nfa)

    write(outname, states, nfa)

'''
Program Main.
'''
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
