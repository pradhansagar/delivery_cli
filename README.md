# Kiki's Delivery Service

A simple command-line application to calculate delivery costs and plan shipments.

## Features

- **Cost Calculation**: Calculate total delivery cost based on weight, distance, and applicable discount offers.
- **Delivery Planning**: Plan shipments for V number of vehicles based on max weight and speed.

## Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses standard library only).

## Usage

### 1. Run the Application

Simply run the `main.py` script from the project root:

```bash
python main.py
```

### 2. Run with Input File

You can also run the application using a pre-defined input file. The application is configured to use `import/sample_input.txt` by default when the `file` option is selected.

1. Run the application:
   ```bash
   python main.py
   ```
2. When prompted, enter `file` (or `f`).

Alternatively, you can run it in a single line:

```bash
echo "file" | python main.py
```

The input file supports comments (lines starting with `#` or `//`) for instructions. You can edit `import/sample_input.txt` to test different scenarios.

### 3. Run Tests

To run the unit tests:

```bash
python -m unittest discover tests
python -m unittest tests/test_cost_service.py
python -m unittest tests/test_delivery_service.py
python -m unittest tests.test_cli_integration.py
```

## Project Structure

- `delivery_app/`: Contains the application logic (offers, calculators, etc.).
- `main.py`: The entry point script.
- `tests/`: Unit tests.

