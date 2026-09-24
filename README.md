# Parser

**Description of project:**\
This project contains a simple CSV-parser written in Python without any external parsing libraries. The parser reads CSV-formatted strings from a file and converts it to a list of dictionaries with key-value pairings based on the header row. The parser follows the RFC standard (except line endings inside of quoted fields), and can handle:
- unquoted fields, 
- quoted fields
- commas inside of quoted fields, 
- escaped quotation marks ("") inside of quoted fields
- different line endings CRLF and LF
- empty fields and empty lines
The result is serialized to a JSON file where each csv row corresponds to one JSON object with header field names as keys.

In the program, the encoding of the input CSV file is given explicitly as a parameter and can vary per file, while the resulting JSON output is always written as UTF-8, regardless of the input encoding.

---------------------------------------------------

**Run and Build:**
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

**Description of the software architecture:**\
The project consists of five functions used in different stages from reading the file (Unicode string) to splitting it into raw fields to converting these to dictionaries to converting this to a list of dictionaries and then writing this to a JSON file:

1. Loading\
    read_file(file_path, encoding) opens the file, reads it, and returns its full content as one decoded string. This is the only place that reads and decodes an input file, isolating the reading logic and encoding parameter. Therefore every other function only works with already decoded Unicode strings, and not raw bytes.

2. Parsing\
    my_split(line) splits one line into raw field strings. It scans the line character by character and uses a boolean (outer_quotations) to track whether the current position is inside a quoted field, deciding whether to split on a comma, toggle quote state, or append the character to the current field (including escaped "" quotes).

3. Internal data structure\
    parse_header turns the first line in a csv file into a list of header keys and raises ValueError on duplicates. 
    parse_csv_line maps the fields of one row onto these keys from parse_header, producing one dictionary per row. It takes a header as an optional argument as not all csv files contain a header.
    parse_csv calls read_file and splits the file's rows where it treats the first line as the header, calling parse_header, and calls parse_csv_line on the remaining lines. Then it collects the results into a list of dictionaries.

4. JSON export\
    write_json_file(file, encoding) calls parse_csv, producing a list of dictionaries. This is serialized to JSON-formatted strings in a .json file using json.dump, with ensure_ascii=False so special characters (æ, ø, å) are preserved rather than showing \uXXXX escapes. The output file is always written as UTF-8, regardless of which encoding the input CSV was read with as JSON standards RFC 8259 and ECMA-404 state that JSON text exchanged between systems should use utf-8 to be interoperable, keeping output consistent no matter input encoding.

5. Encoding handling\
    As it is hard to reliably guess a file's encoding, the encoding for the input csv file is explicitly given as a parameter (default is "utf-8") through read_file, parse_csv, and write_json_file. The caller is therefore responsible for knowing the correct encoding. For some encodings, if it is incompatible with the file's bytes, a UnicodeDecodeError is raised (see test_read_file_æøå_ascii in test_parser.py). This is not the case for some other encodings such as EBCDIC.

6. Error handling\
    In parse_header, a ValueError is raised if header keys are not unique as dictionaries cannot have duplicate keys (the values will get overwritten).
    In parse_csv_line, a ValueError is raised if there is not the same amount of fields in the header and the rows, adhering to the RFC 4180 standard of equal number of fields in all lines.
    In my_split, a ValueError is raised if a field contains unbalanced quotation marks by detecting that the boolean outer_quotations is still true after the while loop iterating through each character in the line.

---------------------------------------------------

**UML diagram:**



