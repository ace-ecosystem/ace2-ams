#!/bin/bash
pytest -vv
find ./ \( -name "*.pyc" -or -name ".pytest_cache" -or -name "__pycache__" \) -exec rm -rf {} +
