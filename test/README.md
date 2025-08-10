# URL Accessibility Checker

This project helps you check the accessibility of external URLs listed in your website’s `index.html` file. You can use the included Python script to send HTTP requests to each URL and log the results. The setup also allows you to run these checks automatically every night using GitHub Actions.

## Project Structure

```
.github/
└── workflows/
   └── url_check.yml   # GitHub Actions workflow for scheduled checks
test/
├── src/
│   ├── check_urls.py       # Main logic for checking URL accessibility
│   └── utils.py            # Utility functions for URL handling
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd test
   ```

2. **Install dependencies**:
   It is recommended that you use a virtual environment. You can create one using `venv`:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the URL checker locally**:
   You can run the URL checker script directly:
   ```bash
   python src/check_urls.py
   ```

## GitHub Actions

The project includes a GitHub Actions workflow so you can automatically check URL accessibility every night. This ensures regular monitoring without manual intervention.

### Workflow Configuration

The workflow is defined in `.github/workflows/url_check.yml`. It sets up the environment, installs dependencies, and runs the `check_urls.py` script.
