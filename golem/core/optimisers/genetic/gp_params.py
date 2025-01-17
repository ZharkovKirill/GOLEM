from dataclasses import dataclass
from typing import Sequence, Union, Any

from golem.core.optimisers.genetic.operators.base_mutations import MutationStrengthEnum, MutationTypesEnum, \
    rich_mutation_set
from golem.core.optimisers.optimizer import AlgorithmParameters
from golem.core.optimisers.genetic.operators.crossover import CrossoverTypesEnum
from golem.core.optimisers.genetic.operators.elitism import ElitismTypesEnum
from golem.core.optimisers.genetic.operators.inheritance import GeneticSchemeTypesEnum
from golem.core.optimisers.genetic.operators.regularization import RegularizationTypesEnum
from golem.core.optimisers.genetic.operators.selection import SelectionTypesEnum


@dataclass
class GPAlgorithmParameters(AlgorithmParameters):
    """
    Defines parameters of evolutionary operators and the algorithm of genetic optimizer.

    :param crossover_prob: crossover probability (the chance that two chromosomes exchange some of their parts)
    :param mutation_prob: mutation probability
    :param static_mutation_prob: probability of applying same mutation to graph in a cycle of mutations
    :param max_num_of_operator_attempts: max number of unsuccessful operator (mutation/crossover)
    attempts before continuing
    :param mutation_strength: strength of mutation in tree (using in certain mutation types)
    :param min_pop_size_with_elitism: minimal population size with which elitism is applicable

    :param selection_types: Sequence of selection operators types
    :param crossover_types: Sequence of crossover operators types
    :param mutation_types: Sequence of mutation operators types
    :param elitism_type: type of elitism operator evolution

    :param regularization_type: type of regularization operator

    Regularization attempts to cut off the subtrees of the graph. If the truncated graph
    is not worse than the original, then it enters the new generation as a simpler solution.
    Regularization is not used by default, it must be explicitly enabled.

    :param genetic_scheme_type: type of genetic evolutionary scheme

    The `generational` scheme is a standard scheme of the evolutionary algorithm.
    It specifies that at each iteration the entire generation is updated.

    In the `steady_state` scheme at each iteration only one individual is updated.

    The `parameter_free` scheme is an adaptive variation of the `generational` scheme.
    It specifies that the population size and the probability of mutation and crossover
    change depending on the success of convergence. If there are no improvements in fitness,
    then the size and the probabilities increase. When fitness improves, the size and the
    probabilities decrease. That is, the algorithm choose a more stable and conservative
    mode when optimization seems to converge.
    """

    crossover_prob: float = 0.8
    mutation_prob: float = 0.8
    static_mutation_prob: float = 0.7
    max_num_of_operator_attempts: int = 100
    mutation_strength: MutationStrengthEnum = MutationStrengthEnum.mean
    min_pop_size_with_elitism: int = 5

    selection_types: Sequence[SelectionTypesEnum] = \
        (SelectionTypesEnum.tournament,)
    crossover_types: Sequence[Union[CrossoverTypesEnum, Any]] = \
        (CrossoverTypesEnum.subtree,
         CrossoverTypesEnum.one_point)
    mutation_types: Sequence[Union[MutationTypesEnum, Any]] = rich_mutation_set
    elitism_type: ElitismTypesEnum = ElitismTypesEnum.keep_n_best
    regularization_type: RegularizationTypesEnum = RegularizationTypesEnum.none
    genetic_scheme_type: GeneticSchemeTypesEnum = GeneticSchemeTypesEnum.generational

    def __post_init__(self):
        if self.multi_objective:
            self.selection_types = (SelectionTypesEnum.spea2,)
            # TODO add possibility of using regularization in MO alg
            self.regularization_type = RegularizationTypesEnum.none
