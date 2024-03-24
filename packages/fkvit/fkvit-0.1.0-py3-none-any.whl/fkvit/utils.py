import pkg_resources

def path_convertor(path):
        try:
            return pkg_resources.resource_filename('fkvit', path)
        except FileNotFoundError and ModuleNotFoundError:
            return path
        
INSTRUCTIONS = """
I am going to pass you a long string with MCQ questions. Your job is so identify the questions and respond in a very specific format which is as follows: 

'{question number} {correct option} {answer text}'

Here is are few examples:

Q1. B) Waltuh

Note: In case you cannot identify the questions, you can respond with "Please paste the questions again."

Your questions are as follows:
"""

JSON_FILE = pkg_resources.resource_filename('fkvit', 'assets/data.json')