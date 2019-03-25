try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import json
import glob


def get_contests(election):
    simplified_contests = [{"title": c['title'], "answers": [a['name'] for a in c['candidates']]} for c in election['contests']]

    return simplified_contests

def convert_ballot_image(contests, image):
    raw_ballot = pytesseract.image_to_string(image)

    position = 0
    result = []

    # expecting ballot with contest title, newline, voter choice
    lines = raw_ballot.split("\n")
    for line_num in range(len(lines)):
        line = lines[line_num]
        if line == contests[position]['title']:
            option = lines[line_num+1]
            result.append(option)
            position += 1

        if position >= len(contests):
            if len(result) == len(contests):
                return result
            else:
                # invalid ballot / ballot not read
                return None
    
def process_directory(contests, directory_path):
    files = glob.glob(directory_path + "/*.jpg")
    # Simple image to string
    for f in files:
        convert_ballot_image(contests, Image.open(f))
        print("\n\n")

        
def main():
    election = json.loads(open("./election.json", "r").read())
    contests = get_contests(election)
    process_directory(contests, "./ballots/batch-1")

if __name__ == "__main__":
    main()


        
