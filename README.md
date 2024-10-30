# json-files
JSON files processing (python)

### Installation
`pip install -r requirements.txt`

### Running
`python people.py [file_name.json] --[command]`

`file_name.json` should be in the following format:
```
{
    "people": [
        {
            "first_name": "John",
            "last_name": "Doe",
            "height": 179,
            "currency": "EUR",
            "salary": 5100
        }
    ]
}
```

Following commands are available:
* --stats - displays people earning in EUR and overall average height
* --add - adds another person to the file
* --mod - asks for person and modifies their earnings

### Testing
Unit tests run using pytest library.
`pytest`

To produce coverage report in html format:
`pytest --cov-report html --cov`