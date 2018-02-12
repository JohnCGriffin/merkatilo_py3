
test: /tmp/merkatilo-test-data/test-series.txt
	cd merkatilo && PYTHONPATH=.. python3 -m unittest `fgrep -l 'def test' *.py`

mypy:
	mypy *.py

/tmp/merkatilo-test-data/test-series.txt:
	@rm -rf /tmp/merkatilo-test-data && \
		(cd /tmp && git clone https://github.com/JohnCGriffin/merkatilo-test-data)

doc-clean:
	cd docs && make clean

doc: doc-clean
	cd docs && make html

clean: doc-clean
	cd merkatilo && \
	rm -rf __pycache__ *.pyc \
		.mypy_cache/ \
		private/__pycache__ private/*.pyc \
		private/.mypy_cache 
