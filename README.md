Scanner
=======

Scanner processes image files (typically jpegs) into cast vote records
(CVRs) with the help of an election definition file (election.json).

# Install

* install Python3 and `pipenv`

* Set up your environment and install required packages

```
pipenv
pipenv install -r requirements.txt
```

* Process scanned ballots, expected to be JPEGs

```
python -m scanner.core <election.json> <directory_of_jpegs>
```
