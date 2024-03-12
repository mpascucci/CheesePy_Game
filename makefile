docs: README.md
	pdoc --no-show-source -o docs src/cheesepy_game

dist:
	python3 -m pip install --upgrade build
	python3 -m build

test_pypi: clean dist
	python3 -m pip install --upgrade twine
	python3 -m twine upload --repository testpypi dist/*

clean:
	rm -r dist
