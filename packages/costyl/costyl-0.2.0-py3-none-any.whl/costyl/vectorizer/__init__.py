
from . import __vectorizer as vec

def vectorize_files(source_files_paths: list[str], type: str = "all"):

    if type == "all":
        vectorized_files_whole = [vec.vectorize_file_whole(path) for path in source_files_paths]
        vectorized_files_lines = [vec.vectorize_file_in_lines(path) for path in source_files_paths]

        return vectorized_files_whole, vectorized_files_lines

    elif type == "whole":
        vectorized_files_whole = [vec.vectorize_file_whole(path) for path in source_files_paths]

        return vectorized_files_whole

    elif type == "lines":
        vectorized_source_files_lines = [vec.vectorize_file_in_lines(path) for path in source_files_paths]

        return vectorized_source_files_lines
