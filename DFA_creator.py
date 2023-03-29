import json
from graphviz import Digraph
from NFA_creator import nfaFlow

EPSILON = "ε" #ε
NOT_EPSILON = "!ε" #ε

def createNfaStates():
    with open('NFA.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    states = {}
    for state in data:
        if state == "startingState":
            continue
        input_next = []
        for edges in data[state]:
            if edges == "isTerminatingState":
                continue
            for edge in data[state][edges]:
                input_next.append((edges, edge))
        states[state] = (data[state]["isTerminatingState"], input_next)

    return states

def createDfaStates(nfa_states):
    while True:
        found_epsilon = False
        for state in nfa_states:
            # print(state)
            to_be_deleted = None
            deleter = None
            for input_next in nfa_states[state][1]:
                if input_next[0] == EPSILON:
                    # print('Extending', nfa_states[input_next[1]][1])
                    nfa_states[state][1].extend(nfa_states[input_next[1]][1])
                    nfa_states[state] = (nfa_states[state][0], list(dict.fromkeys(nfa_states[state][1])))

                    to_be_deleted = input_next[1]
                    deleter = state
                    # print('Removing', input_next)
                    nfa_states[state][1].remove(input_next)

                    found_epsilon = True
                    break
            if found_epsilon == True:
                break
        if found_epsilon == False:
            break

        # print('Before deletion', nfa_states, '\nDeleter:', deleter, 'Deleted:', to_be_deleted)

        deleted_is_terminating = nfa_states[to_be_deleted][0]
        nfa_states[deleter] = (nfa_states[deleter][0] or deleted_is_terminating, nfa_states[deleter][1])

        for state in nfa_states:
            new_input_next = []
            for input_next in nfa_states[state][1]:
                if input_next[1] == to_be_deleted:
                    input_next = (input_next[0], deleter)
                new_input_next.append(input_next)
            nfa_states[state] = (nfa_states[state][0], new_input_next)

        del nfa_states[to_be_deleted]
        to_be_deleted = None
        deleter = None
        # print('\nAfter deletion', nfa_states, '\n\n')
    return nfa_states

# nfaFlow()
def dfaFlow():
    nfa_states = createNfaStates()
    dfa_states = createDfaStates(nfa_states)
    print(dfa_states)

dfaFlow()