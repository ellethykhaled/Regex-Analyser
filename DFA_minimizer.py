from graphviz import Digraph
from NFA_creator import nfaFlow
from DFA_creator import dfaFlow

def minimizeDfa(dfa_states):
    possible_inputs = []
    for state in dfa_states:
        for input_next in dfa_states[state][1]:
            if input_next[0] not in possible_inputs:
                possible_inputs.append(input_next[0])

    accepting_states = []
    non_accepting_states = []


    for state in dfa_states:
        if dfa_states[state][0] == True:
            accepting_states.append(state)
        else:
            non_accepting_states.append(state)

    groups_to_process = []
    if len(accepting_states) > 0:
        groups_to_process.append(accepting_states)
    if len(non_accepting_states) > 0:
        groups_to_process.append(non_accepting_states)

    print('\nInitially non-accepting states:', accepting_states)
    print('\nInitially accepting states:', non_accepting_states)

    while True:
        breaker = True

        copy_to_process = groups_to_process.copy()

        index = -1
        for group in copy_to_process:
            index += 1
            if len(group) > 1:
                out_lier = None
                for possible_input in possible_inputs:
                    elements_behavior = []
                    for element in group:
                        next_state = None
                        for input_next in dfa_states[element][1]:
                            if input_next[0] == possible_input:
                                next_state = input_next[1]
                                break
                        if next_state is not None:
                            sub_index = -1
                            for g in copy_to_process:
                                sub_index += 1
                                if next_state in g:
                                    elements_behavior.append(sub_index)
                                    break
                    print('\nElements behaviour:', elements_behavior, 'for input', possible_input)

                    frequency_dict = {}
                    for behavior in elements_behavior:
                        if behavior not in frequency_dict:
                            frequency_dict[behavior] = 1
                        else:
                            frequency_dict[behavior] = frequency_dict[behavior] + 1
                    for behavior in frequency_dict:
                        if frequency_dict[behavior] == 1:
                            out_lier = behavior
                    if out_lier is not None:
                        sub_index = -1
                        for behavior in elements_behavior:
                            sub_index += 1
                            if behavior == out_lier:
                                out_lier = group[sub_index]
                                break
                        print('\nElement:', out_lier, 'does not belong to group', group)
                        breaker = False
                        break
            if not breaker:
                group.remove(out_lier)
                copy_to_process[index] = group
                copy_to_process.append([out_lier])
                print('\nNew groups:', copy_to_process)
                break

        if breaker:
            break

        groups_to_process = copy_to_process
        
    print(groups_to_process)

    print()
    return dfa_states

def allFlow():
    if nfaFlow(False) == True:
        dfa_states = dfaFlow(True)
        minimized_dfa = minimizeDfa(dfa_states)

allFlow()