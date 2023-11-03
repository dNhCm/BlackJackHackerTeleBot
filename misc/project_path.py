import os.path


def get_project_path() -> str:
    return '\\'.join(os.path.abspath(__file__).split('\\')[:-2])