import json

file_path1 = "employees.csv"
file_path2 = "sogne.csv"

files =[file_path1, file_path2]

def my_split(line):
    """
    Takes a string as input and splits it on the comma-delimiter.
    Handles commas inside quoted fields, quoted fields, quotes inside of quoted fields, 
    as well as newlines inside of quoted fields
    Arg:
        line: a string corresponding to a row in a csv file
    Returns:
        A string list of items, split on the comma-delimiter
    """
    outer_quotations = False
    result_list = []
    current_field ="" #accumulator
    i = 0
    while i < len(line):
        print("1")
        #current_field = current_field + line[i]
        if outer_quotations == False: #and line[i]==",":
            if line[i] ==",": #normal comma seperator (not in quoted field)
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
    result_list.append(current_field)
    return result_list

def parse_header(header_string):
    """
    Function that parses one CSV-header and outputs an array of strings
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
    Function that parses one line in the CSV file.
    Args:
        CSV_line: a string which is a line in the CSV file
        header: a string which is optionally
    Returns:
        One dictionary of JSON objects
    """
    row_items = my_split(CSV_line.rstrip("\r\n")) #arrray of strings
    header_keys = []


    if header != None: #There is a header
        header_keys = header #array of stringss ["name", "age","role"]
        json_objects = {} #empty dictionary

        if len(header_keys) != len(row_items):
            raise ValueError("Unequal number of items in header and rows")
        else:
            for i in range(len(header_keys)):
                json_objects[header_keys[i]] = row_items[i]
            return json_objects
    else: #There is no header. Make keys: 1,2,3,...
        json_objects = {} #empty dictionary
        for i in range(len(row_items)):
            json_objects[i] = row_items[i]
        return json_objects


def parse_csv(file_path):
    """
    Reads and parses the CSV file and returns a list of dictionaries
    Arg:
        file_path: a file path to a csv file that is to be read
    Returns:
        A list of dictionaries (array of arrays)
    """
    array_of_dict = []

    with open(file_path, encoding ="utf-8") as f:
        #seperate header and the rest of the lines
        first_line = parse_header(f.readline().strip("\r\n")) #read first line and parse it through parse_header 

        for lines in f.readlines():
            if lines.strip("\r\n") == "":
                continue
            parsed =parse_csv_line(lines, first_line)
            array_of_dict.append(parsed)
    return array_of_dict
        



def write_json_file(file):
    """
    Calls parse_csv to create a list of dictionaries and converts this to json strings that it writes to a json path
    Arg:
        file: the file path of the file to be parsed. This is also used for for the json file to be written to
    Returns:
        A json file
    """

    dict_array = parse_csv(file)
    json_path = file.replace(".csv", ".json")
    # Write the list of dictionaries to a json file with an array of json objects with indentation for readability
    with open(json_path, "w", encoding ="utf-8") as final:
        json.dump(dict_array, final, indent=2, ensure_ascii=False) # Ensure that "æ", "å", and "ø" are represented as utf-8 and not ascii
        return json_path


# if __name__ == "__main__": # pragma: no cover
#     print(parse_header("employees.csv"))
    #for file in files:
    #    write_json_file(parse_csv(file), file.replace(".csv", ".json"))





