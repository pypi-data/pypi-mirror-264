"""
ClearTerminal Library 1.0
"""

from platform import system as sys
from os import system as cmd

system = sys()

def clear():
    """
    Clear your terminal.
    """
    if system == 'Windows':
        cmd('cls')
    else:
        cmd('clear')