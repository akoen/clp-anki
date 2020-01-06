import pandas as pd
import sys
import re
import genanki

# open the file and read through it line by line
fh = open(sys.argv[1]).read()
# latex_header = open("header.tex").read()

questions = []

def extractQuestions(fileName):
    """
    extractQuestions - Extracts problems from a given CLP file.

    Parameter: fileName - the name of the file to use
    Returns: a pandas dataframe with the questions and soutions
    """
    contents = re.split(r"\\begin{M?question}", fh)

    for i in contents:
        questions_dict = {}

        prompt = re.search(r"(\[(?P<exam>.*?)\])?(\\label{(?P<label>[^\s]*)})?[\n\s](?P<prompt>[\s\S]*?)\n\\end{(?P<representative>M)?question}", i, re.S)
        
        if prompt is not None:
            prompt_str = '[latex]' + prompt.group("prompt") + '[/latex]'
            exam_str = prompt.group("exam")
            label_str = prompt.group("label")
            if prompt.group("representative") == "M":
                representative_str = "Yes"
            else:
                representative_str = "No"
        else:
            prompt_str = None
            exam_str = None
            label_str = None
            representative_str = None

        questions_dict["question"] = prompt_str
        questions_dict["exam"] = exam_str
        questions_dict["label"] = label_str
        questions_dict["representative"] = representative_str

        hint = re.search(r"\\begin{hint}(?P<hint>.*?)\\end{hint}", i, re.S)
        if hint is not None:
            hint_str = '[latex]' + hint.group("hint") + '[/latex]'
        else:
            hint_str = None

        questions_dict["hint"] = hint_str

        answer = re.search(r"\\begin{answer}[\n\s](?P<answer>.*?)\\end{answer}", i, re.S)
        if answer is not None:
            answer_str = '[latex]' + answer.group("answer") + '[/latex]'
        else:
            answer_str = None

        questions_dict["answer"] = answer_str

        solution = re.search(r"\\begin{solution}[\n\s](?P<solution>.*?)\\end{solution}", i, re.S)
        if solution is not None:
            solution_str = '[latex]' + solution.group("solution") + '[/latex]'
        else:
            solution_str = None

        questions_dict["solution"] = solution_str

        questions.append(questions_dict)

    questionsDF = pd.DataFrame(questions)
    return questionsDF

def makeAnki(questionsFrame, deckName):
    """
    makeAnki - generates an Anki deck from a given pandas dataframe.
    
    Parameter: questionsFrame - the data frame from which to build the deck.
    Parameter: deckName - the name of the deck to generate. 
    """

    question_notes = []

    question_model = genanki.Model(
        1831615823,
        'CLP-2 Question',
        fields = [
            {'name': 'Question'},
            {'name': 'Solution'},
        ],
        templates = [
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="solution">{{Solution}}',
            },
        ])

    question_deck = genanki.Deck(
        1211025408,
        deckName,
    )

    for i in range(len(questionsFrame)):
        print(questionsFrame.loc[i]["question"])

        if questionsFrame.loc[i]["question"] is not None:
            question_notes.append(genanki.Note(
                model = question_model,
                fields = [questionsFrame.loc[i]["question"], questionsFrame.loc[i]["solution"]]))

    for i in range(len(question_notes)):
        question_deck.add_note(question_notes[i])


    genanki.Package(question_deck).write_to_file('output.apkg')

questionsDF = extractQuestions(fh)
print(questionsDF["solution"])
makeAnki(questionsDF, "Test")
