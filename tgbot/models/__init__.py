import importlib
import os

from misc.project_path import get_project_path


async def init_models():
    path = os.path.abspath(__file__).split('\\')[:-1]
    python_models = os.listdir("\\".join(path))

    for el in python_models:
        if not el[-3:] == ".py":
            python_models.remove(el)
    python_models.remove("__init__.py")
    python_models = list(map(lambda x: x[:-3], python_models))

    package = ".".join(path[len(get_project_path().split('\\')):])
    for module in python_models:
        import_init = importlib.import_module(f".{module}", package=package).main
        await import_init()
