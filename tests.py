# tests.py

import unittest
# from functions.get_files_info import get_files_info
# from functions.get_file_content import get_file_content, MAX_CHARS
# from functions.write_file import write_file
from functions.run_python import run_python_file

class TestGetFilesInfo(unittest.TestCase):
#     def test_case1(self):
#         result = get_files_info("calculator", ".")
#         print(result)
#         answer = """- main.py: file_size=575 bytes, is_dir=False
# - tests.py: file_size=1342 bytes, is_dir=False
# - pkg: file_size=4096 bytes, is_dir=True"""
#         self.assertEqual(result, answer)

#     def test_case2(self):
#         result = get_files_info("calculator", "pkg")
#         print(result)
#         answer = """- __pycache__: file_size=4096 bytes, is_dir=True
# - calculator.py: file_size=1746 bytes, is_dir=False
# - render.py: file_size=766 bytes, is_dir=False"""
#         self.assertEqual(result, answer)

#     def test_case3(self):
#         result = get_files_info("calculator", "/bin")
#         print(result)
#         answer = """Error: Cannot list "/bin" as it is outside the permitted working directory"""  
#         self.assertEqual(result, answer)

#     def test_case4(self):
#         result = get_files_info("calculator", "../")
#         print(result)
#         answer = """Error: Cannot list "../" as it is outside the permitted working directory"""
#         self.assertEqual(result, answer)

    # def test_case5(self):
    #     result = get_file_content("calculator", "lorem.txt")
    #     print(result)
    #     self.assertEqual(len(result), MAX_CHARS)

    # def test_case6(self):
    #     result = get_file_content("calculator", "main.py")
    #     print(result)
    #     self.assertIn("def main():", result)

    # def test_case7(self):
    #     result = get_file_content("calculator", "pkg/calculator.py")
    #     print(result)
    #     self.assertIn("def _apply_operator(self, operators, values)", result)

    # def test_case8(self):
    #     result = get_file_content("calculator", "/bin/cat")
    #     print(result)
    #     self.assertIn("Error: Cannot read", result)

    # def test_case9(self):
    #     result = get_file_content("calculator", "pkg/does_not_exist.py")
    #     print(result)
    #     self.assertIn("Error: File not found", result)

    # def test_case10(self):
    #     result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    #     print(result)
    #     self.assertIn("28 characters written", result)
    
    # def test_case11(self):
    #     result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    #     print(result)
    #     self.assertIn("26 characters written", result)

    # def test_case12(self):
    #     result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    #     print(result)
    #     self.assertIn("Error:", result)

    def test_case_13(self):
        result = run_python_file("calculator", "main.py") 
        print(result)
        # (should print the calculator's usage instructions)

    def test_case_14(self):
        result = run_python_file("calculator", "tests.py") 
        print(result)
        # (should run the tests and print results)
    def test_case_15(self):
        result = run_python_file("calculator", "../main.py") 
        print(result)
        # (should return an error about running outside the working directory) 
    def test_case_16(self):
        result = run_python_file("calculator", "nonexistent.py") 
        print(result)
        # (should return an error about the file not being found)

if __name__ == "__main__":
    unittest.main()
