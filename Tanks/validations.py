def validate_time(new_entry):
    if len(new_entry) > 5:
        return False
    
    checks = []
    for i, char in enumerate(new_entry):
        if i == 2:
            checks.append(char == ':')
        else:
            checks.append(char.isdecimal())
    
    return all(checks)   

def validate_numeric_entry(entry):
    if entry.isdecimal():
        return True

    elif entry == '.':
        return True

    else:
        return False