# Wiki Wormhole
## Description
This python library leverages graphs and artificial intelligence to find the path from a start wikipedia page to a destination wikipedia page.

## Installation
Install wikiwormhole through pip package manager.
```
pip install wikiwormhole
```
Then run the setup script to accomplish the following:
- Generate `config.yaml` script for the pageviews api (How many pageviews does a wikipedia page have).
- Download pre-trained Word2Vec model using Gensim.
- Download corpus of stop words (insignificant words) to help embed titles using natural language toolkit (NLTK).
```
python setup_wormhole.py <config-path> <download-path>
```
Here config path is where the new `config-yaml` will be created. The download path is where the Word2Vec model weights and NLTK corpus will be downloaded on your system.

The final step in installation is providing a personal website and email in the `config.yaml` file. Once filled you'll be able to use the pageviews API.
