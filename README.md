# Computing Coursework 2023 : Group K
DakshVision is a project created by Daksh Thapar, Tan Xuan Han and Richard Tan (Group Leader).

It was made with the intent to help people with visual impairments to integrate with the world around them more conveniently. It plays audio based on the objects detected, allowing the visually impaired to understand their environments better, and move around easier.

`Look for our model training code in the model_training folder`

## Group Members

- Daksh Thapar (S4-01)
- Richard Tan (S4-07)
- Tan Xuan Han (S4-08)

## Requirements

1. Install HomeBrew : `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
2. Install protobuf with `brew install protobuf`
3. Install portaudio with `brew install portaudio` 
- Python Version : `3.10.9`
- MacOS Version `> 12.6.0`
- Use a Intel Mac

## Usage

> :warning: You need to use a virtual environment to run this project.

4. Create a virtual environment called `coursework-venv`: `python3 -m venv coursework-venv`
5. Activate the environment using: `source coursework-venv/bin/activate`
6. Install dependencies using `pip3 install -q -r requirements.txt`
7. Run the app using: `python3 main.py`

## Common Errors

`These are errors that you may encounter and we can do nothing about them.`
- If your pip3 has a network error, try running it with a proxy. We tested it with a China proxy and it worked. 
- If you get an error saying `portaudio.h` not found, try running `brew install portaudio` and then run the app again.
- If you get an error saying `libportaudio.2.dylib` not found or something simliar, try running `brew install portaudio` and then run the app again.