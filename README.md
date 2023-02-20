# Computing Coursework 2023 : Group K

## Group Members

- Daksh Thapar
- Richard Tan
- Tan Xuan Han


## Requirements

- Install HomeBrew
- Install protobuf with `brew install protobuf` *download_dependencies function installs this*
- Install portaudio with `brew install portaudio` *download_dependencies function installs this*
- Python Version : `3.10.9`
- MacOS Version `> 13.0.0`
- Use a Intel Mac

```py
pip install -q -r requirements.txt #for no output
pip install -r requirements.txt #for output
```

## Usage

> :warning: You need to use a virtual environment to run this project.

name your virtual environment `coursework-test` and run `source venv/bin/activate` to activate it.

Simulate a medium-density screen such as Motorola Droid 2: `python main.py -m screen:droid2`

Simulate a high-density screen such as HTC One X, in portrait: `python main.py -m screen:onex,portrait`

Simulate the iPad 2 screen: `python main.py -m screen:ipad`

If the generated window is too large, you can specify a scale: `python main.py -m screen:note2,portrait,scale=.75`

Get the full list of available screens: `python main.py -m screen`

