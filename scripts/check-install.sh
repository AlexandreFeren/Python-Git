#!/bin/sh

# Try installing the package
if ! pip install . > /dev/null 2>&1; then
    echo "ERROR: Package installation failed! Fix issues before committing."
    exit 1
fi
exit 0