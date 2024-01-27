dist/gemini_cli-*:
	@poetry build

build: dist/gemini_cli-*
	@echo ""

upload: build
	twine upload -r pypi dist/*  --config-file ~/.pypirc

clean:
	rm -rf dist/
