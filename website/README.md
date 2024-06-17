# iBOTS Website Builder


## Setup and Installation

```
pip install .
```

## Download Private Data Files and Licenced Files

```
python -m main --cmd pull-data
```

## Build Site once

```
python main.py --cmd render
```

## Rebuild site while working on it, and serve it

```
python main.py --cmd serve 
```


## For Developers

## Install with all dev dependencies, in editable mode
```
pip install -e .[dev]
```

## Run tests

```
pytest
```

## Add/Modify data in the data folder

```
dvc add data
dvc push
git add data.dvc
git commit -m "added data"
```




