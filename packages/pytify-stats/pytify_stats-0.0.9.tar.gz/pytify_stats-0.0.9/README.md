[![log github events](https://github.com/software-students-spring2024/3-python-package-exercise-team-7/actions/workflows/event-logger.yml/badge.svg)](https://github.com/software-students-spring2024/3-python-package-exercise-team-7/actions/workflows/event-logger.yml) [![log github events multiple versions](https://github.com/software-students-spring2024/3-python-package-exercise-team-7/actions/workflows/event-log-multiple.yml/badge.svg)](https://github.com/software-students-spring2024/3-python-package-exercise-team-7/actions/workflows/event-log-multiple.yml)

# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

# Package Description

The package pytify_stats is a Python package that runs basic stats gathered from the Spotify API.  It can currently get stats such as artist information, track information, and an artist's top ten tracks.


# How to Use

Here is how to set it up:


1. Run this code in the terminal:

```
pipenv install -i https://test.pypi.org/simple/ pytify-stats==0.0.3.3
```

2. Import it in your python file:

```
from pytify_stats import client
```

3. Create a new account or log in [here](https://developers.spotify.com/). Go to the dashboard, create an app and retrieve your new ID and SECRET


4. Authenicate using the Client class

The example below demonstrates how to do this:

```
from pytify_stats import client

spy = client.Client(CLIENT_ID, CLIENT_SECRET)

album = spy.get_album("KOD")

top_ten = spy.get_top_ten("J. Cole")

song = spy.get_song("She Knows")

print(album)
print(top_ten)
print(song)
```

Put your client_id and client secret you've recieved from Spotify in place of the parameters of the Client class

# How to Contribute

1. Download the source code and open it on a code editor

2. Install pipenv and install the following:

pipenv install requests
pipenv install python-dotenv
pipenv install pytest

3. Make changes and run unit test for it

4. Push changes onto a new branch on GitHub

5. Make a pull request and  wait for a review. If accpeted, the branches will be merged and the new code will be uploaded to PyPi


# Contributors

* [Denzel](https://github.com/denprud)
* [Joyce](https://github.com/joyxe-xie)
* [Neal](https://github.com/nhaulsey)
* [Rakshit](https://github.com/RakSridhar23)
