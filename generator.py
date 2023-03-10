import random

from problem import Problem
from list_problem import FromListProblem
from collections import defaultdict
from updates_handler import ConsoleUpdatesHandler

import numbertheory
import complex
import polynomial
import linear_algebra.matrices
import linear_algebra.vector_spaces
import linear_algebra.linear_maps
import linear_algebra.polylinear
import fields
import groups

topics = {
    'numbertheory': numbertheory,
    'complex': complex,
    'polynomial': polynomial,
    'linalg:matrices': linear_algebra.matrices,
    'linalg:vectorspaces': linear_algebra.vector_spaces,
    'linalg:linearmaps': linear_algebra.linear_maps,
    'linalg:polylinear': linear_algebra.polylinear,
    'fields': fields,
    'groups': groups,
}


def construct_problems(problem_types, variants, updates_handler=ConsoleUpdatesHandler()):
    push_update = updates_handler.push
    push_update(', '.join(map(str, problem_types)))
    problems = {}
    for i, pts in enumerate(problem_types):
        problems_number = sum(1 for variant in variants.values() if i in variant)
        problems[i] = []
        if problems_number:
            if not isinstance(pts, list) and hasattr(pts, 'gen_batch'):
                problems[i] = list(pts.gen_batch(problems_number))
            else:
                count = 0
                while len(problems[i]) < problems_number:
                    pt = random.choice(pts) if isinstance(pts, list) else pts
                    parameters = dict()
                    if isinstance(pt, tuple):
                        pt, parameters = pt
                    if issubclass(pt, FromListProblem):
                        problems[i].append(pt(number=-1))
                    else:
                        new_problem = pt(**parameters)
                        if new_problem not in problems[i]:
                            problems[i].append(new_problem)
                    push_update('{} {}/{}\n'.format(pt.__name__, len(problems[i]), problems_number))
                    count += 1
            random.shuffle(problems[i])
            push_update('{} generated'.format(pt.__name__))
    push_update('generation finished')
    return problems


def render_problems(problems, variants, numbering='manual', variant_separator=r'\clearpage'):
    variant_texts = []
    for variant in sorted(variants.keys()):
        variant_text = '\\section*{{{}}}'.format(variant)
        variant_text += '\n\\addcontentsline{{toc}}{{section}}{{{}}}'.format(variant)
        if numbering == 'auto':
            variant_text += '\n\\setcounter{problem}{0}\n'
        for j, pr in problems.items():
            if j in variants[variant]:
                if numbering == 'manual':
                    variant_text += '\n\\setcounter{{problem}}{{{}}} '.format(j)
                variant_text += '\n\\begin{{problem}} {} \\end{{problem}}'.format(pr.pop(0).render())
        variant_texts.append(variant_text)
    return '\n\n{}\n\n'.format(variant_separator).join(variant_texts)


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


def class2topic(cls):
    return cls.__module__[:cls.__module__.find('.')]


problems_classes = {}

problem_types = defaultdict(lambda: [])

for topic_name, topic_module in topics.items():
    for key, value in topic_module.__dict__.items():
        if isinstance(value, type) and issubclass(value, Problem):
            problem_types[topic_name].append(key)
            problems_classes[key] = value
