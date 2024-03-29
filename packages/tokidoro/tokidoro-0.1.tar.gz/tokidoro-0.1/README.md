<div align="center">

# tokidoro

### Pomodoro CLI

`tokidoro` is simple command-line tool that implements the famous pomodoro technique to improve focus and productivity.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

</div>

# Installation

```
cd tokidoro
pip install .
```

# Features

- [x] Start/Stop the timer
- [x] Set duration of breaks/cycle dynamically.
- [x] Save your favourite configuration
- [x] PLAY any audio on completetion of each cycle

---

# Usage

- `tokidoro start` Start a timer with default configuration
- `-d` Set the duration for pomodoro in minutes (int /float)
- `-s`Set the duration for the short break in minutes (int /float)
- `-l`Set the duration for the long break in minutes (int /float)
- `-a` Change the audio by specifying the serial no. of the audio
- `-r`Number of times the audio repeats.
  <br>
- `tokidoro showconfig`displays the current configuration and the list of audio saved.
- `tokidoro configure` Change and save the configuration

---

# Customization

### custom audio

If you want to add a custom audio, paste an mp3 file into the `sounds` directory located in the directory where the pip package is stored
eg :

```
cd /home/<user>/.local/lib/python3.10/site-packages/tokidoro/sounds
```
