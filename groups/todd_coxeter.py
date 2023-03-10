import itertools as it
from collections import defaultdict
import random
from tabulate import tabulate

from problem import Problem


class ToddCoxeterAlgorithm:
    def __init__(self, gens, rels, h_gens):
        self.gens = gens.lower()
        self.gens_symm = self.gens + self.gens.upper()
        self.rels = rels
        self.h_gens = h_gens
        self.cosets_table = {1: {gen: 0 for gen in self.gens_symm}}
        self.rels_tables = {rel: {1: [1] + [0] * (len(rel) - 1) + [1]} for rel in self.rels}
        self.subgr_tables = {gen: {1: [1] + [0] * (len(gen) - 1) + [1]} for gen in self.h_gens}
        for h_gen in self.h_gens:
            if len(h_gen) == 1:
                self.cosets_table[1][h_gen] = 1
                self.cosets_table[1][h_gen.swapcase()] = 1

    def print(self):
        tables_str = []
        table = [[c] + [row[gen] for gen in self.gens_symm] for c, row in self.cosets_table.items()]
        tables_str.append(tabulate(table, headers=it.chain(['cs'], self.gens_symm), tablefmt='fancy_grid'))
        for rel_type, rel_info in it.chain((('rel', ri) for ri in self.rels_tables.items()),
                                           (('sbg', ri) for ri in self.subgr_tables.items())):
            rel, rel_table = rel_info
            table = [row for c, row in rel_table.items()]
            tables_str.append(tabulate(table, headers=it.chain([rel_type], rel), tablefmt='fancy_grid'))
        for tr in it.zip_longest(*it.chain(ts.split('\n') for ts in tables_str), fillvalue=''):
            print('     '.join(tr))

    def introduce_coset(self, ini_coset, gen):
        new_coset = max(self.cosets_table) + 1
        self.cosets_table[ini_coset][gen] = new_coset
        self.cosets_table[new_coset] = {gen: 0 for gen in self.gens_symm}
        self.cosets_table[new_coset][gen.swapcase()] = ini_coset
        for rel, rel_table in self.rels_tables.items():
            rel_table[new_coset] = [new_coset] + [0] * (len(rel) - 1) + [new_coset]

    def propagate(self):
        deductions = set()
        finished = False
        while not finished:
            finished = True
            for rel, rel_table in it.chain(self.rels_tables.items(), self.subgr_tables.items()):
                for coset, row in rel_table.items():
                    for i in range(len(rel)):
                        if row[i] == 0 and row[i - 1] != 0 and self.cosets_table[row[i - 1]][rel[i - 1]]:
                            row[i] = self.cosets_table[row[i - 1]][rel[i - 1]]
                            finished = False
                            if row[i + 1]:
                                deductions.add((row[i], rel[i], row[i + 1]))
                        if row[i] == 0 and row[i + 1] != 0 and self.cosets_table[row[i + 1]][rel[i].swapcase()]:
                            row[i] = self.cosets_table[row[i + 1]][rel[i].swapcase()]
                            finished = False
                            if row[i - 1]:
                                deductions.add((row[i - 1], rel[i - 1], row[i]))
        return deductions

    @staticmethod
    def transitive_closure_nontrivial_classes(rel):
        affected_elements = set()
        for pair in rel:
            affected_elements |= pair
        rel = set(it.chain.from_iterable(((c1, c2), (c2, c1)) for c1, c2 in map(tuple, rel)))
        edges = defaultdict(set)
        for x, y in rel:
            edges[x].add(y)
        for _ in range(len(rel) - 1):
            edges = defaultdict(set, ((k, v.union(*(edges[i] for i in v))) for (k, v) in edges.items()))
        transitive_closure = set((k, i) for (k, v) in edges.items() for i in v)
        classes = {}
        for c1 in list(sorted(affected_elements)):
            if c1 in affected_elements:
                classes[c1] = set()
                affected_elements.remove(c1)
                for c2 in list(sorted(affected_elements)):
                    if (c1, c2) in transitive_closure:
                        classes[c1].add(c2)
                        affected_elements.remove(c2)
        return classes

    def apply_deductions(self, deductions):
        coincidences = set()
        inverted_deductions = ((c2, gen.swapcase(), c1) for c1, gen, c2 in deductions)
        for c1, gen, c2 in it.chain(deductions, inverted_deductions):
            c2_table = self.cosets_table[c1][gen]
            if c2_table == 0:
                self.cosets_table[c1][gen] = c2
            elif c2_table != c2:
                coincidences.add(frozenset((c2_table, c2)))
        return self.transitive_closure_nontrivial_classes(coincidences)

    def apply_coincidences(self, coincidences):
        new_coincidences = set()
        for c_min, cs in coincidences.items():
            for c in sorted(cs):
                for coset, row in self.cosets_table.items():
                    self.cosets_table[coset] = {gen: c_min if row[gen] == c else row[gen] for gen in self.gens_symm}
                for rel, table in it.chain(self.rels_tables.items(), self.subgr_tables.items()):
                    for coset, row in table.items():
                        table[coset] = [c_min if r == c else r for r in row]
                    if c in table:
                        del table[c]
        for c_min, cs in coincidences.items():
            for c in sorted(cs):
                for gen in self.gens_symm:
                    c_min_gen, c_gen = self.cosets_table[c_min][gen], self.cosets_table[c][gen]
                    if c_min_gen == 0 and c_gen != 0:
                        self.cosets_table[c_min][gen] = c_gen
                    if c_gen != 0 and c_min_gen != 0 and c_gen != c_min_gen:
                        new_coincidences.add(frozenset((c_gen, c_min_gen)))
        for c_min, cs in coincidences.items():
            for c in cs:
                if c in self.cosets_table:
                    del self.cosets_table[c]
        return self.transitive_closure_nontrivial_classes(new_coincidences)

    def run(self, log=False, verbose=False, step_by_step=False, cosets_limit=None, stats=False):
        total_coset_number = 1
        max_coset_number = 1
        coincidences_number = 0
        max_coset = 1
        complete = False
        finished = False
        if verbose:
            self.print()
        while not complete and not finished:
            got_new_deductions = True
            while got_new_deductions:
                if log or verbose:
                    print('Propagate:')
                deductions = self.propagate()
                if verbose:
                    self.print()
                if deductions:
                    if log or verbose:
                        print('Deductions:   {}'.format(
                            ',   '.join('{} * {} = {}'.format(c1, g, c2) for c1, g, c2 in deductions)))
                    coincidences = self.apply_deductions(deductions)
                    if verbose:
                        self.print()
                    while coincidences:
                        coincidences_number += 1
                        if log or verbose:
                            print('Coincidences:   {}'.format(',   '.join(
                                '{} = {}'.format(key, ', '.join(map(str, val))) for key, val in coincidences.items())))
                        coincidences = self.apply_coincidences(coincidences)
                        if verbose:
                            self.print()
                else:
                    got_new_deductions = False
            has_empty_slots = False
            for coset in sorted(self.cosets_table.keys()):
                for gen in self.gens_symm:
                    if self.cosets_table[coset][gen] == 0:
                        has_empty_slots = True
                        max_coset += 1
                        total_coset_number += 1
                        max_coset_number = max(max_coset_number, len(self.cosets_table))
                        if log or verbose:
                            print('Introduce coset:   {} = {} * {}'.format(max(self.cosets_table) + 1, coset, gen))
                        self.introduce_coset(coset, gen)
                        if verbose:
                            self.print()
                        break
                if has_empty_slots:
                    break
            if not has_empty_slots:
                complete = True
            if cosets_limit and len(self.cosets_table) > cosets_limit:
                finished = True
                if log or verbose:
                    print('Allowed number of cosets exceeded')
            if step_by_step:
                input()
                print(' - - - NEXT STEP - - -\n')
        if stats:
            return complete, len(self.cosets_table), {'total': total_coset_number, 'max': max_coset_number,
                                                      'coincidences': coincidences_number}
        return complete, len(self.cosets_table)


def rel_to_tex(rel):
    return ''.join(s if s.islower() else '{}^{{-1}}'.format(s.lower()) for s in rel)


def gen_rel(gens):
    gens = gens.lower()
    gens_symm = gens + gens.upper()
    rel_len = random.randint(2, 4)
    rel = random.choice(gens)
    while len(rel) < rel_len:
        last = (rel[-1], rel[-1].swapcase())
        next_symbol = rel[-1]
        while next_symbol in last:
            next_symbol = random.choice(gens_symm)
        if len(rel) < rel_len - 1 or next_symbol != rel[0].swapcase():
            rel += next_symbol
    return rel


class ToddCoxeter(Problem):
    def __init__(self):
        self.gens, self.rels = self.gen_todd_coxeter()

    def render(self):
        return 'Группа $G$ задана при помощи образующих и соотношений\n\\[ G = \\langle {} \\mid {} \\rangle. \\]\n' \
               'При помощи алгоритма Кокстера---Тодда установить ее изоморфизм с одной из известных групп.'.format(
            ',\\ '.join(self.gens),
            ',\\ '.join(rel_to_tex(rel) for rel in self.rels)
        )

    @staticmethod
    def gen_todd_coxeter():
        gens = 'abc'
        while True:
            rels = tuple(sorted(gen_rel(gens) for i in range(random.randint(3, 3))))
            tc = ToddCoxeterAlgorithm(gens, rels, [])
            complete, size, stats = tc.run(cosets_limit=13, stats=True)
            if complete and size in (8, 10, 12) and stats['coincidences'] >= 3 and stats['max'] <= 12 and stats[
                'total'] <= 14 and all(ToddCoxeterAlgorithm(gens, rels, [s]).run()[1] > 1 for s in gens):
                return gens, rels
            # if complete and size in (6, 8) and stats['coincidences'] >= 2 and stats['max'] <= 7 and stats[
            #     'total'] <= 8 and all(ToddCoxeterAlgorithm(gens, rels, [s]).run()[1] > 1 for s in gens):
            #     return gens, rels
