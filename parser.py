import json

file_path1 = "employees.csv"
file_path2 = "sogne.csv"



def my_split(line):
    """
    Takes a string as input and splits it on the comma-delimiter.
    Handles commas inside quoted fields, quoted fields, quotes inside of quoted fields, 
    as well as newlines inside of quoted fields
    Arg:
        line: a string corresponding to a row in a csv file
    Returns:
        A string list of fields, split on the comma-delimiter
    """
    outer_quotations = False
    result_list = []
    current_field ="" #accumulator
    i = 0
    while i < len(line):

        if outer_quotations == False:
            if line[i] ==",": #normal comma separator (not in quoted field)
                result_list.append(current_field.strip(",")) #remove comma and put it into result list
                current_field ="" #reset accumulator
            elif line[i] =='"':
                outer_quotations=True
            else: #normal character
                current_field = current_field+line[i]
        elif outer_quotations == True:
           # if i+1<len(line): #if there's still a next character
            if i+1<len(line) and line[i] =='"' and line[i+1] =='"': # inside double qoutation
                current_field = current_field+'"'
                i=i+2 #skip 2 characters because of the use of double quotes
                continue
            elif i+1<len(line) and line[i]=='"' and line[i+1] !='"': #end of quoted field
                outer_quotations = False
            elif line[i]=='"': #No i+1 exists, but there is a quote
                outer_quotations =False
            else: #normal character
                current_field = current_field+line[i]
        i=i+1
    if outer_quotations == True: #if outer_quotations is still true after exiting the loop, we have unmatched quotationmarks
       raise ValueError("Unterminated quoted field") 
    result_list.append(current_field)
    return result_list


def read_file(file_path, encoding='utf-8'):
    """
    Function that opens a file and returns it as a decoded string
    Arg:
        file_path: file path to the file that is to be read
        encoding: the text encoding to decode file with
    """
    with open (file_path, encoding = encoding) as f:
        return f.read() 


def parse_header(header_string):
    """
    Parses one CSV-header and outputs an array of strings
    Arg:
        header_string: A header which is a string
    Returns:
        An array of strings corresponding to the keys of the header
    """
    header_keys=my_split(header_string.rstrip("\r\n"))

    if len(set(header_keys)) != len(header_keys): #set(header_keys) contains only the unique elements of header_keys
        raise ValueError("Header contains duplicates")
    return header_keys



def parse_csv_line(CSV_line, header=None):
    """
    Parses one line in the CSV file.
    Args:
        CSV_line: a string which is a line in the CSV file
        header: a string array which is optionally given
    Returns:
        One dictionary of JSON objects
    """
    row_items = my_split(CSV_line.rstrip("\r\n")) #array of strings
    header_keys = []


    if header != None: #There is a header
        header_keys = header #array of strings, e.g. ["name", "age","role"]
        json_objects = {} #empty dictionary

        if len(header_keys) != len(row_items):
            raise ValueError("Unequal number of items in header and rows")
        else:
            for i in range(len(header_keys)):
                json_objects[header_keys[i]] = row_items[i]
            return json_objects
    else: #There is no header. Make keys: 0,1,2,...
        json_objects = {} #empty dictionary
        for i in range(len(row_items)):
            json_objects[i] = row_items[i]
        return json_objects


def parse_csv(file_path, encoding="utf-8"):
    """
    Reads and parses the CSV file and returns a list of dictionaries
    Arg:
        file_path: a file path to a csv file that is to be read
        encoding: the text encoding the csv file is written in
    Returns:
        A list of dictionaries
    """
    array_of_dict = []

    lines = read_file(file_path, encoding).splitlines() #read lines in file and return a list of lines with no additional line breaks. Splits blindly on newlines
    if lines == []: #check if string is empty
        return array_of_dict

    first_line = parse_header(lines[0]) #parse the header (first line)
    for line in lines[1:]: #parse the rest of the lines
        if line == "":
            continue
        parsed = parse_csv_line(line, first_line)
        array_of_dict.append(parsed)
    return array_of_dict
        


def write_json_file(file, encoding = "utf-8"):
    """
    Calls parse_csv to create a list of dictionaries and converts this to json strings that it writes to a json path
    Arg:
        file: the file path of the file to be parsed. This is also used for for the json file to be written to
        encoding: the text encoding the csv file is written in
    Returns:
        The filepath to the written JSON file
    """

    dict_array = parse_csv(file, encoding)
    json_path = file.replace(".csv", ".json")
    # Write the list of dictionaries to a json file with an array of json objects with indentation for readability
    with open(json_path, "w", encoding ="utf-8") as final:
        json.dump(dict_array, final, indent=2, ensure_ascii=False) # Ensure that "æ", "å", and "ø" are represented as utf-8 and not ascii
        return json_path


write_json_file(file_path1, encoding ="ascii")
write_json_file(file_path2, encoding = "utf-8")



