import json, os
from graphviz import Digraph

EPSILON = "ε" #ε

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

# Epsilon Closure here is not correct
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

def drawDfa(dfa_states, view_graph):
    dfa_graph = Digraph(graph_attr={'rankdir': 'LR'})

    index = 0
    for state in dfa_states:
        if dfa_states[state][0] == False:
            dfa_graph.attr("node", shape = 'circle')
        else:
            dfa_graph.attr("node", shape = 'doublecircle')
        dfa_graph.node(state)
        if index == 0:
            index += 1
            dfa_graph.attr("node", shape = 'none')
            dfa_graph.node('')
            dfa_graph.edge("", state)
    for state in dfa_states:
        for input_next in dfa_states[state][1]:
            dfa_graph.edge(state, input_next[1], input_next[0])

    picFile = "DFA"
    dfa_graph.render(picFile, view = view_graph, format = 'png', overwrite_source = True)
    os.remove("DFA")

def dfaFlow(view_graph = False):
    nfa_states = createNfaStates()
    dfa_states = createDfaStates(nfa_states)
    print(dfa_states)
    drawDfa(dfa_states, view_graph)
    return dfa_states