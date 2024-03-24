# Prerequisites
- Python 3.5+
- lib playsound
# Build Pypi and upload
### 1. Project structure
```
py-talkingclock:
   src:
     talkingclock:
         talkingclock.py
         __init__.py
         buddha.ics
         mp3:
             1.mp3
             2.mp3
             ...
   setup.py
```

### 2. Build the package
```bash
python3 setup.py sdist bdist_wheel
```
### 3. Upload the package
```bash
twine upload dist/*
```
# Binary Download
- Download the binary: [download link](https://github.com/kcommerce/py-talkingclock/)

## TalkingClock
### 1. Install TalkingClock

  - Run the following command to install talkingclock
    ```bash
    pip install talking clock
    ```

### 2. Use : play sound time

- Import and use talkingclock
    ```bash
    Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from talkingclock import talkingclock
    >>> talkingclock.play_soundtime()   
    ```
