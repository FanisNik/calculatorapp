import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Clean Calculator")
        self.root.geometry("400x680")
        self.root.configure(bg="#ffffff")
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure frame style
        style.configure(
            "Display.TFrame",
            background="#ffffff"
        )
        
        # Configure display styles
        style.configure(
            "Process.TLabel",
            background="#ffffff",
            foreground="#95a5a6",
            font=('SF Pro Display', 16),
            padding=(0, 5)
        )
        
        style.configure(
            "Result.TEntry",
            fieldbackground="#ffffff",
            foreground="#2c3e50",
            borderwidth=0,
            relief="flat"
        )
        
        # Configure button styles
        style.configure(
            "Number.TButton",
            padding=15,
            font=('SF Pro Display', 20),
            background="#ffffff",
            foreground="#2c3e50",
            borderwidth=0,
            relief="flat"
        )
        
        style.configure(
            "Operation.TButton",
            padding=15,
            font=('SF Pro Display', 20),
            background="#f8f9fa",
            foreground="#3498db",
            borderwidth=0,
            relief="flat"
        )
        
        style.configure(
            "Special.TButton",
            padding=15,
            font=('SF Pro Display', 20),
            background="#f8f9fa",
            foreground="#e74c3c",
            borderwidth=0,
            relief="flat"
        )
        
        style.configure(
            "Equal.TButton",
            padding=15,
            font=('SF Pro Display', 20),
            background="#3498db",
            foreground="#ffffff",
            borderwidth=0,
            relief="flat"
        )
        
        # Display frames
        display_frame = ttk.Frame(root, style="Display.TFrame")
        display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=20, pady=(40, 20))
        display_frame.grid_columnconfigure(0, weight=1)
        
        # Process display (shows ongoing calculation)
        self.process_var = tk.StringVar()
        self.process_var.set("")
        self.process_label = ttk.Label(
            display_frame,
            textvariable=self.process_var,
            style="Process.TLabel",
            anchor="e"
        )
        self.process_label.grid(row=0, column=0, sticky="ew")
        
        # Result display
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        display = ttk.Entry(
            display_frame,
            textvariable=self.display_var,
            justify="right",
            font=('SF Pro Display', 40),
            style="Result.TEntry"
        )
        display.grid(row=1, column=0, sticky="nsew", ipady=20)
        
        # Buttons with updated styling
        buttons = [
            ('C', 1, 0, 'Special.TButton'), ('±', 1, 1, 'Special.TButton'),
            ('%', 1, 2, 'Special.TButton'), ('÷', 1, 3, 'Operation.TButton'),
            ('7', 2, 0, 'Number.TButton'), ('8', 2, 1, 'Number.TButton'),
            ('9', 2, 2, 'Number.TButton'), ('×', 2, 3, 'Operation.TButton'),
            ('4', 3, 0, 'Number.TButton'), ('5', 3, 1, 'Number.TButton'),
            ('6', 3, 2, 'Number.TButton'), ('-', 3, 3, 'Operation.TButton'),
            ('1', 4, 0, 'Number.TButton'), ('2', 4, 1, 'Number.TButton'),
            ('3', 4, 2, 'Number.TButton'), ('+', 4, 3, 'Operation.TButton'),
            ('0', 5, 0, 'Number.TButton', 2), ('.', 5, 2, 'Number.TButton'),
            ('=', 5, 3, 'Equal.TButton')
        ]
        
        # Create a frame for buttons with padding
        button_frame = ttk.Frame(root, style="Display.TFrame")
        button_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=20, pady=20)
        
        # Configure button frame grid
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        
        # Add buttons to the frame
        for button in buttons:
            if len(button) == 5:  # For zero button that spans 2 columns
                btn = ttk.Button(
                    button_frame,
                    text=button[0],
                    command=lambda x=button[0]: self.button_click(x),
                    style=button[3]
                )
                btn.grid(row=button[1]-1, column=button[2], columnspan=button[4],
                        padx=4, pady=4, sticky="nsew")
            else:
                btn = ttk.Button(
                    button_frame,
                    text=button[0],
                    command=lambda x=button[0]: self.button_click(x),
                    style=button[3]
                )
                btn.grid(row=button[1]-1, column=button[2], padx=4, pady=4, sticky="nsew")
        
        # Configure main window grid weights
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        self.current_number = "0"
        self.previous_number = None
        self.operation = None
        self.start_new_number = True
        
    def button_click(self, value):
        if value.isdigit() or value == '.':
            if self.start_new_number:
                self.current_number = value
                self.start_new_number = False
            else:
                if value == '.' and '.' in self.current_number:
                    return
                self.current_number += value
            self.display_var.set(self.current_number)
            
        elif value in ('+', '-', '×', '÷'):
            if self.previous_number is not None and not self.start_new_number:
                self.calculate()
            self.operation = value
            self.previous_number = float(self.current_number)
            self.start_new_number = True
            # Update process display
            self.process_var.set(f"{self.previous_number} {self.operation}")
            
        elif value == '=':
            if self.previous_number is not None and not self.start_new_number:
                # Update process display with full calculation
                self.process_var.set(f"{self.previous_number} {self.operation} {self.current_number} =")
                self.calculate()
                self.previous_number = None
                self.operation = None
                self.start_new_number = True
                
        elif value == 'C':
            self.current_number = "0"
            self.previous_number = None
            self.operation = None
            self.start_new_number = True
            self.display_var.set("0")
            self.process_var.set("")  # Clear process display
            
        elif value == '±':
            if self.current_number.startswith('-'):
                self.current_number = self.current_number[1:]
            else:
                self.current_number = '-' + self.current_number
            self.display_var.set(self.current_number)
            
        elif value == '%':
            current = float(self.current_number)
            self.current_number = str(current / 100)
            self.display_var.set(self.current_number)
            if self.previous_number is not None:
                self.process_var.set(f"{self.previous_number} {self.operation} {self.current_number}")
    
    def calculate(self):
        if self.operation is None or self.previous_number is None:
            return
            
        current = float(self.current_number)
        previous = self.previous_number
        
        operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '×': lambda x, y: x * y,
            '÷': lambda x, y: x / y if y != 0 else "Error"
        }
        
        try:
            result = operations[self.operation](previous, current)
            if result == "Error":
                self.display_var.set("Error")
                self.current_number = "0"
                self.process_var.set("Error: Division by zero")
            else:
                # Format result to avoid too many decimal places
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 8)
                self.current_number = str(result)
                self.display_var.set(self.current_number)
        except Exception as e:
            self.display_var.set("Error")
            self.current_number = "0"
            self.process_var.set("Error")

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
