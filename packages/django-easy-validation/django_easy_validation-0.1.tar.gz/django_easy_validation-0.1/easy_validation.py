import regex as re
import json
from django.db import connection

validation_error = {}
def fromDatabase(model, db_column, item):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {db_column} FROM {model} WHERE {db_column} = %s", [item])
        row = cursor.fetchone()
        print("*" * 100, row)
        return row


def unique(item, frags, req):
    if req[item]:
        db_column = item
        model = frags[1]
        attribute = frags[0]
        record = fromDatabase(model, db_column, item)
        if record:
            print('record', record)
            name = f'{item}_unique'
            validation_error[name] = f'{item.title()} must be unique'


def max(item, frags, req):
    if req[item]:
        max_value = frags[1]
        if len(req[item]) > int(max_value):
            name = f'{item}_max'
            validation_error[name] = f'{item.title()} must not be greater than {max_value} characters'


def min(item, frags, req):
    if req[item]:
        min_value = frags[1]
        if len(req[item]) < int(min_value):
            name = f'{item}_max'
            validation_error[name] = f'{item.title()} must be alteast {min_value} characters'


def required(item, frags, req):
    value = frags[0]
    if not req[item]:
        name = f'{item}_required'
        validation_error[name] = f'{item.title()} cannot be empty'


def email(item, frags, req):
    if req[item]:
        em = req['email']
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, em):
            name = "email"
            validation_error[name] = f'Invalid email, please provide valid email id'


def numeric(item, frags, req):
    if req[item]:
        if not str(req[item]).isnumeric():
            validation_error['number'] = f'Not a number: {item.title()} should be a number'


class Validator:

    def __init__(self, args):
        self.args = args

    def process_validation(item, rule):
        print(item, rule)

    def validate(request, rules):
        req = json.loads(request.body)
        for item, rule in rules.items():
            val_rules = rule.split("|")
            for val in val_rules:
                frags = val.split(":")
                function_name = frags[0]
                call_method = globals()[function_name]
                call_method(item, frags, req)
                # raise ValidationError(
                #     (" not an even number"),
                #     code="invalid",
                #     params={"value": "value"},
                # )
        return validation_error
