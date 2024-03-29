# develop and release

## tests

we leverage the `exact-cover-samples` package for the tests

```bash
# install tests dependencies
pip install -e .[tests]

# run the tests
pytest
```

## publish

```bash
# install build dependencies
pip install .[build]

# clean up former builds
rm -rf dist/*

# build in dist/
python -m build

# publish on pypi
twine upload dist/*
```
