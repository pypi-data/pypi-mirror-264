import numpy as np
from evolutionary import AlgoritmaGenetika

# Test case 1
isi_kromosom = {'A': [1, 2, 3], 'B': [4, 5, 6]}
fitness_function = lambda x: sum(x)
ag = AlgoritmaGenetika(n=5, fitness_function=fitness_function, partisi_kromosom=3, isi_kromosom=isi_kromosom)
populasi = ag.inisiasi_kromosom()
assert len(populasi) == 5

# Test case 2
populasi = [[1, 2, 3, 1], [2, 3, 1, 1], [3, 1, 2, 1], [2, 1, 3, 1], [1, 3, 2, 1]]
fitnes_value = ag.fitnes_value(populasi)
assert np.array_equal(fitnes_value, np.array([7, 7, 7, 7, 7]))

# Test case 3
parent_index = ag.select_parent(populasi)
assert len(parent_index) == 2

# Test case 4
parent = [populasi[i] for i in parent_index]
new_gen = ag.crossover("single", parent)
assert len(new_gen) == 2
assert len(new_gen[0]) == 4
assert len(new_gen[1]) == 4

# Test case 5
new_gen = [ag.mutasi(new_gen[i]) for i in range(2)]
assert len(new_gen) == 2
assert len(new_gen[0]) == 4
assert len(new_gen[1]) == 4

# Test case 6
new_populasi = ag.elistisme(populasi, new_gen)
assert len(new_populasi) == len(populasi) - 3

# Test case 7
best_individual = ag.fit(crossover="single")
assert len(best_individual) == 4