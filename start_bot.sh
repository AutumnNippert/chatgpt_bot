#!/bin/bash -x
PWD=`pwd`

activate () {
    . $PWD/.venv/bin/activate
}
activate

python3 bin/bot.py