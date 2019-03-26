
import unittest.mock

import scanner.core
import json

def get_test_election():
    election_json = open("./election.json","r").read()
    return json.loads(election_json)

def test_get_contests():
    election = get_test_election()
    contests = scanner.core.get_contests(election)
    
    assert len(contests) == len(election["contests"])
    assert contests[0]["title"] == election["contests"][0]["title"]

@unittest.mock.patch('pytesseract.image_to_string')
def test_convert_ballot_image(image_to_string):
    # ballot with some typos
    image_to_string.return_value = 'Democratic Nominee for the 2020 Presidential Election\nKamala Harrs / Senator\n\nSelect your preferred dessert\nPi'
    
    election = get_test_election()
    contests = scanner.core.get_contests(election)
    
    result = scanner.core.convert_ballot_image(contests, None)

    assert image_to_string.called
    assert result == ['Kamala Harris', 'Pie']

@unittest.mock.patch('pytesseract.image_to_string')
def test_bad_ballot_convert_ballot_image(image_to_string):
    image_to_string.return_value = 'Select your preferred dessert\nPie'
    
    election = get_test_election()
    contests = scanner.core.get_contests(election)
    
    result = scanner.core.convert_ballot_image(contests, None)

    assert image_to_string.called
    assert result is None
    
@unittest.mock.patch('scanner.core.convert_ballot_image')
def test_process_directory(convert_ballot_image):
    election = get_test_election()
    contests = scanner.core.get_contests(election)

    scanner.core.process_directory(contests, "./ballots/batch-1")

    assert convert_ballot_image.called
