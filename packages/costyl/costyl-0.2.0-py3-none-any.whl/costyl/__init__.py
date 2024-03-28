
from .tools import get_authors_files_paths, get_target_files_paths
from .vectorizer import vectorize_files
from .analysers import analyse_vectorized_files

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


class Costyl:

    def __init__(self):
        pass

    def import_authors_files(self, source_folder_path: str):
        """
            This function gets the source folder path and returns the paths of the files and their respective labels(author names)
        """

        self.__source_files_paths, self.__source_files_labels = get_authors_files_paths(source_folder_path)

    def import_target_files(self, source_folder_path: str):
        """
            This function gets the target folder path and returns the paths of the files and their respective labels(file names)
        """

        self.__target_files_paths, self.__target_files_labels = get_target_files_paths(source_folder_path)

    def __vectorize_files(self, source_files_paths: list[str], target_files_paths: list[str]):
        """
            This function vectorizes the source files and target files
        """
        self.__vectorized_source_files_whole, self.__vectorized_source_files_lines = vectorizer.vectorize_files(source_files_paths)
        self.__vectorized_target_files_whole, self.__vectorized_target_files_lines = vectorizer.vectorize_files(target_files_paths)

    def __generate_features(self):
        self.__source_files_data_matrix = analyse_vectorized_files(self.__vectorized_source_files_whole, self.__vectorized_source_files_lines)
        self.__target_files_data_matrix = analyse_vectorized_files(self.__vectorized_target_files_whole, self.__vectorized_target_files_lines)

    def generate_model(self):
        # TODO: Implement the model generation
        self.__vectorize_files(self.__source_files_paths, self.__target_files_paths)
        self.__generate_features()

        self.__model = KNeighborsClassifier(metric="cityblock", n_neighbors=1, algorithm="brute")
        self.__model.fit(self.__source_files_data_matrix, self.__source_files_labels)

    def predict_authors(self):

        predicted_authors = []

        print(self.__target_files_data_matrix)
        input()

        predicted_authors = self.__model.predict(self.__target_files_data_matrix)

        self.__labels_predicted_authors = dict(zip(self.__target_files_labels, predicted_authors))

        return self.__labels_predicted_authors
