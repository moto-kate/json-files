import sys
import pytest
import schema
import json
import people
from approvaltests.approvals import verify
from approvaltests import verify_all_combinations
from people import parse_json, validate_people, get_people_list, \
    get_full_name, display_eur_earners, display_avg_height, \
    read_person_from_input, add_person

test_person_1 = {
    'first_name': 'John',
    'last_name': 'Doe',
    'height': 179,
    'currency': 'EUR',
    'salary': 5100
}
test_person_2 = {
    'first_name': 'Jane',
    'last_name': 'Marsch',
    'height': 165,
    'currency': 'PLN',
    'salary': 6700
}

test_people_list = [test_person_1, test_person_2]

# @pytest.fixture
# def mock_argv():


def test_get_cl_params(monkeypatch):
    file_name = 'file.json'
    command = '--stats'
    monkeypatch.setattr(sys, 'argv', ['', file_name, command])

    from people import get_cl_params

    assert get_cl_params() == {
        'file_name': file_name, 'command': command}

# def test_read_file(mocker):


def test_parse_json_ok():
    assert parse_json('{ "a": 1 }') == {'a': 1}


def test_parse_json_fail():
    with pytest.raises(json.decoder.JSONDecodeError):
        parse_json('{ "a: 1 }')


def test_validate_people_ok():
    validate_people({'people': [test_person_1, test_person_2]})


def test_validate_people_fail():
    with pytest.raises(schema.SchemaError):
        validate_people({'people': [{}]})


def test_get_people_list(mocker):
    test_file_name = 'test-filename.json'
    test_people = {'people': [test_person_1]}
    mocker.patch('people.read_file', return_value='')
    mocker.patch('people.parse_json', return_value=test_people)
    mocker.patch('people.validate_people', return_value=True)
    read_file_spy = mocker.spy(people, 'read_file')
    parse_json_spy = mocker.spy(people, 'parse_json')
    validate_people_spy = mocker.spy(people, 'validate_people')

    assert get_people_list(test_file_name) == [test_person_1]
    read_file_spy.assert_called_once_with(test_file_name)
    parse_json_spy.assert_called_once_with('')
    validate_people_spy.assert_called_once_with(test_people)


# @pytest.mark.skip('WIP')
# def test_write_file():


@pytest.mark.parametrize(
    'person,full_name', [
        ({'first_name': 'John', 'last_name': 'Rambo'}, 'John Rambo'),
        ({'first_name': '', 'last_name': ''}, '')
    ]
)
def test_get_full_name(person, full_name):
    assert get_full_name(person) == full_name


def test_display_eur_earners(capsys):
    display_eur_earners(test_people_list)

    captured_output = capsys.readouterr().out
    assert captured_output == 'People earning in EUR:\n  John Doe\n'


def test_display_avg_height(capsys):
    display_avg_height(test_people_list)

    captured_output = capsys.readouterr().out
    assert captured_output == 'Average height: 172.00 cm\n'


# def test_display_stats():

def test_read_person_from_input(monkeypatch):
    def mock_inputs():
        yield 'Logan'
        yield 'Wolverine'
        yield '210'
        yield 'USD'
        yield '21000'

    input_values_generator = mock_inputs()
    monkeypatch.setattr(
        'builtins.input', lambda _: next(input_values_generator))

    # Instead of:
    # assert read_person_from_input() == {
    #     'first_name': 'Logan',
    #     'last_name': 'Wolverine',
    #     'height': 210,
    #     'currency': 'USD',
    #     'salary': 21000
    # }
    # verify(read_person_from_input())
    verify_all_combinations(read_person_from_input, ())
    # ( (some args,...), (other args...) )
    # https://snyk.io/advisor/python/approvaltests/functions/approvaltests.verify_all_combinations


def test_add_person(mocker):
    people_list = [test_person_1]
    file_name = 'f.json'

    mocker.patch('people.read_person_from_input', return_value=test_person_2)
    mocker.patch('people.write_file', return_value=None)
    write_file_spy = mocker.spy(people, 'write_file')

    add_person(file_name, people_list)

    write_file_spy.assert_called_once_with(
        file_name, '{\n  "people": null\n}')
