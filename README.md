# 🧮 Python Calculator

A fully working desktop calculator app built with Python's built-in `tkinter` library. No external dependencies required.

![<img width="430" height="781" alt="image" src="https://github.com/user-attachments/assets/51b17b5a-6634-47dd-be69-dcbb22f9038d" />
](calculator.png)

## Features

- Basic arithmetic: addition, subtraction, multiplication, division
- Operator chaining (e.g. `12 + 5 * 3 =`)
- Decimal point support
- Percentage (`%`) and sign toggle (`+/-`)
- Clear (`C`), Clear Entry (`CE`), and Backspace (`⌫`)
- Full keyboard support — type numbers/operators directly, `Enter` to evaluate, `Esc` to clear
- Graceful error handling (e.g. division by zero shows a message instead of crashing)
- Safe expression evaluation — restricted `eval` with no access to builtins, so user input can't execute arbitrary code

## Getting Started

### Prerequisites

- Python 3.x ([download here](https://www.python.org/downloads/))
- `tkinter` — included with Python on Windows and macOS. On Linux, install it with:
  ```bash
  sudo apt install python3-tk
  ```

### Running the app

```bash
git clone https://github.com/yourusername/python-calculator-app.git
cd python-calculator-app
python calculator.py
```

(On macOS/Linux you may need `python3` instead of `python`.)

## How It Works

The app is a single Python file built with `tkinter`:

- The UI is a grid of `Button` widgets laid out with `.grid()`, styled to resemble a modern calculator.
- Button presses build up an expression string (e.g. `"12+5*3"`), shown live in the display label.
- Pressing `=` evaluates the expression using a restricted version of Python's `eval()` — only digits and `+ - * / . ( )` are allowed, and builtins are disabled, so it can't be used to run arbitrary code.
- Keyboard events are bound so the calculator can be operated without touching the mouse.

## What I Learned

- Building a GUI with `tkinter`: widgets, layout with `.grid()`, and event binding
- Managing application state cleanly (tracking the current expression vs. the displayed result)
- Writing safer alternatives to raw `eval()` for parsing user input
- Handling edge cases (division by zero, malformed expressions, repeated operators)

## License

This project is open source and available under the [MIT License](LICENSE).
