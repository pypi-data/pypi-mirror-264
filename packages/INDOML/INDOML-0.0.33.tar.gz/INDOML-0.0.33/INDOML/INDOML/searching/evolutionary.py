import numpy as np

class AlgoritmaGenetika:
    """
    Kelas yang merepresentasikan algoritma genetika.

    Atribut:
        n (int): Jumlah individu dalam populasi.
        fitness_function (function): Fungsi fitness yang digunakan untuk mengevaluasi individu.
        partisi_kromosom (int): Jumlah partisi dalam kromosom.
        isi_kromosom (dict): Nilai-nilai yang mungkin untuk setiap partisi dalam kromosom.
        iterasi (int): Jumlah maksimum iterasi yang akan dilakukan (default adalah 0, yang berarti tidak ada batasan).

    Metode:
        inisiasi_kromosom(): Menginisialisasi populasi dengan menghasilkan kromosom acak.
        fitnes_value(populasi): Menghitung nilai fitness untuk setiap individu dalam populasi.
        select_parent(populasi): Memilih induk untuk crossover berdasarkan nilai fitness mereka.
        crossover(tipe, parent): Melakukan crossover antara dua induk untuk menciptakan keturunan baru.
        mutasi(newgen): Melakukan mutasi pada sebuah kromosom.
        elistisme(populasi, new_gen): Mengaplikasikan elitisme untuk memilih individu terbaik untuk generasi berikutnya.
        fit(crossover): Menjalankan algoritma genetika untuk mencari individu terbaik dalam populasi.

    """
    def __init__(self, n: int, fitness_function, partisi_kromosom: int, isi_kromosom: dict, iterasi: int = 0):
        self.n = n
        self.fitness_function = fitness_function
        self.partisi_kromosom = partisi_kromosom
        self.isi_kromosom = isi_kromosom
        self.iterasi = iterasi

    def inisiasi_kromosom(self) -> list:
        list_kromosom = []
        while len(list_kromosom) < self.n:
            kromosom = [np.random.default_rng().choice(self.isi_kromosom[key]) for key in self.isi_kromosom.keys()]
            kromosom.append(1)
            list_kromosom.append(kromosom)
        return list_kromosom

    def fitnes_value(self, populasi) -> np.array:
        return np.array([self.fitness_function(val) for val in populasi])

    def select_parent(self, populasi) -> list:
        fit_value = self.fitnes_value(populasi)
        prob_ind = fit_value / fit_value.sum()
        cum_prob = np.cumsum(prob_ind)
        parent_indeks = []
        for _ in range(2):
            ran_angka = np.random.default_rng().random()
            parent_indeks.append(np.argmax(cum_prob > ran_angka))
        return parent_indeks

    def crossover(self, tipe, parent):
        
        parent1 = parent[0][:-1]
        parent2 = parent[1][:-1]
        if tipe == "single":
            random = np.random.default_rng().integers(self.partisi_kromosom)
            new_gen1 = parent1[:random] + parent2[random:]
            new_gen2 = parent2[:random] + parent1[random:]
        elif tipe == 'double':
            random1 = np.random.default_rng().integers(self.partisi_kromosom)
            random2 = np.random.default_rng().integers(self.partisi_kromosom)
            while random2 == random1:
                random2 = np.random.default_rng().integers(self.partisi_kromosom)
            new_gen1 = parent1[:random1] + parent2[random1:random2] + parent1[random2:]
            new_gen2 = parent2[:random1] + parent1[random1:random2] + parent2[random2:]
        new_gen1.append(1)
        new_gen2.append(1)
        return new_gen1, new_gen2

    def mutasi(self, newgen):
        key_random = np.random.default_rng().choice(list(self.isi_kromosom.keys()))
        random_replace = np.random.default_rng().choice(self.isi_kromosom[key_random])
        newgen[key_random] = random_replace
        return newgen

    def elistisme(self, populasi, new_gen):
        new_populasi = []
        for sublist in populasi:
            sublist[-1] += 1
        populasi = populasi + new_gen
        while len(populasi) > 0:
            maxi = 0
            for i in range(len(populasi[1:])):
                if self.fitness_function(populasi[i + 1]) > self.fitness_function(populasi[maxi]):
                    maxi = i + 1
                elif self.fitness_function(populasi[i + 1]) == self.fitness_function(populasi[maxi]) and populasi[i + 1][-1] < populasi[maxi][-1]:
                    maxi = i + 1
            new_populasi.append(populasi[maxi])
            populasi.pop(maxi)
        populasi = sorted(populasi, key=lambda individu: self.fitness_function(individu), reverse=True)
        new_populasi = new_populasi+populasi
        if len(new_populasi) != self.n:
            elimi = len(new_populasi) - self.n
            new_populasi = new_populasi[:-elimi]
        return new_populasi

    def fit(self, crossover="single"):
        populasi = self.inisiasi_kromosom()
        iterasi = self.iterasi
        prev_avg_fitness = None
        gen = 0
        count = 0
        if crossover == 'double' and self.partisi_kromosom <=2:
            raise Exception("Partisi kromosom harus lebih dari 2")
        while True:
            max_gen = max([self.fitness_function(individu) for individu in populasi])
            print(f"gen-{gen} - best fitnes : {max_gen}")
            parent_index = self.select_parent(populasi)
            parent = [populasi[i] for i in parent_index]
            new_gen = self.crossover(crossover, parent)
            new_gen = [self.mutasi(new_gen[i]) for i in range(2)]
            new_populasi = self.elistisme(populasi, new_gen)
            populasi = new_populasi
            avg_fitness = sum(self.fitness_function(individu) for individu in populasi) / len(populasi)
            if prev_avg_fitness is not None and abs(avg_fitness - prev_avg_fitness) < 0.001:
                break
            prev_avg_fitness = avg_fitness
           
            count += 1
            gen += 1
            if iterasi != 0 and count >= iterasi:
                break
        return populasi[0][:-1]
            
            
        
            
            
        
        
        
            
        
            
        
    