import json
import sys
import schema
from operator import itemgetter
from functools import reduce


def get_cl_params():
    file_name = sys.argv[1]
    command = sys.argv[2]
    return {'file_name': file_name, 'command': command}


def read_file(file_name: str) -> str:
    with open(file_name, 'r') as file:
        file_content = file.read()
        return file_content


def parse_json(json_as_str: str) -> dict:
    return json.loads(json_as_str)


people_schema = schema.Schema(
    {
        'people': [
            {
                'first_name': str,
                'last_name': str,
                'currency': schema.Or('EUR', 'USD', 'PLN'),
                'salary': int,
                'height': int,
            }
        ]
    }
)


def validate_people(people):
    people_schema.validate(people)


def get_people_list(file_name: str) -> list[dict]:
    people_as_json_str = read_file(file_name)
    people = parse_json(people_as_json_str)
    validate_people(people)
    return people.get('people')


def write_file(file_name: str, content: str):
    with open(file_name, 'w') as file:
        file.write(content)


def get_full_name(person):
    first_name, last_name = person.get('first_name'), person.get('last_name')
    if first_name and last_name:
        return first_name + ' ' + last_name
    return first_name + last_name


def display_eur_earners(people: list[dict]):
    people_earning_in_eur = filter(
        lambda person: person.get('currency') == 'EUR', people)
    print('People earning in EUR:')
    for person in people_earning_in_eur:
        print('  ' + get_full_name(person))


def display_avg_height(people: list[dict]):
    total = reduce(lambda sum, person: sum + person.get('height'), people, 0)
    avg_height = total / len(people)
    print('Average height:', '%.2f' % avg_height, 'cm')


def display_stats(people: list[dict]):
    display_eur_earners(people)
    display_avg_height(people)


def read_person_from_input():
    print('Please specify person data:')
    first_name = input('First name? ')
    last_name = input('Last name? ')
    height = int(input('Height [cm]? '))
    currency = input('Currency [EUR, USD, PLN]? ')
    salary = int(input('Salary? '))
    return {
        'first_name': first_name,
        'last_name': last_name,
        'height': height,
        'currency': currency,
        'salary': salary
    }


def add_person(file_name: str, people: list[dict]):
    person = read_person_from_input()
    updated_people = people.copy().append(person)
    write_file(file_name, json.dumps({'people': updated_people}, indent=2))


def modify_person(file_name: str, people: list[dict]):
    last_name = input('Last name? ')
    new_salary = int(input('New salary? '))
    updated_people = list(map(
        lambda person: dict(
            person, **{'salary': new_salary}) if person.get('last_name') == last_name else person,
        people
    ))
    write_file(file_name, json.dumps({'people': updated_people}, indent=2))


def handle_error(message: str, e: Exception):
    print(message)
    print(type(e))
    exit(1)


def main():
    try:
        file_name, command = itemgetter(
            'file_name', 'command')(get_cl_params())
    except Exception as e:
        handle_error('Missing or incorrect command line parameters', e)

    try:
        people_list = get_people_list(file_name)
    except Exception as e:
        handle_error('Missing or corrupt json file', e)

    try:
        if command == '--stats':
            display_stats(people_list)
        elif command == '--add':
            add_person(file_name, people_list)
        elif command == '--mod':
            modify_person(file_name, people_list)
        else:
            print('Unknown command.')
    except Exception as e:
        handle_error('Could not execute command', e)


if __name__ == '__main__':
    main()
