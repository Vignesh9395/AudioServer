# Audio File Server - Simulation
## Overview

This Flask application demonstrates the functionalities of an audio server.

## How to Run

In the top-level directory:

```sh
$ python run.py
```

## Installation Instructions

Pull down the source code from this GitLab repository:

```sh
$ git clone https://github.com/Vignesh9395/AudioServer.git```
```

Create a new virtual environment:

```sh
$ cd AudioServer
$ python3 -m venv venv
```

Activate the virtual environment:

```sh
$ source venv/bin/activate
```

Install the python packages in requirements.txt:

```sh
(venv) $ pip install -r requirements.txt
```

Run development server to serve the Flask application:

```sh
(venv) $ python run.py
```

Navigate to 'http://localhost:9935/audioFileType/audioFileID' to use the endpoint!

create, read, upload, and delete endpoints for an audio file as defined
below:

### Create API:
The request will have the following fields:
- audioFileType – mandatory, one of the 3 audio types possible
- audioFileMetadata – mandatory, dictionary, contains the metadata for one
of the three audio files (song, podcast, audiobook)
### Delete API:
- The route will be in the following format:
“audioFileType/audioFileID”
### Update API:
- The route be in the following format: “audioFileType/audioFileID”
- The request body will be the same as the upload
### Get API:
- The route “audioFileType/audioFileID” will return the specific audio
file
- The route “audioFileType” will return all the audio files of that type

## MetaData
Audio file type can be one of the following:
1.  Song
2. Podcast
3. Audiobook
### Song file fields:
- ID – (mandatory, integer, unique)
- Name of the song – (mandatory, string, cannot be larger than 100
characters)
- Duration in number of seconds – (mandatory, integer, positive)
- Uploaded time – (mandatory, Datetime, cannot be in the past)
### Podcast file fields:
- ID – (mandatory, integer, unique)
- Name of the podcast – (mandatory, string, cannot be larger than 100
characters)
- Duration in number of seconds – (mandatory, integer, positive)
- Uploaded time – (mandatory, Datetime, cannot be in the past)
- Host – (mandatory, string, cannot be larger than 100 characters)
- Participants – (optional, list of strings, each string cannot be larger than
100 characters, maximum of 10 participants possible)
### Audiobook file fields:
- ID – (mandatory, integer, unique)
- Title of the audiobook – (mandatory, string, cannot be larger than 100
characters)
- Author of the title (mandatory, string, cannot be larger than 100
characters)
- Narrator - (mandatory, string, cannot be larger than 100 characters)
- Duration in number of seconds – (mandatory, integer, positive)
- Uploaded time – (mandatory, Datetime, cannot be in the past)

## Key Python Modules Used

* Flask: micro-framework for web application development
* pytest: framework for testing Python projects
* SQLAlchemy - ORM (Object Relational Mapper)

This application is written using Python 3+.

## Testing

To run the tests:

### Create Endpoint
```sh
(venv) $ cd tests/create
(venv) $ python -m pytest -v
```
### Read Endpoint
```sh
(venv) $ cd tests/read
(venv) $ python -m pytest -v
```
### Update Endpoint
```sh
(venv) $ cd tests/update
(venv) $ python -m pytest -v
```
### Delete Endpoint
```sh
(venv) $ cd tests/delete
(venv) $ python -m pytest -v
```
