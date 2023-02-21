# Computing Coursework 2023 : Group K

## Group Members

- Daksh Thapar
- Richard Tan
- Tan Xuan Han


## Requirements

- Install HomeBrew : `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- Install protobuf with `brew install protobuf` *download_dependencies function installs this*
- Install portaudio with `brew install portaudio` *download_dependencies function installs this*
- Python Version : `3.10.9`
- MacOS Version `> 12.6.0`
- Use a Intel Mac

```py
pip3 install -q -r requirements.txt #for no output
pip3 install -r requirements.txt #for output
```

## Usage

> :warning: You need to use a virtual environment to run this project.

- Create a virtual environment called `coursework-venv` :

  - `python3 -m venv coursework-venv`

- Activate it the environment using :
  - `source coursework-venv/bin/activate`

- Install dependencies using `pip3 install -q -r requirements.txt`

- Run the app using :  `python3 main.py`

## Common Errors

`These are errors that you may encounter and we can do nothing about them.`

- If your pip3 has a network error, try running it with a proxy. We tested it with a China proxy and it worked. 
- If you get an error saying `portaudio.h` not found, try running `brew install portaudio` and then run the app again.
- If you get an error saying `libportaudio.2.dylib` not found or something simliar, try running `brew install portaudio` and then run the app again.
