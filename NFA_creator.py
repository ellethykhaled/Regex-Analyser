import json, os
from graphviz import Digraph

EPSILON = "ε" #ε
PLUS = '+'
STAR = '*'
Q_MARK = '?'
OR = '|'

ALL_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALL_NUMBERS = "1234567890"
ALL_SPECIAL = " ~[{]}!@#-_+=$%^&*()?><"

ALL_CHARACTERS = ALL_LETTERS+ALL_NUMBERS+ALL_SPECIAL

def firstElementValidation(regex):
    if len(regex) > 0:
        c = regex[0]
        if c == PLUS or c == STAR or c == '/' or c == Q_MARK:
            return False
    return True

def regexBracketValidation(regex):
    all_brackets = []
    index = 0
    for c in regex:
        back_iterator = index - 1
        index += 1
        backslash_count = 0
        while back_iterator >= 0 and regex[back_iterator] == '\\':
            backslash_count += 1
            back_iterator -= 1
        if backslash_count % 2 == 1:
            continue
        if c == '(':
            flag = False
            for b in all_brackets:
                if b == '[':
                    flag = True
                    break
            if flag:
                continue
            all_brackets.append(c)
        elif c == ')':
            flag = False
            for b in all_brackets:
                if b == '[':
                    flag = True
                    break
            if flag:
                continue
            if len(all_brackets) > 0:
                if all_brackets[-1] == '(':
                    all_brackets.pop()
                else:
                    return False
            else:
                return False
        elif c == '[':
            flag = False
            for b in all_brackets:
                if b == '[':
                    flag = True
                    break
            if flag:
                continue
            all_brackets.append(c)
        elif c == ']':
            if len(all_brackets) > 0:
                if all_brackets[-1] == '[':
                    all_brackets.pop()
                else:
                    return False
        elif c == '{':
            all_brackets.append(c)
        elif c == '}':
            if len(all_brackets) > 0:
                if all_brackets[-1] == '{':
                    all_brackets.pop()
                else:
                    return False
            else:
                return False
        elif c == Q_MARK or c == STAR or c == PLUS:
            if (len(all_brackets) > 0 and all_brackets[-1] == '[') or index == 0:
                continue
            elif regex[index - 2] == Q_MARK or regex[index - 2] == STAR or regex[index - 2] == PLUS:
                return False

    if len(all_brackets) > 0:
        return False
    return True

def lastBackslashValidation(regex):
    if regex[-1] == '\\':
        back_iterator = len(regex) - 2
        backslash_count = 0
        while back_iterator >= 0 and regex[back_iterator] == '\\':
            backslash_count += 1
            back_iterator -= 1
        return backslash_count % 2 == 1
    return True

def squareBracketContentsValidation(regex):
    if len(regex) == 0 or (len(regex) == 1 and regex[0] == '^'):
        return False
    index = 0
    dash_indices = []
    for c in regex:
        if index == 1 and c == '-' and regex[0] == '^':
            index += 1
            continue
        if c == '-' and index > 0 and index < len(regex) - 1:
            if len(dash_indices) > 0:
                old_index = dash_indices[-1]
                if index == old_index + 1 or index == old_index + 2:
                    index += 1
                    continue
            dash_indices.append(index)
        index += 1
    for dash_index in dash_indices:
        if regex[dash_index - 1] > regex[dash_index + 1]:
            return False
    return True

def bracketContentsValidation(regex):
    index = 0
    bracket_indices_stack = []

    for c in regex:
        if c == '(':
            found_opening_bracket = False
            for b in bracket_indices_stack:
                if regex[b] == '[':
                    found_opening_bracket = True
                    break
            if found_opening_bracket:
                continue
            bracket_indices_stack.append(index)
        elif c == ')':
            found_opening_bracket = False
            for b in bracket_indices_stack:
                if regex[b] == '[':
                    found_opening_bracket = True
                    break
            if found_opening_bracket:
                continue
            opening_index = bracket_indices_stack.pop()
            if not firstElementValidation(regex[opening_index+1:index]):
                return False
        elif c == '[':
            found_opening_bracket = False
            for b in bracket_indices_stack:
                if regex[b] == '[':
                    found_opening_bracket = True
                    break
            if found_opening_bracket:
                continue
            bracket_indices_stack.append(index)
        elif c == ']':
            found_opening_bracket = False
            for b in bracket_indices_stack:
                if regex[b] == '[':
                    found_opening_bracket = True
                    break
            if not found_opening_bracket:
                continue
            opening_index = bracket_indices_stack.pop()
            if not squareBracketContentsValidation(regex[opening_index+1:index]):
                return False
        index += 1
    return True

def validateRegex(regex):
    if len(regex) == 0:
        return True
    if not firstElementValidation(regex):
        return False
    if not regexBracketValidation(regex):
        return False
    if not lastBackslashValidation(regex):
        return False
    if not bracketContentsValidation(regex):
        return False
    return True

def lexSquareBrackets(regex, level):
    is_allowed = True
    allowed_characters = []
    index = 0
    dash_indices = []
    for c in regex:
        if index == 1 and c == '-' and regex[0] == '^':
            index += 1
            continue
        if c == '-' and index > 0 and index < len(regex) - 1:
            if len(dash_indices) > 0:
                old_index = dash_indices[-1]
                if index == old_index + 1 or index == old_index + 2:
                    index += 1
                    continue
            dash_indices.append(index)
        index += 1
    if regex[0] == '^':
        is_allowed = False

    allowed_tuples = []
    for dash_index in dash_indices:
        current_tuple = (regex[dash_index - 1], regex[dash_index + 1])
        if current_tuple not in allowed_tuples:
            allowed_tuples.append(current_tuple)

    allowed_all = []

    index = -1
    dash_index = 0
    for c in regex:
        index += 1
        if index == 0 and regex[0] == '^':
            continue
        if dash_index < len(dash_indices):
            if index == dash_indices[dash_index] or index == dash_indices[dash_index] - 1:
                continue
            elif index == dash_indices[dash_index] + 1:
                dash_index += 1
                continue
        add_c = True
        for t in allowed_tuples:
            if c >= t[0] and c <= t[1]:
                add_c = False
        if add_c and c not in allowed_characters:
            allowed_characters.append(c)

    for c in allowed_characters:
        allowed_all.append(c)
    for t in allowed_tuples:
        allowed_all.append(t)
    
    # print(allowed_all)
    
    return (allowed_all, level, is_allowed)

def lexBrackets(regex, level = 0, character_level_extra = []):
    i = -1
    last_ignorer = 0
    indices = []
    for c in regex:
        i += 1
        if i < last_ignorer:
            continue
        if c == '[':
            indices.append(i)
            character_level_extra.append((c, level, None))
            brackets_indices = [i]
            for j in range(i + 1, len(regex)):
                if regex[j] == ']':
                    brackets_indices.pop()
                    if len(brackets_indices) == 0:
                        character_level_extra.append(lexSquareBrackets(regex[i+1:j], level + 1))
                        last_ignorer = j
                        break
        elif c == '(':
            indices.append(i)
            character_level_extra.append((c, level, None))
            brackets_indices = [i]
            for j in range(i + 1, len(regex)):
                if regex[j] == '(':
                    brackets_indices.append(j)
                elif regex[j] == ')':
                    brackets_indices.pop()
                    if len(brackets_indices) == 0:
                        lexBrackets(regex[i+1:j], level + 1)
                        last_ignorer = j
                        break
        elif c == Q_MARK or c == STAR or c == PLUS or c == OR:
            if c == OR:
                if i > 0:
                    previous = regex[i - 1]
                    if previous == Q_MARK or previous == STAR or previous == PLUS:
                        character_level_extra.append((c, level, None))
                else:
                    character_level_extra.append((EPSILON, level, OR))
            continue
        else:
            if c == '\\':
                last_ignorer += 2
            if not(c == ')' or c == ']'):
                # print(regex[i])
                pass
            extra = None
            if i + 1 < len(regex):
                next = regex[i + 1]
                if next == Q_MARK or next == STAR or next == PLUS or next == OR:
                    extra = next
                elif regex[i] == '\\':
                    extra = next
                    if i + 2 < len(regex):
                        next_of_next = regex[i + 2]
                        if next_of_next == Q_MARK or next_of_next == STAR or next_of_next == PLUS or next_of_next == OR:
                            extra += next_of_next
            character_level_extra.append((c, level, extra))
            indices.append(i)
    characters = []
    for j in indices:
        characters.append(regex[j])
    # print(regex, characters)
    # print(regex, indices)
    return character_level_extra


def removeUnnessecaryBrackets(character_level_extra):
    while True:
        found = False
        index = -1
        for c_l_e in character_level_extra:
            index += 1
            character = c_l_e[0]
            level = c_l_e[1]
            if character == '(':
                for sub_index in range(index, len(character_level_extra)):
                    if character_level_extra[sub_index][0] == ')' and character_level_extra[sub_index][1] == level:
                        if character_level_extra[sub_index][2] == None:
                            if index > 0 and character_level_extra[index - 1][2] != OR and character_level_extra[index - 1][0] != OR:
                                # print('Removing:', c_l_e, character_level_extra[sub_index], index, sub_index)
                                found = True
                                character_level_extra.pop(sub_index)
                                character_level_extra.pop(index)
                        break

        if not found:
            break
    return character_level_extra

def fillEmptyBrackets(character_level_extra):
    index = -1
    for c_l_e in character_level_extra:
        index += 1
        character = c_l_e[0]
        level = c_l_e[1]
        if character == '(':
            if index + 1 < len(character_level_extra) and character_level_extra[index + 1][0] == ')' and level == character_level_extra[index + 1][1]:
                character_level_extra.insert(index + 1, (EPSILON, level + 1, None))
    return character_level_extra

def fillEmptyOrsRight(character_level_extra):
    index = -1
    for c_l_e in character_level_extra:
        index += 1
        level = c_l_e[1]
        extra = c_l_e[2]
        if extra is not None:
            if len(extra) == 1:
                if extra == OR:
                    if index == len(character_level_extra) - 1 or character_level_extra[index + 1][0] == ')':
                        character_level_extra.insert(index + 1, (EPSILON, level, None))
            elif extra[-1] == OR:
                if index == len(character_level_extra) - 1 or character_level_extra[index + 1][0] == ')':
                        character_level_extra.insert(index + 1, (EPSILON, level, None))
    return character_level_extra

# State: (name, isTerminatingState, [(input, State)]
global states
states = []
   
def createStates(character_level_extra, state_index = 1, previous_state_index = 0, next_state_index = None):
    base_call = False
    if next_state_index is None:
        base_call = True
        states = [('S0', False, [])]
    else:
        absolute_next_index = next_state_index
        absolute_previous_index = previous_state_index

    skipper = 0
    state_indexer = -1
    or_flag = None
    for c_l_e in character_level_extra:
        state_indexer += 1
        if skipper > 0:
            skipper -= 1
            continue

        # in-state
        previous_state = states[previous_state_index]

        character, level, extra = c_l_e

        # Create the new state to be next (out-state)
        if next_state_index is None or previous_state_index == next_state_index or (not base_call and (or_flag is not None or state_indexer == 0)):
            next_state_index = state_index
            new_state_name = 'S'+str(state_index)
            new_state = (new_state_name, False, [])
            states.append(new_state)
            next_state = states[state_index]

            state_index += 1
        else:
            next_state = states[next_state_index]


        if character == '[':
            skipper = 1
            available_index = -1
            characters = ''
            for c_t in character_level_extra[state_indexer + 1][0]:
                available_index += 1
                add_comma = False
                if available_index < len(character_level_extra[state_indexer + 1][0]) - 1:
                    add_comma = True
                if type(c_t) is str:        # Character
                    characters += c_t
                elif type(c_t) is tuple:    # Tuple
                    characters += (c_t[0] + '-' + c_t[1])
                if add_comma:
                    characters += ', '
            # Create the new states
            new_state_name = 'S'+str(state_index)
            new_state = (new_state_name, False, [])
            states.append(new_state)
            current_state1 = states[state_index]
            state_index += 1

            new_state_name = 'S'+str(state_index)
            new_state = (new_state_name, False, [])
            states.append(new_state)
            current_state2 = states[state_index]
            state_index += 1

            if character_level_extra[state_indexer + 1][2] == False:
                characters = "NOT " + characters

            previous_state[2].append((EPSILON, current_state1[0]))
            current_state1[2].append((characters, current_state2[0]))
            current_state2[2].append((EPSILON, next_state[0]))

        elif character == '(':
            for iterator in range(state_indexer, len(character_level_extra)):
                current_character = character_level_extra[iterator][0]
                current_level = character_level_extra[iterator][1]
                current_extra = character_level_extra[iterator][2]
                if current_character == ')' and level == current_level:
                    skipper = iterator - state_indexer
                    # print('Call', previous_state_index, next_state_index)
                    c1_index, c2_index, state_index = createStates(character_level_extra[state_indexer + 1:iterator], state_index, previous_state_index, next_state_index)
                    # print('Return', c1_index, c2_index)
                    current_state1 = states[c1_index]
                    current_state2 = states[c2_index]
                    # print(previous_state, current_state1, current_state2, next_state)
                    extra = current_extra
                    if extra is not None and iterator + 1 < len(character_level_extra) and character_level_extra[iterator + 1][0] == OR:
                        current_extra = OR
                        skipper += 1
                    break
                    
        elif character == OR or character == ']' or character == ')':
            pass
        else:
            if character == '\\':
                skipper = 1
                if len(extra) == 1:
                    character += extra
                    extra = None
                else:
                    character += extra[0]
                    extra = extra[1]
            if character == '.':
                character = "CHAR"
            elif character == '\\w':
                character = "ALPHANUM"
            elif character == '\\W':
                character = "SPECIAL"
            elif character == '\\d':
                character = "DIGIT"
            elif character == '\\D':
                character = "NON-DIGIT"
            # Create the new current states
            new_state_name = 'S'+str(state_index)
            new_state = (new_state_name, False, [])
            states.append(new_state)
            current_state1 = states[state_index]

            state_index += 1

            new_state_name = 'S'+str(state_index)
            new_state = (new_state_name, False, [])
            states.append(new_state)
            current_state2 = states[state_index]

            state_index += 1

            previous_state[2].append((EPSILON, current_state1[0]))
            current_state1[2].append((character, current_state2[0]))
            current_state2[2].append((EPSILON, next_state[0]))
            
        if extra == STAR:
            current_state2[2].append((EPSILON, current_state1[0]))
            current_state1[2].append((EPSILON, next_state[0]))
        elif extra == PLUS:
            current_state2[2].append((EPSILON, current_state1[0]))
        elif extra == Q_MARK:
            current_state1[2].append((EPSILON, next_state[0]))
        
        if character == '(':
            extra = current_extra
            # print('Here extra character', character, current_extra)

        if extra != OR and character != OR and character != '[' and state_indexer < len(character_level_extra) - 1 and character_level_extra[state_indexer + 1][0] != OR:
            # print('Proceeding Here', c_l_e, character_level_extra[state_indexer + 1], previous_state_index, next_state_index)
            previous_state_index = next_state_index
            or_flag = True
        else:
            or_flag = None

    if base_call and state_indexer == len(character_level_extra) - 1:
        if next_state_index is None:
            next_state_index = 0
        t_state = states[next_state_index]
        states[next_state_index] = (t_state[0], True, t_state[2])
        print('Terminating State:', states[next_state_index],'\n')

    if not base_call:
        next_state[2].append((EPSILON, 'S'+str(absolute_next_index)))
        return absolute_previous_index, next_state_index, state_index
    else:
        for state in states:
            state = (state[0], state[1], list(dict.fromkeys(state[2])))
    
def writeNfa(states):
    with open('NFA.json', 'w', encoding='utf-8') as f:
        dict_to_write = {"startingState": "S0"}
        for state in states:
            sub_dict = {}
            sub_dict["isTerminatingState"] = state[1]
            for input_output in state[2]:
                if input_output[0] not in sub_dict:
                    sub_dict[input_output[0]] = []
                sub_dict[input_output[0]].append(input_output[1])
            dict_to_write[state[0]] = sub_dict
        json_string = json.dumps(dict_to_write, indent=3)
        f.write(json_string)

def drawNfa(view_graph):
    nfa_graph = Digraph(graph_attr={'rankdir': 'LR'})
    with open('NFA.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for state in data:
        if state == "startingState":
            continue
        if data[state]["isTerminatingState"] == False:
            nfa_graph.attr("node", shape = 'circle')
        else:
            nfa_graph.attr("node", shape = 'doublecircle')
        nfa_graph.node(state)
        if state == data["startingState"]:
            nfa_graph.attr("node", shape = 'none')
            nfa_graph.node('')
            nfa_graph.edge("", state)
    for state in data:
        if state == "startingState":
            continue
        for edges in data[state]:
            if edges == "isTerminatingState":
                continue
            for edge in data[state][edges]:
                nfa_graph.edge(state, edge, edges)

    picFile = "NFA"
    nfa_graph.render(picFile, view = view_graph, format = 'png', overwrite_source = True)
    os.remove("NFA")

def nfaFlow(view_graph = False):
    input_regex = input("\nEnter regular expression: ")
    if validateRegex(input_regex):
        print('\nValid regex\n')

        character_level_extra = lexBrackets(input_regex, 0, [])

        character_level_extra = fillEmptyOrsRight(character_level_extra)
        character_level_extra = removeUnnessecaryBrackets(character_level_extra)
        character_level_extra = fillEmptyBrackets(character_level_extra)
        print('Characters to parse:', character_level_extra, '\n')

        createStates(character_level_extra)
        print('NFA states: ',states, '\n')

        writeNfa(states)
        drawNfa(view_graph)

        print('Input regex: ', input_regex + '\n')
        return True   
    else:
        print('Invalid regex')
        return False