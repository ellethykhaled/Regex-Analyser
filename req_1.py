def firstElementValidation(regex):
    if len(regex) > 0:
        c = regex[0]
        if c == '+' or c == '*' or c == '/' or c == '?':
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
        elif c == '?' or c == '*' or c == '+':
            if (len(all_brackets) > 0 and all_brackets[-1] == '[') or index == 0:
                continue
            elif regex[index - 2] == '?' or regex[index - 2] == '*' or regex[index - 2] == '+':
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
        return False
    if not firstElementValidation(regex):
        return False
    if not regexBracketValidation(regex):
        return False
    if not lastBackslashValidation(regex):
        return False
    if not bracketContentsValidation(regex):
        return False
    return True

character_level_extra = []

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
    
    character_level_extra.append((allowed_all, level, is_allowed))

def lexBrackets(regex, level = 0):
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
                        lexSquareBrackets(regex[i+1:j], level + 1)
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
        elif c == '?' or c == '*' or c == '+' or c == '|':
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
                if next == '?' or next == '*' or next == '+' or next == '|':
                    extra = next
                elif regex[i] == '\\':
                    extra = next
                    if i + 2 < len(regex):
                        next_of_next = regex[i + 2]
                        if next_of_next == '?' or next_of_next == '*' or next_of_next == '+' or next_of_next == '|':
                            extra += next_of_next
            character_level_extra.append((c, level, extra))
            indices.append(i)
    characters = []
    for j in indices:
        characters.append(regex[j])
    # print(regex, characters)
    # print(regex, indices)


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
                    if character_level_extra[sub_index][0] == ')' and character_level_extra[sub_index][1] == level and character_level_extra[sub_index][2] == None:
                        found = True
                        character_level_extra.remove(character_level_extra[sub_index])
                        character_level_extra.remove(c_l_e)
                        break
        if not found:
            break
    return character_level_extra

ALL_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALL_NUMBERS = "1234567890"
ALL_SPECIAL = "!@#-_+=$%^&*()?><"

# State: (name, isTerminatingState, [(input, State)]
states = [('S0', False, [])]

def createStates(character_level_extra, state_index = 1, current_states_indices = [0], base_call = True):
    skipper = 0
    index = -1
    first_input = None
    first_state_index = None
    for c_l_e in character_level_extra:
        index += 1
        if skipper > 0:
            skipper -= 1
            continue
        character = c_l_e[0]
        level = c_l_e[1]
        extra = c_l_e[2]
        if character == '[':
            skipper = 1
            available_index = -1
            available_input_string = ''
            for c_t in character_level_extra[index + 1][0]:
                available_index += 1
                add_comma = False
                if available_index < len(character_level_extra[index + 1][0]) - 1:
                    add_comma = True
                if type(c_t) is str:        # Character
                    available_input_string += c_t
                elif type(c_t) is tuple:    # Tuple
                    available_input_string += (c_t[0] + '-' + c_t[1])
                if add_comma:
                    available_input_string += ', '
            if first_input is None:
                first_input = available_input_string
            # Create the new state
            new_state_name = 'S'+str(state_index)
            new_state = (new_state_name, False, [])
            states.append(new_state)
            if first_state_index is None and not base_call:
                first_state_index = state_index
            state_index += 1

            # Point the current older states to the new state
            current_states_indices = list(dict.fromkeys(current_states_indices))
            for old_state_index in current_states_indices:
                states[old_state_index][2].append((available_input_string, new_state_name))
        elif character == ']':
            available_index = -1
            available_input_string = ''
            for c_t in character_level_extra[index - 1][0]:
                available_index += 1
                add_comma = False
                if available_index < len(character_level_extra[index - 1][0]) - 1:
                    add_comma = True
                if type(c_t) is str:        # Character
                    available_input_string += c_t
                elif type(c_t) is tuple:    # Tuple
                    available_input_string += (c_t[0] + '-' + c_t[1])
                if add_comma:
                    available_input_string += ', '
            if first_input is None:
                first_input = available_input_string
        elif character == '(':
            for iterator in range(index, len(character_level_extra)):
                current_character = character_level_extra[iterator][0]
                current_level = character_level_extra[iterator][1]
                if current_character == ')' and level == current_level:
                    skipper = iterator - index
                    new_indices, state_index, available_input_string, sub_first_state_index = createStates(character_level_extra[index + 1:iterator], state_index, current_states_indices, False)
                    if first_state_index is None:
                        first_state_index = sub_first_state_index
                    if first_input is None:
                        first_input = available_input_string
                    # print(current_states_indices, new_indices, state_index)
                    character = ')'
                    extra = character_level_extra[iterator][2]
                    if extra == '*':
                        current_states_indices.extend(new_indices)
                    elif extra == '?':
                        current_states_indices.extend(new_indices)
                    elif extra == '+':
                        pass                            
                    else:
                        if iterator + 1 < len(character_level_extra) and character_level_extra[iterator + 1][1] != ')':
                            current_states_indices.clear()
                        current_states_indices.extend(new_indices)
                    break
        else:
            # Create the new state
            available_input_string = character
            if first_input is None:
                first_input = available_input_string
            new_state_name = 'S'+str(state_index)
            new_state = (new_state_name, False, [])
            states.append(new_state)
            if first_state_index is None and not base_call:
                first_state_index = state_index
            current_states_indices = list(dict.fromkeys(current_states_indices))
            for current_state_index in current_states_indices:
                states[current_state_index][2].append((character, new_state_name))
            current_states_indices.append(state_index)
            state_index += 1
        if extra == '*':
            current_state = states[state_index - 1]
            if character != ')':
                current_state[2].append((available_input_string, current_state[0]))
            else:
                if first_state_index is not None:
                    in_out = (available_input_string, 'S'+str(first_state_index))
                    if in_out not in current_state[2]:
                        current_state[2].append(in_out)
                else:
                    for new_index in new_indices:
                        in_out = (available_input_string, 'S'+str(new_index))
                        if in_out not in current_state[2]:
                            print(in_out, new_indices)
                            current_state[2].append(in_out)
            current_states_indices.append(state_index - 1)
        elif extra == '+':
            current_state = states[state_index - 1]
            current_state[2].append((available_input_string, new_state_name))
            current_states_indices.clear()
            current_states_indices.append(state_index - 1)
        elif extra == '?':
            current_states_indices.append(state_index - 1)
        elif extra == '|':
            available_input_string = character_level_extra[index + 1][0]
            skipper = 1
            current_states_indices = list(dict.fromkeys(current_states_indices))
            for current_state_index in current_states_indices:
                sub_index = 0
                for input_output in states[current_state_index][2]:
                    input_output = (input_output[0] + ', ' + available_input_string, input_output[1])
                    states[current_state_index][2][sub_index] = input_output
                    sub_index += 1
            next_extra = character_level_extra[index + 1][2]
            while next_extra == '|':
                skipper += 1
                available_input_string = character_level_extra[index + skipper][0]
                current_states_indices = list(dict.fromkeys(current_states_indices))
                for current_state_index in current_states_indices:
                    sub_index = 0
                    for input_output in states[current_state_index][2]:
                        input_output = (input_output[0] + ', ' + available_input_string, input_output[1])
                        states[current_state_index][2][sub_index] = input_output
                        sub_index += 1
                        if first_input is None or first_input == character:
                            first_input = input_output[0]
                next_extra = character_level_extra[index + skipper][2]
        else:
            if character == '(' or character == '[':
                pass
            elif (index == 0 and base_call) or (character != ')' and (character_level_extra[index - 1][2] == '?' or character_level_extra[index - 1][2] == '*') or character_level_extra[index - 1][2] is None):
            # elif (index == 0 and base_call) or (character != ')' and (character_level_extra[index][2] != '?' and character_level_extra[index][2] != '*')):
                # print('Clearing', character, character_level_extra[index - 1][2], index, base_call, current_states_indices)
                current_states_indices.clear()
            current_states_indices.append(state_index - 1)
    if base_call == True and index == len(character_level_extra) - 1:
        current_states_indices = list(dict.fromkeys(current_states_indices))
        for indexy in current_states_indices:
            states[indexy] = (states[indexy][0], True, states[indexy][2])
    if base_call == False:
        return current_states_indices, state_index, first_input, first_state_index

input_regex = input("Enter regular expression: ")
if validateRegex(input_regex):
    print('Valid\n')
    lexBrackets(input_regex)
    character_level_extra = removeUnnessecaryBrackets(character_level_extra)
    print(character_level_extra)
    createStates(character_level_extra)
    print(states)
else:
    print('Invalid')