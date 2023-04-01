$PWD = (Get-Location).Path

function activate {
    . "$PWD/.venv/bin/activate.ps1"
}

activate

python3 bin/bot.py
