import yaml
import sys
import os
import nltk

# constants
W2V_PRETRAINED_MODEL = "fasttext-wiki-news-subwords-300"


def download_w2v(download_path: str):
    # Ensure directory for holding W2V model exists
    w2v_download_path = os.path.join(download_path, "w2v")

    if not os.path.isdir(w2v_download_path):
        os.makedirs(w2v_download_path)

    # Download W2V model if missing
    if W2V_PRETRAINED_MODEL not in os.listdir(w2v_download_path):
        print("Word2Vec: Downloading pretrained weights...")
        os.environ["GENSIM_DATA_DIR"] = w2v_download_path
        import gensim.downloader as gsapi
        path = gsapi.load(W2V_PRETRAINED_MODEL, return_path=True)
        print(f"Downloaded weights to:\n{path}")


def download_nltk(download_path: str):
    # Ensure directory for holding nltk stopwords exists.
    nltk_download_path = os.path.join(download_path, "nltk")

    if not os.path.isdir(nltk_download_path):
        os.makedirs(nltk_download_path)

    # Download stopwords if missing
    if 'corpora' not in os.listdir(nltk_download_path):
        print("NLTK: Downloading nltk stopwords...")
        nltk.download('stopwords', download_dir=nltk_download_path)
        print("Downloaded nltk.stopwords")

    # Download punkt if missing.
    if 'tokenizers' not in os.listdir(nltk_download_path):
        print("NLTK: Downloading nltk punkt...")
        nltk.download('punkt', download_dir=nltk_download_path)
        print("Downloaded ntlk.punkt")


def generate_config(location: str):
    config = {
        "PERSONAL_WEBSITE": "https://github.com/<PERSONAL_ACCOUNT_HERE>",
        "EMAIL_ADDRESS": "example@email.com"
    }

    filepath = os.path.join(location, "config.yaml")
    with open(filepath, "w") as file:
        yaml.dump(config, file)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("setup_wikiwormhole <config-path> <download-path>")
    generate_config(sys.argv[1])
    download_w2v(sys.argv[2])
    download_nltk(sys.argv[2])
