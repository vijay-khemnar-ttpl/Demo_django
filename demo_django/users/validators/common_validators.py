from django.core.exceptions import ValidationError
import re
from django.contrib.auth.password_validation import validate_password


def validate_custom_password(password):

    error_list = []
    # Minimum length of 8 characters
    if len(password) < 8 or not re.search(r'[a-z]', password) or not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[!@#\$%^&*()_+{}\[\]:;<>,.?~\\-]', password):
        if len(password) < 8 :
            error_list.append("8 Characters long")

         # At least one lowercase letter
        if not re.search(r'[a-z]', password) or  not re.search(r'[A-Z]', password):
            error_list.append("One lowercase letter and One uppercase letter")

        # At least one digit
        if not re.search(r'[0-9]', password):
            error_list.append("One number")

        # At least one symbol (you can customize the symbols as needed) 
        if not re.search(r'[!@#\$%^&*()_+{}\[\]:;<>,.?~\\-]', password):
            error_list.append("One special character")

        raise ValidationError(error_list)
        
    try:
        validate_password(password)
    except ValidationError as e:
        raise ValidationError({"password": e.messages})