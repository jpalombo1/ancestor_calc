import numpy as np

population = 50
max_gens = 100

common_ancestor = [i for i in range(population)]
# np.random.seed(123456)

trials = 100
monte_carlo = np.zeros(trials)

for trial in range(trials):

    parent_tree = {}
    all_kids = {}

    class ForLoopBreak(Exception):
        pass

    try:
        for gen in range(max_gens):
            for child in range(population):
                p1 = np.random.randint(population)
                p2 = np.random.randint(population)
                while p1 == p2:
                    p2 = np.random.randint(population)
                parents = [p1, p2]
                parent_tree[(gen, child)] = parents
            for parent in range(population):
                for parent2 in range(population):
                    if parent in parent_tree[(gen, parent2)]:
                        if (gen + 1, parent) not in all_kids:
                            all_kids[(gen + 1, parent)] = [parent2]
                        else:
                            if gen == 0:
                                all_kids[(gen + 1, parent)].append(parent2)
                            else:
                                if (gen, parent2) not in all_kids:
                                    all_kids[(gen, parent2)] = []
                                all_kids[(gen + 1, parent)].extend(
                                    all_kids[(gen, parent2)]
                                )
                                all_kids[(gen + 1, parent)] = list(
                                    set(all_kids[(gen + 1, parent)])
                                )
                                if all_kids[(gen + 1, parent)] == common_ancestor:
                                    print(
                                        "First Common ancestor, person {0}, generation {1}".format(
                                            parent, gen + 1
                                        )
                                    )
                                    print(all_kids)
                                    monte_carlo[trial] = gen + 1
                                    raise ForLoopBreak()
    except ForLoopBreak:
        pass

print("Average generations for common ancestor: ", np.mean(monte_carlo))
print("Log2 of Population: ", np.log2(population))
# print("Gen : ", gen)
# print("Parent relations")
# print(parent_tree)
# print("All Kids")
# print(all_kids)
