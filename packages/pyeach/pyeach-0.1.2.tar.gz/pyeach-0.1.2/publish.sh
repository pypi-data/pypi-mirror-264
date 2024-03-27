###### Perform tests ######
echo 'Performing unit tests.'
bash runtests.sh
echo 'Unit tests successful.'

####### Build pyeach ######
echo 'Building pyeach'
python3.9 -m build
echo 'pyeach successfully built.'

###### publish to TestPyPi ######
# python3.9 -m twine upload --repository testpypi dist/*
###### publish to PyPi ######
python3.9 -m twine upload dist/*
