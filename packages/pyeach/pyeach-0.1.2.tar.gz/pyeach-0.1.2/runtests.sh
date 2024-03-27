echo 'Performing unit tests.'

source . venv/bin/activate
python3.9 -m unittest
source deactivate

echo 'All unit tests successfull.'
