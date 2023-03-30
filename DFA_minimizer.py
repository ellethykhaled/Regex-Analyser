from graphviz import Digraph
from NFA_creator import nfaFlow
from DFA_creator import dfaFlow

def minimizeDfa(dfa_states):
    return dfa_states

def allFlow():
    nfaFlow(False)
    dfa_states = dfaFlow(True)
    minimized_dfa = minimizeDfa(dfa_states)

allFlow()