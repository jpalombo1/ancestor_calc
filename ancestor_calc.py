from typing import Dict, List, Tuple

import numpy as np


def monte_carlo_run(trials: int, max_gens: int, population: int):
    """Run Monte Carlo Analysis."""
    monte_carlo = np.zeros(trials)
    for trial in range(trials):
        monte_carlo[trial] = do_trial(max_gens=max_gens, population=population)

    print("Average generations for common ancestor: ", np.mean(monte_carlo))
    print("Log2 of population: ", np.log2(population))


def do_trial(max_gens: int, population: int) -> int:
    """Single Monte Carl trial finding first common ancestor.

    Construct parent map of gen and child to its parents.
    Get all kids of given parent using parent tree

    e.g. Parent tree {{0 child: (1 p1, 2 p2), 1: (2, 1), 2: (0, 3), 3: (3, 0), 4: (4, 0)}}
    all_kids_of_parent {(Gen 1, parent 0): [child 2, child 3, child 4], (1, 1): [0, 1], (1, 2): [0, 1], (1, 3): [2, 3], (1, 4): [4]}
    since for parent 0 exists in parent_tree in keys (0,2),(0,3),(0,4) or child 2,3,4 so parent 0 had kids 2,3,4
    Follow on generations will get kids of kids from previous generation.

    Stops when a parent is a common ancestor to all children in latest generation. Most recent common ancestor.
    """
    all_kids_of_parent: Dict[Tuple[int, int], List[int]] = {}
    common_ancestor = np.arange(0, population, dtype=int)

    for gen in range(max_gens):
        cp_tree = get_child_parent_tree(population)
        for parent in range(population):
            all_kids_of_parent[(gen + 1, parent)] = get_all_kids(
                parent, gen, cp_tree, all_kids_of_parent
            )
            if np.array_equal(all_kids_of_parent[(gen + 1, parent)], common_ancestor):
                print(
                    "First Common ancestor, person {0}, generation {1}".format(
                        parent, gen + 1
                    )
                )
                return gen + 1
    return 0


def get_parents(population: int) -> Tuple[int, int]:
    """Get 2 random parents form population that aren't ot the same.
    e.g. In population of 10, child 3 gets parents (5,7)
    """
    p1 = np.random.randint(population).astype(int)
    p2 = np.random.randint(population).astype(int)
    while p1 == p2:
        p2 = np.random.randint(population).astype(int)
    return (p1, p2)


def get_child_parent_tree(population: int) -> Dict[int, Tuple[int, int]]:
    """For a given population, for population number of current children, get random parents from previous generation.
    e.g. Child 0 parents (1,3) Child 1 parents (6,1) Child 2 Parents (4,5), etc...
    """
    return {child: get_parents(population) for child in range(population)}


def get_all_kids(
    parent: int,
    gen: int,
    parent_tree: Dict[int, Tuple[int, int]],
    all_kids_prev: Dict[Tuple[int, int], List[int]],
) -> List[int]:
    """For a given parent, get all kids that the parent made using child parents tree and previous kids tree.

    Get the parent's direct children by finding all instances where current parent is a parent to child in cp_tree.
    If gen 0, these are the members of population parent relates to so return direct kids.
    Otherwise, find recursive children by finding direct children of those kids when they are parents from previous (really future) gen.

    e.g. For gen 0, only denote direct kids since that population we care about as latest gen so cp_tree parent 0 yields (2,4)
    e.g. Other gens, Direct kids of parent 0 are (3,5) Kids of kids would be kids of cp_tree 1 gen back so kids of parent 3 (5,6) and parent 5 (2,4) so all kids (2,4,5,6)
    Note NOT (3,5) in this set since those are not latest gen numbers, but parents of them numbers, need to get latest gen numbers by getting kids of kids which only carry over latest gen numbers.
    """
    direct_kids = [child for child, parents in parent_tree.items() if parent in parents]
    if gen == 0:
        return direct_kids
    kids_kids = [
        all_kids_prev[(gen, child)]
        for child in direct_kids
        if (gen, child) in all_kids_prev
    ]
    return list(sorted(set(sum(kids_kids, []))))


def main():
    """Main function."""
    np.random.seed(123456)
    POPULATION = 50
    MAX_GENS = 100
    TRIALS = 100
    monte_carlo_run(TRIALS, MAX_GENS, POPULATION)


if __name__ == "__main__":
    main()
