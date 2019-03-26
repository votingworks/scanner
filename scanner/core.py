try:
    from PIL import Image
except ImportError: # pragma: no cover
    import Image

import pytesseract
import json
import glob
import stringdist
import sys

def get_contests(election):
    simplified_contests = [{"title": c['title'], "answers": [a['name'] for a in c['candidates']]} for c in election['contests']]

    return simplified_contests

def convert_ballot_image(contests, image):
    raw_ballot = pytesseract.image_to_string(image)

    position = 0
    current_contest = contests[position]
    
    result = []

    # expecting ballot with contest title, newline, voter choice
    lines = raw_ballot.split("\n")
    for line_num in range(len(lines)):
        line = lines[line_num]
        if stringdist.levenshtein(line, current_contest['title']) < (len(current_contest['title'])/2):
            option = lines[line_num+1]

            # remove party affiliation
            option = option.split(" / ")[0]
            
            # include "[no selection]" as an option            
            answers_enumerated = list(enumerate(current_contest["answers"]))
            answers_enumerated.append((None, "[no selection]"))

            # match option against candidates using min Levenshtein distance
            distances = [(answer_num, answer, stringdist.levenshtein(option, answer)) for answer_num, answer in answers_enumerated]
            the_answer = min(distances, key = lambda a: a[2])
            result.append(the_answer[1])
            
            position += 1

            if position >= len(contests):
                break

            current_contest = contests[position]


    if len(result) == len(contests):
        return result
    else:
        # invalid ballot / ballot not read
        return None
    
def process_directory(contests, directory_path):
    files = glob.glob(directory_path + "/*.jpg")
    # Simple image to string
    result = ""
    failures = []
    for f in files:
        one_ballot = convert_ballot_image(contests, Image.open(f))
        if one_ballot:
            result += f + "," + ",".join(one_ballot) + "\n"
        else:
            failures.append(f)

    return result, failures

        
def main(): # pragma: no cover
    election = json.loads(open(sys.argv[1], "r").read())
    contests = get_contests(election)
    result, failures = process_directory(contests, sys.argv[2])

    print(result)

    print("\n\n")

    print(failures)

if __name__ == "__main__": # pragma: no cover
    main()


        
