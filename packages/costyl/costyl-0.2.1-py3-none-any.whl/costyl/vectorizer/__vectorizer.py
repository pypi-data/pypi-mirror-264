
import io
from sklearn.feature_extraction.text import CountVectorizer


def vectorize_file_whole(filePath: str) -> str:

    with open(filePath, "rb") as f:
        file = f.read().decode("utf-8")

        return file


def vectorize_file_in_lines(filePath: str) -> list[str]:

    with open(filePath, "rb") as f:
        file = f.readlines()
        file = [line.decode("utf-8") for line in file]

        return file
