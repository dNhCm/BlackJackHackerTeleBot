import importlib
import os

from aiogram import Dispatcher

from misc.project_path import get_project_path


def register_dp_middlewares(dp: Dispatcher):
    """


    :param dp:
    :return:
    """

    path = os.path.abspath(__file__).split('\\')[:-1]
    modules: list[str] = list(map(lambda x: x[:-3], os.listdir("\\".join(path))))
    modules.remove('__init__')
    modules.remove('__pycach')

    package = ".".join(path[len(get_project_path().split('\\')):])
    for module in modules:
        import_register = importlib.import_module(f".{module}", package=package).register
        import_register(dp)
