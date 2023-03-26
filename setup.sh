sudo apt-get install virtualenv
sudo apt-get install ffmpeg
sudo apt-get install tesseract-ocr

virtualenv .venv

PWD=`pwd`

activate () {
    . $PWD/.venv/bin/activate
}
activate

python3 -m pip install -r requirements.txt
python3 setup_nltk.py