
def validate_phone_number(number: str):
    if number.startswith('+'):
        number = number[1:]
    
    if number.isdigit() and len(number) == 11:
        if number[0] in ('7', '8'):
            return True
    
    return False


def edit_number(phone_number: str):
    if phone_number.startswith('+'):
        phone_number = phone_number[1:]
    
    if phone_number.startswith('7'):
        phone_number = '8' + phone_number[1:]

    return phone_number