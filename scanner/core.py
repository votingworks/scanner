try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import json
import glob

election = json.loads(open("./election.json", "r").read())

simplified_contests = [{"title": c['title'], "answers": [a['name'] for a in c['candidates']]} for c in election['contests']]

print(simplified_contests)

# loop through ballots
files = glob.glob("./ballots/batch-1/*.jpg")

print(files)

# Simple image to string
for f in files:
    raw_ballot = pytesseract.image_to_string(Image.open(f))

    position = 0

    lines = raw_ballot.split("\n")
    for line_num in range(len(lines)):
        line = lines[line_num]
        if line == simplified_contests[position]['title']:
            option = lines[line_num+1]
            print(option)
            position += 1

        if position >= len(simplified_contests):
            break

    print("\n\n")
        
