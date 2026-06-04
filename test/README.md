# URL Accessibility Checker

This project helps you check the accessibility of external URLs listed in your website’s `index.html` file. The test tooling has been reworked to use pytest and a simpler, importable module for unit testing.

## Project Structure

```
.github/
└── workflows/
   └── url_check.yml   # GitHub Actions workflow (runs pytest)
test/
├── src/
│   ├── link_checker.py    # Importable link-checker module
│   └── utils.py           # Utility functions for URL handling
├── requirements.txt       # Python dependencies (pytest included)
└── README.md              # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone git@github.com:matthlud/matthlud.github.io.git
   cd test
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Run tests locally (pytest)**:
   ```bash
   pytest -q test/
   ```

4. **(Optional) Run the legacy checker**:
   A thin CLI runner remains (`test/src/main.py`) which invokes the importable module:
   ```bash
   python test/src/main.py
   ```

## Skiplist format

The skiplist at `test/skip_domains.txt` now uses a JSON array format (one file, JSON array). The checker will also accept legacy one-domain-per-line content for backward compatibility.

## CI

The GitHub Actions workflow was updated to run `pytest` instead of invoking the checker script directly.
