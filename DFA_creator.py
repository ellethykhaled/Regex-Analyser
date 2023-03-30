import json, os
from graphviz import Digraph

EPSILON = "ε" #ε

def getNfaStates():
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

# Again, not always working algorith; it only works if every input character is unique
def createDfaStates(nfa_states):
    possible_dfa_states = {}

    for state in nfa_states:
        current_state_to_be = [state]
        index = -1
        while index < len(nfa_states) - 1:
            index += 1
            for current_state in current_state_to_be:
                for input_next in nfa_states[current_state][1]:
                    if input_next[0] == EPSILON and input_next[1] not in current_state_to_be:
                        current_state_to_be.append(input_next[1])

        current_state_to_be.sort()
        possible_dfa_states[state] = current_state_to_be

    start_states = ['S0']
    previous_input = {'S0': None}
    for state in nfa_states:
        for input_next in nfa_states[state][1]:
            if input_next[0] != EPSILON and input_next[1] not in start_states:
                start_states.append(input_next[1])
                previous_input[input_next[1]] = (state, input_next[0])

    to_be_deleted = []
    dfa_states = {}
    for state in possible_dfa_states:
        if state not in start_states:
            to_be_deleted.append(state)
        else:
            dfa_states[state] = (False, [])
    for state in to_be_deleted:
        del possible_dfa_states[state]
    
    for state in previous_input:
        is_terminating = False
        for sub_state in possible_dfa_states[state]:
            if nfa_states[sub_state][0] == True:
                is_terminating = True
                break
        dfa_states[state] = (is_terminating, dfa_states[state][1])
        if previous_input[state] is None:
            continue
        for mother_state in dfa_states:
            if previous_input[state][0] in possible_dfa_states[mother_state]:
                # print('Adding', (previous_input[state][1], state), 'to', mother_state)
                dfa_states[mother_state][1].append((previous_input[state][1], state))

    return dfa_states

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
    nfa_states = getNfaStates()
    dfa_states = createDfaStates(nfa_states)
    print(dfa_states)
    drawDfa(dfa_states, view_graph)
    return dfa_states