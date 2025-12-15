"""
POS System - Point of Sale
Main entry point for the application
"""
import tkinter as tk
from gui import POSWindow

def main():
    root = tk.Tk()
    app = POSWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()