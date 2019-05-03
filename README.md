Scanner
=======

Scanner processes image files (typically jpegs) into cast vote records
(CVRs) with the help of an election definition file (election.json).

# Install

* install Python3 and `pipenv`

* Install `zbar`

```
sudo apt install libzbar0
```

* install SANE

```
sudo apt install sane sane-utils libsane-extras xsane
```

* Set up your environment and install required packages

```
pipenv
pipenv install
```

* Process scanned ballots, expected to be JPEGs

```
pipenv shell
python -m scanner.core <election.json> <directory_of_jpegs>
```

It will take a little while to process the ballots, and there is
currently no progress update, but eventually you'll get a CSV dump of
the processed ballots.

