
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def validate_date_format(value):
    date_format = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(date_format, value):
        raise ValidationError("Invalid date format. Use YYYY-MM-DD.")

def only_int(value): 
    if value.isdigit()==False:
        raise ValidationError('ID contains characters')