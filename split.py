import pandas as pd
import re

# open the file and read through it line by line
fh = open('Problem-Files/prob_s1.1.tex').read()

questions = []

contents = re.split(r"\\begin{question}.*\n", fh)
# contents.pop(0)
# print(contents)

for i in contents:
    questions_dict = {}

    prompt = re.search(r"(?P<prompt>.*?)\\end{question}", i, re.S)
    if prompt is not None:
        prompt_str = prompt.group("prompt")
    else:
        prompt_str = None

    questions_dict["question"] = prompt_str

    solution = re.search(r"\\begin{solution}(?P<solution>.*?)\\end{solution}", i, re.S)
    if solution is not None:
        solution_str = solution.group("solution")
    else:
        solution_str = None

    questions_dict["solution"] = solution_str

    questions.append(questions_dict)

questions_df = pd.DataFrame(questions)
print(questions_df)
