# rendersrt <a href="https://pypi.python.org/pypi/rendersrt"><img src="https://img.shields.io/pypi/v/rendersrt.svg"></img></a>

### Render subtitle files into any video / audio files
rendersrt is a simple command line tool made with python to render a subtitle file into any video or audio files.

### Installation
If you don't have python on your Windows system you can get compiled version from this git release assets
https://github.com/botbahlul/rendersrt/releases

Just extract those ffmpeg.exe and rendersrt.exe into a folder that has been added to PATH ENVIRONTMET for example in C:\Windows\system32

You can get latest version of ffmpeg from https://www.ffmpeg.org/

In Linux you have to install this script with python (version minimal 3.8 ) and install ffmpeg with your linux package manager for example in debian based linux distribution you can type :

```
sudo apt update
sudo apt install -y ffmpeg
```

To install this rendersrt, just type :
```
pip install rendersrt
```

You can try to compile that rendersrt.py script in win/linux folder into a single executable file with pyinstaller by typing these :
```
pip install pyinstaller
pyinstaller --onefile rendersrt.py
```

The executable compiled file will be placed by pyinstaller into dist subfolder of your current working folder, so you can just rename and put that compiled file into a folder that has been added to your PATH ENVIRONTMENT so you can execute it from anywhere

I was succesfuly compiled it in Windows 10 with pyinstaller-5.1 and Pyhton-3.10.4, and python-3.8.12 in Debian 9

Another alternative way to install this script with python is by cloning this git (or downloading this git as zip then extract it into a folder), and then just type :

```
pip install wheel
python setup.py build
python setup.py bdist_wheel
```

Then check the name of the whl file created in dist folder. In case the filename is rendersrt-0.0.1-py2.py3-none-any.whl then you can install that whl file with pip :
```
cd dist
pip install rendersrt-0.0.1-py2.py3-none-any.whl
```

You can also install this script (or any pip package) in ANDROID DEVICES via PYTHON package in TERMUX APP

https://github.com/termux/termux-app/releases/tag/v0.118.0

Choose the right apk for your device, install it, then open it

Type these commands to get python, pip, this rendersrt, (and any other pip packages) :

```
termux-setup-storage
pkg update -y
pkg install -y python
pkg install -y ffmpeg
pip install rendersrt
```

### Simple usage example 

```
rendersrt --help
rendersrt "Episode 1.mp4" "Episode 1.srt" "output.mp4"
```

### Usage

```
usage: rendersrt [-h] [-v] video_file_path subtitle_file_path output_file_path

positional arguments:
  video_file_path     video file path
  subtitle_file_path  SRT subtitle file path
  output_file_path    output video file path

options:
  -h, --help          show this help message and exit
  -v, --version       show program's version number and exit
```

### License

MIT

Check my other SPEECH RECOGNITIION + TRANSLATE PROJECTS in https://botbahlul.github.io
