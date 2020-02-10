import getopt, sys
import os
from parse import extractQuestions, makeAnki
import pandas as pd

argumentList = sys.argv[1:]

try:
    opts, args = getopt.getopt(argumentList, "vrs:c:", ["verbose", "representative", "section=", "to_csv="])
except getopt.error as err:
    print(str(err))
    sys.exit(2)

verbose = False
question_filter = None
csv_file = None

for o, a in opts:
    if o == "-v" or o == "--verbose":
        verbose = True
    if o == "-r" or o == "--representative":
        question_filter = "Mquestion"
    if o == "-c" or o == "--to_csv=":
        csv_file = a

files = args

questions = pd.DataFrame()

if verbose:
    if question_filter is not None:
        print("Generating anki deck using custom filter " + question_filter)
    print("Importing files:\n")

for file_name in files:
    if verbose:
        print(file_name)

    file_questions = extractQuestions(file_name, question_filter)
    questions = questions.append(file_questions, ignore_index=True)

if verbose:
    print(questions)
    print("Generated " + str(len(questions)) + " questions from " + str(len(files)) + " files.")

# Generate either a csv file or an Anki deck
if csv_file:
    questions.to_csv(os.path.abspath(csv_file))
else:
    makeAnki(questions, "CLP2")
