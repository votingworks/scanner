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
    return election["contests"]

def convert_ballot_image(contests, image):
    raw_ballot = pytesseract.image_to_string(image)

    position = 0
    current_contest = contests[position]
    
    result = {}

    # expecting ballot with contest title, newline, voter choice
    lines = raw_ballot.split("\n")
    for line_num in range(len(lines)):
        line = lines[line_num]
        if stringdist.levenshtein(line, current_contest['title']) < (len(current_contest['title'])/4):
            voter_selection = lines[line_num+1]

            # remove party affiliation if it exists
            voter_selection = voter_selection.split(" / ")[0]
            
            # include "[no selection]" as an option
            candidates = current_contest["candidates"]
            candidates += [{"id": None, "name": "[no selection]"}]

            # match option against candidates using min Levenshtein distance
            distances = [(candidate, stringdist.levenshtein(voter_selection, candidate["name"])) for candidate in candidates]
            the_answer = min(distances, key = lambda a: a[1])

            result[current_contest['id']] = the_answer[0]['id']
            
            position += 1

            if position >= len(contests):
                break

            current_contest = contests[position]


    if len(result.items()) == len(contests):
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
        # crop image to not include 20% of header and 9% of footer
        image = Image.open(f)
        cropped_image = image.crop(box=(0, image.height/5, image.width, image.height*91/100))
        
        one_ballot = convert_ballot_image(contests, cropped_image)
        if one_ballot:
            one_ballot['file'] = f
            result += json.dumps(one_ballot) + "\n"
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


        
