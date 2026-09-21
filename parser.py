import json

file_path1 = "employees.csv"
file_path2 = "sogne.csv"

files =[file_path1, file_path2]



def my_split(line):
    """
    Takes a string as input and splits it on the comma-delimiter.
    Handles commas inside quoted fields

    """
    outer_quotations = False
    result_list = []
    current_field ="" #accumulator
    i =0
    while i < len(line):
        print("1")
        #current_field = current_field + line[i]
        if outer_quotations == False: #and line[i]==",":
            print("2")
            
            if line[i] ==",": #normal komma seperator (ikke i quotes)
                result_list.append(current_field.strip(","))
                current_field =""
            elif line[i] =='"':
                outer_quotations=True
            else: #almindeligt tegn
                current_field = current_field+line[i] #sker altid
        elif outer_quotations == True:
            print("4")
        
            if line[i] =='"' and line[i+1] =='"': # inside double qoutation
                print("6")
                current_field = current_field+'"'
                i=i+2
            elif line[i]=='"' and line[i+1] !='"': #end of quotation
                print("7")
                outer_quotations = False
            else: #almindeligt tegn
                current_field = current_field+line[i] #sker altid
                
        i=i+1
    result_list.append(current_field)
    return result_list


print(my_split("aa,\"b,bb\",cc"))


def parse_header(header_string):
    """
    Function that parses one CSV-header and outputs an array of strings
    :type: string
    :rtype: string array 
    """
    header_keys=my_split(header_string.rstrip("\r\n"))

    if len(set(header_keys)) != len(header_keys): #set(data_list_keys) contains only the unique elements of data_list_keys
        raise ValueError("Header contains duplicates")
    return header_keys



def parse_csv_line(CSV_line, header=None):
    """
    Function that parses one line in the CSV file. It takes one line from a CSV file and optionally a string for the header from parse_header
    :type CSV_line: string
    :type string: string
    :rtype: dict
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
    Read the CSV file and returns a list of dictionaries
    rtype: list of dictionaries
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
    Takes in an array of arrays and a path to write the json file to and returns a json file
    with the first row of the array as the keys and the rest of the rows as values in a list of dictionaries.
    returns the path to the json file
    """

    dict_array = parse_csv(file)
    json_path = file.replace(".csv", ".json")
    # Write the list of dictionaries to a json file with an array of json objects with indentation for readability
    with open(json_path, "w", encoding ="utf-8") as final:
        json.dump(dict_array, final, indent=2, ensure_ascii=False) #ensures that "æ", "å", and "ø" are represented as utf-8 and not ascii
        return json_path


#print(parse_header("name,email,department,role\n"))
#print(parse_csv_line("a,a@email,engineering,engineer",parse_header("name,mail,dept,role")))

#print(parse_csv(file_path1))



#write_json_file(file_path2)


# SPØRG: OK IKKE AT TAGE DETTE MED I TESTS?
# if __name__ == "__main__": # pragma: no cover
#     print(parse_header("employees.csv"))
    #for file in files:
    #    write_json_file(parse_csv(file), file.replace(".csv", ".json"))





