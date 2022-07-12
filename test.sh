#!/bin/bash
pytest -vv $1
find ./ \( -name "*.pyc" -or -name ".pytest_cache" -or -name "__pycache__" \) -exec rm -rf {} +
