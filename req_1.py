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

ALL_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALL_NUMBERS = "1234567890"
ALL_SPECIAL = "!@#-_+=$%^&*()?><"

# State: (name, isTerminatingState, [(input, State)]
states = [('S0', False, [])]
state_index = 1

def createStates(character_level_extra, current_state_indices = [0]):

    skipper = 0
    for c_l_e in character_level_extra:
        if skipper > 0:
            skipper -= 1
            continue
        character = c_l_e[0]
        level = c_l_e[1]
        extra = c_l_e[2]
        if character == '[':
            skipper = 1

        print(c_l_e)


    pass

input_regex = input("Enter regular expression: ")
if validateRegex(input_regex):
    print('Valid\n')
    lexBrackets(input_regex)
    print(character_level_extra, '\n')
    createStates(character_level_extra)
else:
    print('Invalid')