# Computing Coursework 2023 : Group K

## Group Members

- Daksh Thapar
- Richard Tan
- Tan Xuan Han


## Requirements

`Install protobuf-compiler for Ubuntu and protobuf for macOS first!!`

```py
pip install -r requirements.txt
```

## Usage

> :warning: We **strongly recommend** using a virtual environment to run this project and run it on a `screen:onex,portrait`.

Simulate a medium-density screen such as Motorola Droid 2: `python main.py -m screen:droid2`

Simulate a high-density screen such as HTC One X, in portrait: `python main.py -m screen:onex,portrait`

Simulate the iPad 2 screen: `python main.py -m screen:ipad`

If the generated window is too large, you can specify a scale: `python main.py -m screen:note2,portrait,scale=.75`

Get the full list of available screens: `python main.py -m screen`

