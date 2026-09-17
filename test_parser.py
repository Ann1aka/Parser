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
            ["name", "email", "department"],
            ["Alice Smith", "as@gmail.com", "Engineering"]
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8") #Check that you use the correct path and encoding

    def test_parse_csv_special_characters_ÆØÅ(self):
        csv_data="name,email,department\nÆå Smith,as@gmail.com,Ingeniør\n" #simulate contents of a csv file
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file: #mock the open-function with a fake temporary one. The fake file contains "data"
            result = parser.parse_csv("test.csv")

        expected = [
            ["name", "email", "department"],
            ["Æå Smith", "as@gmail.com", "Ingeniør"]
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8") 


    #test for empty csv file
    def test_parse_csv_empty_csv(self):
        with patch("builtins.open", mock_open(read_data="")):
            result = parser.parse_csv("empty.csv")     
        self.assertEqual(result, [])



    def test_parse_csv_unequal_headers_and_columns1(self):
        csv_data="name\nAlice Smith,as@gmail.com\n" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = [
            ["name"],
            ["Alice Smith", "as@gmail.com"]
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8")


    def test_parse_csv_unequal_headers_and_columns2(self):
        csv_data="name,email,department\nAlice Smith,as@gmail.com\n" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = [
            ["name", "email", "department"],
            ["Alice Smith", "as@gmail.com"]
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8") 


    def test_parse_csv_trailing_empty_line(self):
        csv_data="name,email,department\nAlice Smith,as@gmail.com,Engineering\n\n" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = [
            ["name", "email", "department"],
            ["Alice Smith", "as@gmail.com", "Engineering"]
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8")

    def test_parse_csv_trailing_whitespace_part_of_field(self):
        csv_data=" name,email , department\nAlice Smith,as@gmail.com ,Engineering\n" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = [
            [" name", "email ", " department"],
            ["Alice Smith", "as@gmail.com ", "Engineering"]
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8") 

    #Tests that readlines() handles last line without newline correctly
    def test_parse_csv_one_line(self):
        csv_data=" name,email , department" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = [
            [" name", "email ", " department"]
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8") 

    def test_parse_csv_line_with_only_whitespace(self):
        csv_data=" \n" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = [
            [" "]
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8") 

    def test_parse_csv_empty_fields(self):
        csv_data="name,email,department\n,,\n" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            result = parser.parse_csv("test.csv")

        expected = [
            ["name", "email", "department"],
            ["","",""]
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8") 
    


#----------------------------------------------------------------------------

#Test cases for write_json_file function

    def test_write_json_file_opened_correctly_and_data_written_to_json(self):
        data_list = [
            ["name", "email", "department"],
            ["Alice Smith", "as@gmail.com", "Engineering"],
            ["John Smith", "js@gmail.com", "Marketing"]]

        #Write to a real file in temp-directory and read it.
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = os.path.join(tmpdir, "test.json")
            result = parser.write_json_file(data_list, json_path)

            with open(json_path, encoding="utf-8") as f:
                written_data = json.load(f)

        self.assertEqual(written_data, [{"name": "Alice Smith", "email": "as@gmail.com", "department": "Engineering"}, 
                                        {"name": "John Smith", "email": "js@gmail.com", "department": "Marketing"}])
        self.assertEqual(result, json_path)

    def test_write_json_file_ÆØÅ(self):
        data_list = [
            ["name", "email", "department"],
            ["Åge Sæby", "as@gmail.com", "Ingeniør"]]

        #Write to a real file in temp-directory and read it.
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = os.path.join(tmpdir, "test.json")
            result = parser.write_json_file(data_list, json_path)

            with open(json_path, encoding="utf-8") as f:
                written_data = json.load(f)

        self.assertEqual(written_data, [{"name": "Åge Sæby", "email": "as@gmail.com", "department": "Ingeniør"}])
        self.assertEqual(result, json_path)



#Test that an exception is raised when given unequal header and row
    def test_write_json_file_unequal_headers_and_columns_raises1(self):
        data_list = [
            ["name"],
            ["Alice Smith", "as@gmail.com"]]

        json_path = "test.json"

        with patch("builtins.open", mock_open()) as mock_file:
            with self.assertRaises(ValueError):
                parser.write_json_file(data_list, json_path)


    def test_write_json_file_unequal_headers_and_columns_raises2(self):
        data_list = [
            ["name", "email", "department"],
            ["Alice Smith"]]

        json_path = "test.json"

        with patch("builtins.open", mock_open()) as mock_file:
            with self.assertRaises(ValueError):
                parser.write_json_file(data_list, json_path)


    def test_write_json_file_unequal_headers_and_columns_raises3(self):
        data_list = [
            ["name", "email", "department"],
            []]

        json_path = "test.json"

        with patch("builtins.open", mock_open()) as mock_file:
            with self.assertRaises(ValueError):
                parser.write_json_file(data_list, json_path)


    def test_write_json_file_empty_data_list_raises(self):
        data_list = []
        json_path = "test.json"

        with patch("builtins.open", mock_open()) as mock_file:
            with self.assertRaises(ValueError):
                parser.write_json_file(data_list, json_path)

            mock_file.assert_not_called()


    def test_write_json_file_duplicate_header(self):
        data_list = [
            ["name", "name", "department"],
            ["Alice Smith", "as@gmail.com", "engineering"]]
             #This input creates empty json array
        json_path = "test.json"

        with patch("builtins.open", mock_open()) as mock_file:
            with self.assertRaises(ValueError):
                parser.write_json_file(data_list, json_path)
        mock_file.assert_not_called()


    def test_write_json_file_only_header(self):
        data_list = [
            ["name", "email", "department"]
            ] #This input creates empty json array
        json_path = "test.json"
        #Write to a real file in temp-directory and read it.
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = os.path.join(tmpdir, "test.json")
            result = parser.write_json_file(data_list, json_path)

            with open(json_path, encoding="utf-8") as f:
                written_data = json.load(f)

        self.assertEqual(written_data, [])
        self.assertEqual(result, json_path)

if __name__ == '__main__':
    unittest.main()
