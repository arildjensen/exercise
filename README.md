# Exercise

## Overview
This repository contains the code of an exercise to build a script to collect metrics from a running Docker container and write the data to a local file in either json or cvs format at a specified frequency.

## Files
* run.py -- the main script
* requirements.txt -- PIP packages required
* config.json -- Configuration settings used by the main script
* Dockerfile -- Used to create a custom nginx image
* README.md -- This file
* metrics -- Automatically created by the script. This is the default output file name and can be changed

## Installation
It is assumed you have Python 3 and Docker Desktop already installed.

Add the required packaged
```sh
pip -r requirements.txt
```

Create the Docker image
```sh
cd ~/git/exercise
docker build -t mynginx .
```

Start the Docker container using Docker Desktop

Start the script
```sh
cd ~/git/exercise
python3 run.py
```

## Future Improvements
* The csv output was not implemented but can easily be done given some more time
* A bug was encountered during development where the Docker API stopped working silently in the script during execution but always started working again with a new terminal session. This needs to be investigated further.
* Better input sanitation, such as no empty input or special characters.
* Some code cleanup for readability, variable management, etc.
* More more functions to limit repeat code blocks