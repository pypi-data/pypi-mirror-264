# xdantic
Lightweight configuration library on top of PyDantic

## How to set up a local dev environment
- Clone repo
- Download & install Python 3.9 from official website: https://www.python.org/downloads/
- Check if you have installed the right Python version via Python --version / Python3 --version
- Create virtual environment via `Python3.10 -m venv <env_folder>` and activate your virtual environment via `source <env_folder>/bin/activate`
  - Usually we create your <env_folder> right under project root folder
- Install required build tools: `pip install --upgrade pip setuptools wheel flit`
  - If you don't have pip preinstalled, run `python get-pip.py`. More info from https://pip.pypa.io/en/stable/installation/
- Install dependencies: `flit install -s --deps production --extras testing`
  -If new dependency needs to be added, you should define it in file `pyproject.toml`

## How to build docs
To build the documentation locally, install the `docs` dependency group and run:

```
mkdocs build --site-dir build
```

## Tutorial

The [notebooks](./notebooks) folder contains a Jupyter notebooks that show examples of using xdantic.

## Tests

To run the test locally, install the `testing` dependency group and run:

```
pytest -s test
```

## Release a new version

Use bumpversion to update the project file with a new version

```
bumpversion {patch, minor, major}
```
