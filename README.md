# Parser

Description of project:
This project, contains a parser that reads the rows in a csv-file and parses them to an array of arrays which are inserted to a list of dictionaries with key-value pairings. Lastly it writes the key-value pairings to a json file.
It handles parsing of unquoted fields, quoted fields, commas inside of quoted fields, as well as escaped quotation marks inside of quoted fields.

It follows the RFC 4180 standard with regards to parsing
- simple unquoted fields
- multiple rows
- quoted fields
- commas inside of quoted fields
- quotes inside of quotes

---------------------------------------------------

Run and Build:
```
    py parser.py
```


Run tests and check codecoverage:

First, install the coverage package (only needed once):
```
    python -m pip install coverage
```

Then run the tests and generate a coverage report:
```
    py -m unittest test_parser.py
    python -m coverage run -m unittest discover
    python -m coverage report -m
```
---------------------------------------------------

Description of the softwarearchitecture:


---------------------------------------------------

UML diagram:
