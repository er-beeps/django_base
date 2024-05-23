from django import template
from django.contrib.auth.models import Group
import itertools,os
from authentication.models import User


register = template.Library()

global app_label
app_label=[]
@register.simple_tag
def create_list(*args):
    return args

@register.filter
def check_permission(user,param):
    # check if Model is present or not
    action=param[0]
    slug=param[1]
    
    try:
        permission = underscore_to_camelcase(slug).lower()
    except Exception as e:
        print(e)
        return False
    # check for if a user has permission (check in both directly and through group)
    # get group permission from user group
    if user.groups.first():
        group_permissions = Group.objects.get(name=user.groups.first()).permissions.all().values_list('codename')
    else:
        return False    
    
    #join all tuples in single list
    user_permissions = [i for i in itertools.chain(*group_permissions)]
    #check if persmission exists
    check_perm = "%s_%s" % (action,permission)
    
    if check_perm in user_permissions:
        return True
    else:
        return False

def underscore_to_camelcase(value):
    output = ""
    first_word_passed = False
    for word in value.split("_"):
        if not word:
            output += "_"
            continue
        if first_word_passed:
            output += word.capitalize()
        else:
            output += word.capitalize()
        first_word_passed = True
    return output


@register.filter(name='has_group') 
def has_group(user, group_names):
    group_names = group_names.split(',')
    return user.groups.filter(name__in=group_names).exists()
    
# for getting column label
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# for getting value from db using column key
@register.filter
def get_item_value(item, column):
    value = getattr(item, column, '')
    if isinstance(value, str) and len(value) > 50:
        value = f"{value[:50]}..."
    # Truncate the value if its length is greater than 50 characters
    return value


# prepare link for column
@register.filter
def get_item_value_as_url(item, column):
    value = 'item.'+column
    return eval(value).url


@register.filter(name='field_type')
def field_type(field):
    return field.field.widget.__class__.__name__ 

@register.filter(name='column_type')
def column_type(field,model):
    field_object = eval(model)._meta.get_field(field)
    field_type=field_object.get_internal_type()
    return field_type 

@register.filter
def make_action_only(value):
    action = value.split('_')[0]
    action = 'create' if action == 'add' else 'edit' if action == 'change' else action
    return action

@register.filter
def check_app_label(value):
    if value in app_label:
        return False
    else:
        app_label.append(value)
        return True
    
@register.filter
def clear_app_label(value):
    app_label.clear()
    return ''


@register.filter
def add_to_query(querydict, keyvalue):
    """
    Adds a key-value pair to the given QueryDict and returns the updated QueryDict.
    Usage: {{ request.GET|add_to_query:"page=2" }}
    """
    key, value = keyvalue.split("=")
    updated_querydict = querydict.copy()
    updated_querydict[key] = value
    return updated_querydict.urlencode()

# check file extension
@register.filter
def get_extension(url):
    # Split the URL to get the file extension
    file_extension = url.split('.')[-1].lower()
    return file_extension

@register.filter
def file_extension(value):
    _, extension = os.path.splitext(value)
    return extension.lower()

@register.filter
def encoded_file_path(path):
    return path.replace('/', '%slash%')

@register.filter
def encoded_path(path):
    return path.replace('\\', '/')

@register.filter
def info_value(path):
    file_info = FileInfo.objects.filter(path=path)
    if file_info.exists():
        return file_info.first().info
    else:
        return ""

@register.simple_tag
def calculate_number(value,percent):
    value = float(value)
    percent = float(percent)
    return (value*percent)/100

@register.simple_tag
def calculate_sum(val1,val2):
    val1 = 0 if val1 == '' else val1
    val2 = 0 if val2 == '' else val2
    return int(val1)+int(val2)

@register.filter(name='calculate_total')
def calculate_total(data, category):
    total = sum(item[category] for item in data.values())
    return total

@register.filter(name='calculate_dict_total')
def calculate_dict_total(data, keys_string):
    keys_to_sum = keys_string.split(":")
    total = 0
    for key in keys_to_sum:
        total+= sum(data[d_key][key] for d_key in data)
    return total


@register.filter
def calculate_total_marks(exam_grades):
    return sum(item.final_marks for item in exam_grades)


##convert 1,2,3 to nepali ordinal
@register.filter
def ordinal(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value == 1 :
        suffix = "प्रथम"
    elif value == 2 :
        suffix = "दोश्रो"
    elif value == 3 :
        suffix = "तेश्रो"
    elif value == 4 :
        suffix = "चौथो"
    elif value == 5 :
        suffix = "पाँचौ"
    elif value == 6 :
        suffix = "छैठौ"
    elif value == 7 :
        suffix = "सातौं"
    elif value == 8 :
        suffix = "आठौ"
    else:
        suffix = " " 

    return f"{suffix}"

@register.filter
def ordinal_program_type(value):

    if value == 'Yearly' :
        suffix = "वर्ष"
    elif value == 'Semester' :
        suffix = "सेमेष्टर"
    elif value == 'Trimester' :
        suffix = "सेमेष्टर"
    else:
        suffix = " " 

    return f"{suffix}"

nepali_numbers = {
    '0': '०',
    '1': '१',
    '2': '२',
    '3': '३',
    '4': '४',
    '5': '५',
    '6': '६',
    '7': '७',
    '8': '८',
    '9': '९',
}

def convert_to_nepali_numbers(value):
    return ''.join(nepali_numbers.get(char, char) for char in str(value))

register.filter('nepali_numbers', convert_to_nepali_numbers)


@register.filter
def unless_exists(value, check_list):
    lists = check_list.split(',')
    return False if value in lists else True