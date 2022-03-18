import requests, zipfile

ELECTRICITY_URL = "http://archive.ics.uci.edu/ml/machine-learning-databases/00321/LD2011_2014.txt.zip"
zip_save_path = './data/LD2011_2014.txt.zip'

# Get file using requests library and write in chunks
r = requests.get(ELECTRICITY_URL, stream=True)
with open(zip_save_path, 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)

# Extract zip file
with zipfile.ZipFile(zip_save_path, 'r') as zip_file:
    zip_file.extractall('./data/')