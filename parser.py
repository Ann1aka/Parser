import json
import csv

file_path1 = "employees.csv"
file_path2 = "sogne.csv"

files =[file_path1, file_path2]


def parse_csv(file_path):
    """
    Read the CSV file and return an array of arrays (list of lists) 
    where each inner array is a row in the CSV file
    """
    array_of_rows = []
    with open(file_path, encoding ="utf-8") as f:
        for row in f.readlines(): #read multiple lines at a time
            new_row = row.strip().split(",")
            if (new_row == [""]):
                continue
            array_of_rows.append(new_row) #strip for \n and whitespaces and then Split the row into individual items with comma delimiter
    return array_of_rows #array of arrays




def write_json_file(data_list, json_path): 
    """
    Takes in an array of arrays and a path to write the json file to and returns a json file
    with the first row of the array as the keys and the rest of the rows as values in a list of dictionaries
    """
    data_list_keys = data_list[0] #get the first row/arry of the data_list (array of arrays) as keys for the json object
    result_list = []
    for row in data_list[1:]: #skip first row/array and iterate through the rest of the arrays in the list of arrays
        json_objects = {} #empty dictionary
        for i in range(len(data_list_keys)): #iterate for as long as there are keys
            json_objects[data_list_keys[i]] = row[i] #assign the key of the current index to the value of the current index in the row
        result_list.append(json_objects) #append the json object to the result list to get a list of dictionaries

    # Write the list of dictionaries to a json file with an array of json objects with indentation for readability
    with open(json_path, "w", encoding ="utf-8") as final:
        json.dump(result_list, final, indent=2)
        return json_path


if __name__ == "__main__":
    for file in files:
        write_json_file(parse_csv(file), file.replace(".csv", ".json"))





