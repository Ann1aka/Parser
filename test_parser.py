import unittest
import parser
import json
from unittest.mock import mock_open, patch
import tempfile, os

class TestParser(unittest.TestCase): #Inherit from unittest.TestCase
    #Test cases for parse_csv function
    
    def test_parse_csv(self):
        csv_data="name,email,department\nAlice Smith,as@gmail.com,Engineering\n" #simulate contents of a csv file
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file: #mock the open-function with a fake temporary one. The fake file contains "data"
            result = parser.parse_csv("test.csv") #Open "fake" file test.csv, but gets file contents from csv_data

        expected = [
            {"name": "Alice Smith", "email": "as@gmail.com", "department": "Engineering"}
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8") #Check that you use the correct path and encoding

    def test_parse_csv_special_characters_ÆØÅ(self):
        csv_data="name,email,department\nÆå Smith,as@gmail.com,Ingeniør\n" #simulate contents of a csv file
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file: #mock the open-function with a fake temporary one. The fake file contains "data"
            result = parser.parse_csv("test.csv", encoding="ascii")

        expected = [
            {"name": "Æå Smith", "email": "as@gmail.com", "department": "Ingeniør"}
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="ascii") 


    #test for empty csv file
    def test_parse_csv_empty_csv(self):
        with patch("builtins.open", mock_open(read_data="")):
            result = parser.parse_csv("empty.csv")     
        self.assertEqual(result, [])


    def test_parse_csv_trailing_empty_line(self):
        csv_data="name,email,department\nAlice Smith,as@gmail.com,Engineering\n\n" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv", encoding ="utf-8")

        expected = [
            {"name": "Alice Smith", "email": "as@gmail.com", "department":"Engineering"}
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8")



    def test_parse_csv_trailing_whitespace_part_of_field(self):
        csv_data=" name,email ,department\nAlice Smith, as@gmail.com,Engineering\n" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = [
            {" name": "Alice Smith", "email ": " as@gmail.com", "department":"Engineering"}
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8") 

    def test_parse_csv_only_header(self):
        csv_data = "name,email,department\n"
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = []
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8")



    #Tests that readlines() handles last line without newline correctly
    def test_parse_csv_one_line(self):
        csv_data="name,email,department\nAlice Smith,as@gmail.com,Engineering" #no \n at the end
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = [
            {"name": "Alice Smith", "email": "as@gmail.com", "department": "Engineering"}
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8")


    def test_parse_csv_line_with_only_whitespace(self):
        csv_data=" \n" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = []
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8") 

    def test_parse_csv_empty_fields(self):
        csv_data="name,email,department\n,,\n" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = [
            {"name": "", "email": "", "department": ""}
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8") 


    def test_parse_csv_unterminated_quoted_field(self):
        csv_data = 'name,comment\nAlice,"unterminated\n'
        with patch("builtins.open", mock_open(read_data=csv_data)):
            with self.assertRaises(ValueError):
                parser.parse_csv("test.csv")



    def test_parse_csv_crlf_line_endings(self):
        csv_data = "name,email,department\r\nAlice Smith,as@gmail.com,Engineering\r\nBob,bob@gmail.com,HR"
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = [
            {"name": "Alice Smith", "email": "as@gmail.com", "department": "Engineering"},
            {"name": "Bob", "email": "bob@gmail.com", "department": "HR"}
        ]
        self.assertEqual(result, expected)


    def test_parse_csv_fields_containing_commas(self):
        csv_data="name,email,address,department\nAlice Smith,as@gmail.com,\"Nørregade 5, 2. sal\",Engineering\n" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file: 
            result = parser.parse_csv("test.csv")
        expected = [
            {"name":"Alice Smith", "email":"as@gmail.com", "address":"Nørregade 5, 2. sal", "department":"Engineering"}
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8")


# #----------------------------------------------------------------------------

#Test cases for write_json_file function

    def test_write_json_file_opened_correctly_and_data_written_to_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            with open(csv_path, "w", encoding="utf-8") as f:
                f.write("name,email,department\nAlice Smith,as@gmail.com,Engineering\n")

            result = parser.write_json_file(csv_path)

            with open(result, encoding="utf-8") as f:
                written_data = json.load(f)

        self.assertEqual(written_data, [{"name": "Alice Smith", "email": "as@gmail.com", "department": "Engineering"}])
        self.assertEqual(result, csv_path.replace(".csv", ".json"))



    def test_write_json_file_ÆØÅ(self):
        #Write a real csv file to a temp-directory, run write_json_file on it, and read the result back.
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            with open(csv_path, "w", encoding="utf-8") as f:
                f.write("name,email,department\nÅge Sæby,as@gmail.com,Ingeniør\n")

            result = parser.write_json_file(csv_path)

            with open(result, encoding="utf-8") as f:
                written_data = json.load(f)

        self.assertEqual(written_data, [{"name": "Åge Sæby", "email": "as@gmail.com", "department": "Ingeniør"}])
        self.assertEqual(result, csv_path.replace(".csv", ".json"))

#---------------------------------------------

#Test cases for parse_header

    def test_parse_header(self):
        header = "name,email,department,role\r\n"
        expected = ["name","email","department","role"]
        result = parser.parse_header(header)
        self.assertEqual(expected, result)


    def test_parse_header_empty_header(self):
        header = "" #Header that is an empty string
        expected = [""] #an array with an empty string.
        result = parser.parse_header(header)
        self.assertEqual(expected, result)

    def test_parse_header_duplicate_header(self):
        with self.assertRaises(ValueError):
            parser.parse_header("name,name,department,role\r\n")

#-----------------------------------------------------------

#Test cases for parse_csv_line

    def test_parse_csv_line_with_header(self):
        result = parser.parse_csv_line("a,a@email,engineering,engineer",parser.parse_header("name,mail,dept,role"))
        expected = {'name': 'a', 'mail': 'a@email', 'dept': 'engineering', 'role': 'engineer'}
        self.assertEqual(expected,result)

    def test_parse_csv_line_no_header(self):
        result = parser.parse_csv_line("a,a@email,engineering,engineer")
        expected = {0: 'a', 1: 'a@email', 2: 'engineering', 3: 'engineer'}
        self.assertEqual(expected,result)

    def test_parse_csv_line_unequal_header_and_columns1(self):
        json_path = "test.json"
        with patch("builtins.open", mock_open()) as mock_file:
            with self.assertRaises(ValueError):
                parser.parse_csv_line("Alice Smith, AS@gmail.com", "name")

    def test_parse_csv_line_unequal_header_and_columns2(self):
        json_path = "test.json"
        with patch("builtins.open", mock_open()) as mock_file:
            with self.assertRaises(ValueError):
                parser.parse_csv_line("Alice Smith", "name, email, department")



#-----------------------------------------------------------------

#Test cases for my_split

    def test_my_split_quoted_and_empty_fields(self):
        example_string = "John,\"Johnny\",28,"",engineer"
        expected = ["John","Johnny", "28","", "engineer"]
        result = parser.my_split(example_string)
        self.assertEqual(expected, result)

    def test_my_split_comma_in_quoted_fields(self):
        example_string = "\"Smith, John\",28,engineer"
        expected = ["Smith, John", "28", "engineer"]
        result = parser.my_split(example_string)
        self.assertEqual(expected, result)

    def test_my_split_multiple_comma_in_quoted_fields(self):
        example_string = "\"Smith, John, 28\",engineer"
        expected = ["Smith, John, 28", "engineer"]
        result = parser.my_split(example_string)
        self.assertEqual(expected, result)

    def test_my_split_double_quoted_fields(self):
        example_string = 'aa,"b""bb",cc'
        expected = ['aa','b"bb','cc']
        result = parser.my_split(example_string)
        self.assertEqual(expected, result)

    def test_my_split_tripple_quoted_fields(self):
        example_string = 'aa,"""b,b""",cc'
        expected = ['aa','"b,b"','cc']
        result = parser.my_split(example_string)
        self.assertEqual(expected, result)

    def test_my_split_quotation_at_the_end(self):
        example_string = 'aa,"""k"'
        expected = ['aa','"k']
        result = parser.my_split(example_string)
        self.assertEqual(expected, result)

    def test_my_split_newline_in_quoted_field(self):
        example_string = 'aa,"b\nb",cc'
        expected = ['aa','b\nb','cc']
        result = parser.my_split(example_string)
        self.assertEqual(expected, result)

    def test_my_split_unterminated_quoted_field(self):
        example_string = 'aa, "b, cc'
        with self.assertRaises(ValueError):
            parser.my_split(example_string)

    def test_my_split_unterminated_quoted_field2(self):
        example_string = 'aa, " b"", cc'
        with self.assertRaises(ValueError):
            parser.my_split(example_string)

    def test_my_split_unterminated_quoted_field3(self):
        example_string = 'aa, "" b", cc'
        with self.assertRaises(ValueError):
            parser.my_split(example_string)
        

#----------------------------------------------------------------------

#Test cases for read_file

    def test_read_file_utf8(self):
        csv_data = "name,email,department\n"
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.read_file("test.csv")

        expected = "name,email,department\n"
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8")

    def test_read_file_ascii(self):
        csv_data = "name,email,department\n"
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.read_file("test.csv", encoding="ascii")

        expected = "name,email,department\n"
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="ascii")

    def test_read_file_empty(self):
        with patch("builtins.open", mock_open(read_data="")) as mock_file:
            result = parser.read_file("test.csv", encoding="ascii") #returns empty string

        expected ="" 
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="ascii")


    def test_read_file_æøå_ascii(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            with open(csv_path, "w", encoding="utf-8") as f:
                f.write("æøå\n")

            with self.assertRaises(UnicodeDecodeError):
                parser.read_file(csv_path, encoding = "ascii")


    def test_read_file_æøå_utf8(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            with open(csv_path, "w", encoding="utf-8") as f:
                f.write("æøå\n")

            result = parser.read_file(csv_path, encoding = "utf-8")

        expected = "æøå\n"

        self.assertEqual(expected, result)






if __name__ == '__main__':
    unittest.main()
