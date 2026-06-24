.PHONY: help install test demo clean

help:
	@echo "Available commands:"
	@echo "  make install  - install Python dependencies"
	@echo "  make test     - run unit tests"
	@echo "  make demo     - run safe demo parser"
	@echo "  make clean    - remove Python cache files"

install:
	python3 -m pip install -r requirements.txt

test:
	python3 -m unittest discover -s tests -v

demo:
	python3 src/main.py --city "Москва" --category "Металлообработка" --limit 3 --demo

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
