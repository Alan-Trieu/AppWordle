# main.py
from Start import StartMenu
from game import App

if __name__ == "__main__":
    WordleApp = StartMenu()
    WordleApp.on_execute()