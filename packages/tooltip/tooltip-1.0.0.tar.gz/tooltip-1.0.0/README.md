# Tooltip for labels, entries, buttons and more

[![PyPI version](https://img.shields.io/pypi/v/tooltip)](https://pypi.org/project/tooltip/) [![License](https://img.shields.io/github/license/guisaldanha/tooltip)](LICENSE) [![Downloads](https://img.shields.io/pypi/dm/tooltip)](https://img.shields.io/pypi/dm/tooltip)

A simple tooltip for tkinter widgets.

## Installation

```bash
pip install tooltip
```

## Usage

```python
ToolTip(widget, text='Widget info', justify='left', width=None, background=None, foreground=None):
```

## Example

```python
import tkinter as tk
from tooltip import ToolTip

root = tk.Tk()

button = tk.Button(root, text='Button')
button.pack(pady=20)
ToolTip(button, text='This is a button and you can describe it here. You can also add a lot of text to see how it will appear and even use bright colors', width=50, justify='center', background='yellow', foreground='blue')

label = tk.Label(root, text='Label')
label.pack(pady=20)
ToolTip(label, 'Descriptions can be discreet too')

root.mainloop()
```

## Authors

* **Guilherme Saldanha** - [guisaldanha](https://github.com/guisaldanha/) - [guisaldanha.com](https://guisaldanha.com)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
