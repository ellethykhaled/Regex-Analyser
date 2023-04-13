import NFA_creator, DFA_creator, DFA_minimizer

# This function holds the whole flow from the input regex to the output minimized DFA
def allFlow():
    if NFA_creator.nfaFlow() == True:
        DFA_minimizer.minimizedDfaFlow(DFA_creator.dfaFlow())

allFlow()