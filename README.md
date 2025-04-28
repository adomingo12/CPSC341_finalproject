# MyPL DevOps Project

## Overview

This project is a DevOps modernization of the **MyPL** language interpreter originally built for CPSC 326.  
It has been updated for **CPSC 334** to include a full **CI/CD pipeline**, **linting**, **testing**, and **automation scripts**.

---

## Project Structure

```
mypl/
├── src/                  # All source code
├── tests/                # All unit tests (pytest)
├── .github/workflows/    # GitHub Actions CI/CD workflow
├── lint.sh               # Bash script to run flake8 silently
├── test.sh               # Bash script to run pytest silently
├── Makefile              # Automates linting, testing, cleaning
├── mypl                  # Runner bash script for mypl.py
├── screenshots/          # Screenshots of test and CI/CD runs
├── reflection.pdf        # Reflection document
├── README.md             # This file
```

---

## Features

- ✅ 10+ Unit Tests using **pytest**
- ✅ Silent Linting with **flake8**
- ✅ GitHub Actions **CI/CD pipeline**
- ✅ Auto-installs **flake8**, **pytest**, and **make** if missing
- ✅ `Makefile` automation (`make lint`, `make test`, `make all`, `make clean`)
- ✅ Clean Bash scripts for local automation (`lint.sh`, `test.sh`)
- ✅ Professional project structure
- ✅ No output spam; silent and clean console logs

---

## How to Use

### 1. Install Dependencies

If needed:

```bash
pip install pytest flake8
```

---

### 2. Running Locally

Run linter:
```bash
./lint.sh
```

Run tests:
```bash
./test.sh
```

Or use `make`:
```bash
make           # Runs lint + test
make lint      # Only linter
make test      # Only tests
make clean     # Removes __pycache__ folders
```

---

### 3. GitHub Actions CI/CD

GitHub Actions automatically:
- Runs `flake8` linting
- Runs `pytest` testing
- Installs missing tools
- Checks `make` exists
- Passes or fails the build visibly

---

## Reflection

See `reflection.pdf` for a full write-up on:
- Tools used
- Process followed
- DevOps learnings
- Challenges faced

---

## Final Notes

This project is a DevOps upgrade of an academic compiler/interpreter project.  
The new setup ensures **automation**, **reproducibility**, and **clean code practices**.

---

✅ **Built for CPSC 334 Final Project, Spring 2024.**