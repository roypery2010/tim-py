# Makefile for building Python executables with PyInstaller

PYINSTALLER = pyinstaller
FLAGS = --onefile

all: tim_py tasm_py

tim_py: main.py tim_py.py time.py
	$(PYINSTALLER) $(FLAGS) time.py

tasm_py: tasm.py tasmlexer.py tasmparser.py tim_py.py
	$(PYINSTALLER) $(FLAGS) tasm.py

clean:
	rm -rf build dist __pycache__ *.spec