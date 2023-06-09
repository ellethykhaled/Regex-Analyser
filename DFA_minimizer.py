import json
from DFA_creator import drawDfa

# This function reduces the DFA to a minimized DFA by combining states that have the same behaviour
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
                out_liers = []
                out_lier_behavior = None
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
                        else:
                            elements_behavior.append(-1)
                    # print('\nElements behaviour:', elements_behavior, 'for input', possible_input)

                    frequency_dict = {}
                    for behavior in elements_behavior:
                        if behavior not in frequency_dict:
                            frequency_dict[behavior] = 1
                        else:
                            frequency_dict[behavior] = frequency_dict[behavior] + 1

                    minimum_behavior = len(dfa_states)
                    if len(frequency_dict) != 1:
                        for behavior in elements_behavior:
                            if frequency_dict[behavior] < minimum_behavior:
                                minimum_behavior = frequency_dict[behavior]
                    
                        for behavior in elements_behavior:
                            if frequency_dict[behavior] == minimum_behavior:
                                out_lier_behavior = behavior
                                break
                    if out_lier_behavior is not None:
                        sub_index = -1
                        for behavior in elements_behavior:
                            sub_index += 1
                            if behavior == out_lier_behavior:
                                out_liers.append(group[sub_index])
                        # print('\nElements:', out_liers, 'does not belong to group', group)
                        breaker = False
                        break
            if not breaker:
                for out_lier in out_liers:
                    group.remove(out_lier)
                copy_to_process[index] = group
                copy_to_process.append(out_liers)
                # print('\nNew groups:', copy_to_process)
                break

        if breaker:
            break

        groups_to_process = copy_to_process
        
    print('\nFinal groups:', groups_to_process)

    for group in groups_to_process:
        if len(group) > 1:
            if 'S0' in group:
                representative = 'S0'
            else:
                representative = group[0]
            for state in dfa_states:
                index = -1
                for input_next in dfa_states[state][1]:
                    index += 1
                    if input_next[1] in group:
                        dfa_states[state][1][index] = (dfa_states[state][1][index][0], representative)
            for element in group:
                if element == representative:
                    continue
                del dfa_states[element]
    print('\nMinimized Dfa:', dfa_states)
    return dfa_states

# This function outputs the minimized DFA states to a json file
# as well as to a png file illustrating the states and their transitions
def writeMinimizedDfa(dfa_states):
    with open('Minimized_DFA.json', 'w', encoding='utf-8') as f:
        dict_to_write = {"startingState": "S0"}
        for state in dfa_states:
            sub_dict = {}
            sub_dict["isTerminatingState"] = dfa_states[state][0]
            for input_next in dfa_states[state][1]:
                sub_dict[input_next[0]] = input_next[1]
            dict_to_write[state] = sub_dict
        json_string = json.dumps(dict_to_write, indent=3)
        f.write(json_string)

# This function holds the flow from the input DFA to the output minimized DFA
def minimizedDfaFlow(dfa_states):
    minimized_dfa = minimizeDfa(dfa_states)
    drawDfa(minimized_dfa, another_name='Minimized_DFA')
    writeMinimizedDfa(minimized_dfa)

