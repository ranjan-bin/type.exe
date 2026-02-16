# type.exe

a typing test that runs in your terminal.

![Python](https://img.shields.io/badge/python-3.8+-blue) ![Terminal](https://img.shields.io/badge/runs%20in-terminal-green)

## setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## run

```bash
./run.sh
```

or manually:

```bash
source venv/bin/activate
python3 main.py
```

## how it works

- pick a content type: code, paragraphs, single lines, logs, or shell commands
- pick a test mode: completion or timed (15s / 30s / 60s)
- type. green = correct, red = wrong
- WPM, accuracy, and history tracked locally

nothing leaves your machine.

## project structure

```
type.exe/
  main.py              # entry point
  menu.py              # menus and navigation
  game_engine.py       # typing test loop
  ui_renderer.py       # live render during typing
  content_generator.py # text pools for each mode
  input_handler.py     # raw terminal input
  stats.py             # stats tracking and dashboard
  run.sh               # convenience launcher
```

## requirements

- python 3.8+
- [rich](https://github.com/Textualize/rich)
- a terminal that supports unicode
