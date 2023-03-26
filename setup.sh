sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
sudo apt-get install virtualenv -y
sudo apt-get install ffmpeg -y
sudo apt-get install tesseract-ocr -y

virtualenv .venv

PWD=`pwd`

activate () {
    . $PWD/.venv/bin/activate
}
activate

python3 -m pip install -r requirements.txt
python3 setup_nltk.py

# check for .env file
if [ ! -f .env ]; then
    echo "Creating .env file"
    cp .env.example .env
fi

# check for if all 3 variables are set in the .env file
# OPENAI_API_KEY=stuff
# DISCORD_TOKEN=stuff
# WATSON_API_KEY=stuff
# Read the .env file and save the lines containing our variables to a variable
vars=$(grep -e "^OPENAI_API_KEY=" -e "^DISCORD_TOKEN=" -e "^WATSON_API_KEY=" .env)

# Check if all three variables are present
if [ $(echo "$vars" | wc -l) -eq 3 ]; then
  echo "All three variables are set!"
else
  echo "Not all three variables are set."
  echo "Please set the following variables in the .env file:"
  echo "OPENAI_API_KEY"
  echo "DISCORD_TOKEN"
  echo "WATSON_API_KEY"
fi