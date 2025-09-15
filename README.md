### UV
- uv init .
- uv tool install ruff

### Pytest
- uv run pytest
- uv run pytest tests/test_name_of_test.py

### Pandas
- uv add "pandas>=2.0.0"
- uv add pandas-stubs

### Jupyter
- uv add jupyterlab
- juypter notebook # starts the juypter server which can be accessed via browser
  - OR creat a *.ipynb file and in it place the following code to load a csv
  ```python
    from pathlib import Path

    import pandas as pd

    # For notebook, use:
    ROOT_DIR = Path.cwd().parent

    # Load your CSV
    df = pd.read_csv(ROOT_DIR / "data" / "your_data.csv")
  ```