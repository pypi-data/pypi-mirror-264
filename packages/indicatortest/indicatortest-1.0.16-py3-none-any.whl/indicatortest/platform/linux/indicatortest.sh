#!/bin/sh

cd $HOME && \
. .local/venv_indicatortest/bin/activate && \
python3 $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/indicatortest.py && \
deactivate
