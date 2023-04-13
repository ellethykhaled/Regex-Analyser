import json, os
from graphviz import Digraph

EPSILON = "ε" #ε

# This function reads the NFA json file and restore its different states with their transitions
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

# This function removes EPSILONS and combines states that are connected together using EPSILONS
def epsilonlessNfaStates(nfa_states):
    possible_epsiloness_states = {}

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
        possible_epsiloness_states[state] = current_state_to_be

    start_states = ['S0']
    previous_input = {'S0': None}
    for state in nfa_states:
        for input_next in nfa_states[state][1]:
            if input_next[0] != EPSILON and input_next[1] not in start_states:
                start_states.append(input_next[1])
                previous_input[input_next[1]] = (state, input_next[0])

    to_be_deleted = []
    epsilonless_states = {}
    for state in possible_epsiloness_states:
        if state not in start_states:
            to_be_deleted.append(state)
        else:
            epsilonless_states[state] = (False, [])
    for state in to_be_deleted:
        del possible_epsiloness_states[state]
    
    for state in previous_input:
        is_terminating = False
        for sub_state in possible_epsiloness_states[state]:
            if nfa_states[sub_state][0] == True:
                is_terminating = True
                break
        epsilonless_states[state] = (is_terminating, epsilonless_states[state][1])
        if previous_input[state] is None:
            continue
        for mother_state in epsilonless_states:
            if previous_input[state][0] in possible_epsiloness_states[mother_state]:
                # print('Adding', (previous_input[state][1], state), 'to', mother_state)
                epsilonless_states[mother_state][1].append((previous_input[state][1], state))

    return epsilonless_states

# This function takes the epsilonless states and converts to DFA states
def createDfaStates(nfa_states):
    is_already_dfa = True
    for state in nfa_states:
        possible_inputs = []
        for input_next in nfa_states[state][1]:
            if input_next[0] in possible_inputs:
                is_already_dfa = False
                break
            possible_inputs.append(input_next[0])
        if not is_already_dfa:
            break
    if is_already_dfa:
        print('\nNFA is already a DFA\n')
        return nfa_states
    # print('\nNFA states:', nfa_states, '\n')

    possible_inputs = set()
    for state in nfa_states:
        print(state, nfa_states[state][1])
        for input_next in nfa_states[state][1]:
            possible_inputs.add(input_next[0])
    # print('Possible inputs:', possible_inputs, '\n')

    explored_sets_of_states = []

    dfa_states = {'S0': (nfa_states['S0'][0], [])}

    print('Possible inputs:', possible_inputs)
    for possible_input in possible_inputs:
        print(possible_input)
        current_state_to_be = ['S0']
        index = -1
        while index < len(nfa_states) - 1:
            index += 1
            for current_state in current_state_to_be:
                for input_next in nfa_states[current_state][1]:
                    if input_next[0] == possible_input and input_next[1] not in current_state_to_be:
                        current_state_to_be.append(input_next[1])
        current_state_to_be.sort()
        current_state_to_be.remove('S0')
        if current_state_to_be not in explored_sets_of_states:
            explored_sets_of_states.append(current_state_to_be)
        if len(current_state_to_be) > 0:
            dfa_states['S0'][1].append((possible_input, current_state_to_be))

    print('Initial dfa states:', dfa_states)

    set_of_new_states = {}

    explored_state_index = 0
    for states in explored_sets_of_states:
        explored_state_index += 1
        set_of_new_states['S'+str(explored_state_index)] = states

    for state in nfa_states:
        for input_next in nfa_states[state][1]:
            possible_inputs.add(input_next[0])

    state_index = 0
    for set_of_states in explored_sets_of_states:
        state_index += 1
        is_terminating = False
        for state in set_of_states:
            if nfa_states[state][0] == True:
                is_terminating = True
        
        list_of_transitions = []
        for possible_input in possible_inputs:
            current_state_to_be = []
            states_to_loop_on = []
            states_to_loop_on.extend(set_of_states)

            for current_state in states_to_loop_on:
                for input_next in nfa_states[current_state][1]:
                    if input_next[0] == possible_input and input_next[1] not in current_state_to_be:
                        current_state_to_be.append(input_next[1])

            current_state_to_be.sort()
            if current_state_to_be not in explored_sets_of_states:
                explored_state_index += 1
                explored_sets_of_states.append(current_state_to_be)
                set_of_new_states['S'+str(explored_state_index)] = current_state_to_be
            if len(current_state_to_be) > 0:
                for state_name in set_of_new_states:
                    if set_of_new_states[state_name] == current_state_to_be:
                        list_of_transitions.append((possible_input, state_name))
                        break
        if len(list_of_transitions) > 0 or is_terminating:
            dfa_states['S'+str(state_index)] = (is_terminating, list_of_transitions)

    # Renaming states of start state:
    new_names = []
    for input_next in dfa_states['S0'][1]:
        for state_name in set_of_new_states:
            if set_of_new_states[state_name] == input_next[1]:
                new_names.append((input_next[0], state_name))
                break
    dfa_states['S0'] = (dfa_states['S0'][0], new_names)

    return dfa_states

# This function outputs the DFA states to a png file illustrating the states and their transitions
def drawDfa(dfa_states, view_graph = False, another_name = 'DFA'):
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

    picFile = another_name
    dfa_graph.render(picFile, view = view_graph, format = 'png', overwrite_source = True)
    os.remove(another_name)

# This function holds the flow from the input NFA to the output DFA
def dfaFlow(view_graph = False):
    nfa_states = getNfaStates()
    epsilonless_nfa_states = epsilonlessNfaStates(nfa_states)
    print('Epsilonless states:', epsilonless_nfa_states)
    drawDfa(epsilonless_nfa_states, another_name = 'Epsilonless_NFA')
    dfa_states = createDfaStates(epsilonless_nfa_states)
    print('\nDfa states:', dfa_states)
    drawDfa(dfa_states, view_graph)
    return dfa_states