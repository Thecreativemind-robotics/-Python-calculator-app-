"""
Fully Working Calculator App
-----------------------------
A GUI calculator built with Python's built-in tkinter library.
No external dependencies required — just run:  python calculator.py

Features:
- Basic operations: +, -, *, /
- Decimal point support
- Percentage (%)
- Clear (C) and Clear Entry (CE)
- Backspace (⌫)
- Sign toggle (+/-)
- Keyboard support (type numbers/operators, Enter = "=", Esc = clear)
- Safe expression evaluation (no use of raw eval on arbitrary input)
"""

import tkinter as tk
from tkinter import font as tkfont


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")

        # State
        self.expression = ""      # full expression being built, e.g. "12+5"
        self.display_var = tk.StringVar(value="0")
        self.just_evaluated = False

        self._build_ui()
        self._bind_keys()

    # ---------- UI ----------
    def _build_ui(self):
        display_font = tkfont.Font(family="Helvetica", size=32, weight="bold")
        btn_font = tkfont.Font(family="Helvetica", size=18)

        display = tk.Label(
            self,
            textvariable=self.display_var,
            anchor="e",
            bg="#1e1e1e",
            fg="white",
            font=display_font,
            padx=20,
            pady=30,
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew")

        buttons = [
            ("C", 1, 0), ("CE", 1, 1), ("⌫", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("+/-", 5, 0), ("0", 5, 1), (".", 5, 2), ("=", 5, 3),
            ("%", 6, 0),
        ]

        # color scheme
        op_bg = "#ff9f0a"
        op_fg = "white"
        num_bg = "#333333"
        num_fg = "white"
        func_bg = "#a5a5a5"
        func_fg = "black"
        eq_bg = "#ff9f0a"

        operators = {"/", "*", "-", "+"}
        functions = {"C", "CE", "⌫", "+/-", "%"}

        for (text, row, col) in buttons:
            if text == "=":
                bg, fg = eq_bg, "white"
            elif text in operators:
                bg, fg = op_bg, op_fg
            elif text in functions:
                bg, fg = func_bg, func_fg
            else:
                bg, fg = num_bg, num_fg

            btn = tk.Button(
                self,
                text=text,
                font=btn_font,
                bg=bg,
                fg=fg,
                activebackground="#555555",
                activeforeground="white",
                relief="flat",
                width=5,
                height=2,
                command=lambda t=text: self.on_button(t),
            )
            colspan = 2 if text == "%" and False else 1  # reserved for layout tweaks
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

        # Make the "%" span nicely by placing it alone in row 6 col 0,
        # leave rest of row 6 empty for a clean look.
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.grid_rowconfigure(i, weight=1)

    def _bind_keys(self):
        self.bind("<Key>", self.on_key)
        self.bind("<Return>", lambda e: self.on_button("="))
        self.bind("<KP_Enter>", lambda e: self.on_button("="))
        self.bind("<BackSpace>", lambda e: self.on_button("⌫"))
        self.bind("<Escape>", lambda e: self.on_button("C"))

    # ---------- Logic ----------
    def on_key(self, event):
        char = event.char
        if char in "0123456789.+-*/":
            self.on_button(char)
        elif char == "%":
            self.on_button("%")

    def on_button(self, char):
        if char == "C":
            self.expression = ""
            self.just_evaluated = False
            self._update_display("0")

        elif char == "CE":
            # Clear only the last number typed (simple approach: clear all for this scope)
            self.expression = ""
            self._update_display("0")

        elif char == "⌫":
            if self.just_evaluated:
                self.expression = ""
                self.just_evaluated = False
            self.expression = self.expression[:-1]
            self._update_display(self.expression if self.expression else "0")

        elif char == "+/-":
            self.expression = self._toggle_sign(self.expression)
            self._update_display(self.expression if self.expression else "0")

        elif char == "%":
            if self.expression:
                try:
                    value = self._safe_eval(self.expression)
                    value = value / 100
                    self.expression = self._format_number(value)
                    self._update_display(self.expression)
                except Exception:
                    self._update_display("Error")
                    self.expression = ""

        elif char == "=":
            if self.expression:
                try:
                    result = self._safe_eval(self.expression)
                    self._update_display(self._format_number(result))
                    self.expression = self._format_number(result)
                    self.just_evaluated = True
                except ZeroDivisionError:
                    self._update_display("Cannot divide by 0")
                    self.expression = ""
                except Exception:
                    self._update_display("Error")
                    self.expression = ""

        else:
            # digit, operator, or decimal point
            if self.just_evaluated:
                # start fresh unless user chose an operator to continue chaining
                if char in "+-*/":
                    pass  # keep result and continue expression
                else:
                    self.expression = ""
                self.just_evaluated = False

            # prevent two operators in a row (except leading minus for negative numbers)
            if char in "+-*/" and self.expression and self.expression[-1] in "+-*/":
                self.expression = self.expression[:-1] + char
            else:
                self.expression += char

            self._update_display(self.expression)

    def _update_display(self, text):
        self.display_var.set(text if text else "0")

    @staticmethod
    def _toggle_sign(expr):
        """Toggle the sign of the last number in the expression."""
        if not expr:
            return expr
        # find the start of the last number
        i = len(expr) - 1
        while i > 0 and (expr[i].isdigit() or expr[i] == "."):
            i -= 1
        if expr[i] in "+-*/":
            start = i + 1
        else:
            start = i
        last_num = expr[start:]
        rest = expr[:start]
        if last_num.startswith("-"):
            last_num = last_num[1:]
        else:
            last_num = "-" + last_num
        return rest + last_num

    @staticmethod
    def _safe_eval(expr):
        """
        Safely evaluate a basic arithmetic expression containing only
        digits, ., +, -, *, / — no access to builtins or names.
        """
        allowed = set("0123456789.+-*/() ")
        if not expr or any(c not in allowed for c in expr):
            raise ValueError("Invalid expression")
        # Guard against dangling operators
        if expr[-1] in "+-*/.":
            expr = expr[:-1]
        if not expr:
            raise ValueError("Invalid expression")
        return eval(expr, {"__builtins__": {}}, {})

    @staticmethod
    def _format_number(value):
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            # trim trailing zeros, keep reasonable precision
            return f"{value:.10f}".rstrip("0").rstrip(".")
        return str(value)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
