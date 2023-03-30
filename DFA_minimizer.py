from graphviz import Digraph
from NFA_creator import nfaFlow
from DFA_creator import dfaFlow

def minimizeDfa(dfa_states):

    accepting_states = []
    non_accepting_states = []

    groups_to_process = []

    for state in dfa_states:
        if dfa_states[state][0] == True:
            accepting_states.append(state)
        else:
            non_accepting_states.append(state)

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
                for element in group:
                    for input_next in dfa_states[element][1]:
                        if input_next[1] not in group:
                            print('Element', element, 'belonging to group', group,'can transition to', input_next[1], 'through', input_next[0])
                            breaker = False
                            out_lier = element
                            break
                    if not breaker:
                        break
                if not breaker:
                    found_group = False
                    print('Removing element', out_lier, 'from group', group)
                    group.remove(out_lier)
                    copy_to_process[index] = group
                    print('Available candidate groups:', copy_to_process, 'for element:', out_lier)
                    for candidate_group in copy_to_process:
                        if candidate_group == group:
                            continue
                        valid_candidate = True
                        for input_next in dfa_states[out_lier][1]:
                            if input_next[1] not in candidate_group and input_next[1] != out_lier:
                                print('Element', out_lier, 'cannot belong to group', candidate_group,'can transition to', input_next[1], 'through', input_next[0])
                                valid_candidate = False
                        if not valid_candidate:
                            break

                        if valid_candidate:
                            found_group = True
                            candidate_group.append(out_lier)
                            break
                    if not found_group:
                        copy_to_process.append([out_lier])
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