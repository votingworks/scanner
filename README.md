Scanner
=======

Scanner processes image files (typically jpegs) into cast vote records
(CVRs) with the help of an election definition file (election.json).

This scanner works on Linux

# Install Linux Scanning

```
sudo apt install sane sane-utils libsane-extras xsane
```

Install Canon DR-C225 drivers

```
wget http://downloads.canon.com/bisg2015/software/scanners/C225_W_LINUX_V10.zip
unzip C225_W_LINUX_V10.zip
sudo dpkg -i cndrvsane-drc225-1.00-2_i386.deb
```

# Install Application Packages

```
yarn install
```

* Process scanned ballots, expected to be JPEGs

```
yarn start
```


