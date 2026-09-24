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
    python -m coverage run -m unittest discover
    python -m coverage report -m
```
---------------------------------------------------

**Description of the software architecture:**\
The project consists of five functions used in different stages from reading the file (Unicode string) to splitting it into raw fields to converting these to dictionaries to converting this to a list of dictionaries and then writing this to a JSON file:

1. Loading\
    read_file(file_path, encoding) opens the file, reads it, and returns its full content as one decoded string. This is the only place that reads and decodes an input file, isolating the reading logic and encoding parameter. Therefore every other function only works with already decoded Unicode strings, and not raw bytes.

2. Parsing\
    my_split(line) splits one line into raw field strings. It scans the line character by character and uses a boolean (outer_quotations) to track whether the current position is inside a quoted field, deciding whether to split on a comma or append the character to the current field.

3. Internal data structure\
    parse_header turns the first line in a csv file into a list of header keys and raises ValueError on duplicates. 
    parse_csv_line maps the fields of one row onto these keys from parse_header, producing one dictionary per row. It takes a header as an optional argument as not all csv files contain a header.
    parse_csv calls read_file and splits the file's rows where it treats the first line as the header, calling parse_header, and calls parse_csv_line on the remaining lines. Then it collects the results into a list of dictionaries.

4. JSON export\
    write_json_file(file, encoding) calls parse_csv, producing a list of dictionaries. This is serialized to JSON-formatted strings in a .json file using json.dump, with ensure_ascii=False so special characters (æ, ø, å) are preserved rather than showing \uXXXX escapes. The output file is always written as UTF-8, regardless of which encoding the input CSV was read with.

5. Encoding handling\
    As it is hard to reliably guess a file's encoding, the encoding for the input csv file can optionally be given as a parameter (default is "utf-8") to read_file, parse_csv, and write_json_file. For some encodings, if the encoding is incompatible with the file's bytes, a UnicodeDecodeError is raised (see test_read_file_æøå_ascii in test_parser.py). This is not the case for some other encodings such as EBCDIC.

6. Error handling\
    In parse_header, a ValueError is raised if header keys are not unique as dictionaries cannot have duplicate keys (the values will get overwritten).
    In parse_csv_line, a ValueError is raised if there is not the same amount of fields in the header and the rows, adhering to the RFC 4180 standard of equal number of fields in all lines.
    In my_split, a ValueError is raised if a field contains unbalanced quotation marks by detecting that the boolean outer_quotations is still true after the while loop iterating through each character in the line.

---------------------------------------------------

**UML diagram:**\
Program starts by calling write_json_file(file), which calls parse_csv(file) which calls read_file to read the contents of the file, generating a long string which is split into a list of lines using splitlines(). 
if the file is empty, parse_csv returns an empty list [] which is written to a JSON file through write_json_file. 
Otherwise, the first line is parsed as the header, using my_split and parse_header, checking if the header fields are unique. If duplicate fields exist, ValueError is raised.
Otherwise we enter a loop, looping over the remaining lines with parse_csv_line, calling my_split that splits each line into fields. Parse_csv_line checks that the header and rows have the same amount of fields. If they don't, a ValueError is raised. Otherwise, the keys in the header and the values in the row are mapped into a dictionary, which is added to a list of dicitonaries.
When we have been through all lines, parse_csv returns the list of dictionaries to write_json_file that writes these to a JSON file.


![alt text](<activity diagram - parser.drawio (5).png>)