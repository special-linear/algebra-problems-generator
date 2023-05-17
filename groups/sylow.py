from list_problem import FromListProblem
from os.path import abspath, relpath, join, dirname


class SylowNotSimple(FromListProblem):
    problems_source = (join(dirname(__file__), 'sylow.toml'), 'not_simple')
