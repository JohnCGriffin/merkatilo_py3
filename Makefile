
ok: user_imports.py /tmp/merkatilo-test-data/test-series.txt
	@python3 user_imports.py

mypy:
	mypy *.py

/tmp/merkatilo-test-data/test-series.txt:
	@rm -rf /tmp/merkatilo-test-data && (cd /tmp && git clone https://github.com/JohnCGriffin/merkatilo-test-data)

test: /tmp/merkatilo-test-data/test-series.txt
	python3 -m unittest *.py

clean:
	rm -rf __pycache__ *.pyc .mypy_cache/ private/__pycache__ private/*.pyc private/.mypy_cache
