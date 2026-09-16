import unittest
import parser
from unittest.mock import mock_open, patch

class TestParser(unittest.TestCase): #Inherit from unittest.TestCase

    # Run before and after every test case
    def setUp(self):
        pass

    def tearDown(self):
        pass

    
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


#!!!!!!!!!!!!!!!!!!IKKE LIGE ANTAL RÆKKER OG KOLONNER (implementeres i write_json_file)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Skal korte rækker paddes med tomme strenge, skal det give en fejl, eller er det ok at det crasher som nu? 


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

    #FAIL
    def test_parse_csv_fields_containing_commas(self):
        csv_data="name,email, address, department\nAlice Smith,as@gmail.com, Nørregade 5, 2. sal, Engineering\n" 
        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file: 
            result = parser.parse_csv("test.csv")
        expected = [
            ["name", "email", "address", "department"],
            ["Alice Smith", "as@gmail.com", "Nørregade 5, 2. sal", "Engineering"]
        ]
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("test.csv", encoding="utf-8")


#----------------------




               

if __name__ == '__main__':
    unittest.main()
