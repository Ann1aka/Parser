

#Gennemløb teksten tegn for tegn og hold styr på: current field, current row, er jeg i quotes, alle færdige rækker.

file_path1 = r"C:\Users\SPAC-B-6\OneDrive - Specialisterne\Dokumenter\GitHub\Parser\employees.csv"

file_path2 = r"C:\Users\SPAC-B-6\OneDrive - Specialisterne\Dokumenter\GitHub\Parser\sogne.csv"




def read_data(file_path):
    array_of_rows = []
    with open(file_path) as f:
        first_row = f.readline() #Read one line at a time. This is the first row (header) of the file
        print(first_row)
        for row in f.readlines(): #Read multiple lines at a time
            array_of_rows.append(row.split(",")) #Split the row into individual items
    return array_of_rows
    #print(array_of_rows) #array of arrays

def transformList(data_list):

def write_json_file(data_list):

parse_csv(file_path1)




# split() the rows into individual items and get them transformed into a dictionary. 
# Every row could be it's own dictionary, so you'll actually want to store those in a list.

#Open file


#read rows in file
#check values
#open json file for writing
#write list of rows



