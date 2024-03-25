import numpy as np
import pandas as pd
from ..matematika.error import sum_error_square as sse


class KmeansGA:
    
    def __init__(self, n_clusters, n_pop,iterasi=0, random_state=2):
        self.n_clusters = n_clusters
        self.n_pop = n_pop
        self.iterasi = iterasi
        self.random_state = random_state
        
    
    def fitness_function(self,kromosom:list,x:np.array):
        
        error = 0
        for i in range(1,self.n_clusters+1):
            
            index = [idx for idx, val in enumerate(kromosom[:-1]) if val == i]
            mean = np.mean(x[index],axis=0)
            error += sse(x[index],mean)
            #print(sse(x[index],mean))
        
        return error
    
    def fitnees_value(self,populasi,x:np.array):
        
        return np.array([self.fitness_function(val,x) for val in populasi])
            
    def init_kromosom(self,partisi):
        np.random.seed(self.random_state)
        populasi = []
        while len(populasi) < self.n_pop:
            valid = False
            while not valid:
                kromosom = np.random.randint(0, self.n_clusters, size=partisi)
                # Periksa apakah setiap nilai dari 0 sampai n_clusters-1 muncul minimal sekali
                if all(val in kromosom for val in range(self.n_clusters)):
                    valid = True
            
            # Konversi ke list dan tambahkan ke populasi jika belum ada
            kromosom_list = kromosom.tolist()
            kromosom_list.append(1)
            if kromosom_list not in populasi:
                populasi.append(kromosom_list)
        
        return populasi
    
    def select_parent(self,populasi,x:np.array):
        np.random.seed(self.random_state)
        fit_value = self.fitnees_value(populasi,x)
        prob_ind = fit_value / fit_value.sum()
        cum_prob = np.cumsum(prob_ind)
        parent_indeks = []
        for _ in range(2):
            ran_angka = np.random.default_rng().random()
            parent_indeks.append(np.argmax(cum_prob > ran_angka))
        return parent_indeks
        
    
    def crossover(self, tipe, parent,partisi):
        np.random.seed(self.random_state)
        
        parent1 = parent[0][:-1]
        parent2 = parent[1][:-1]
        if tipe == "single":
            random = np.random.default_rng().integers(partisi)
            new_gen1 = parent1[:random] + parent2[random:]
            new_gen2 = parent2[:random] + parent1[random:]
        elif tipe == 'double':
            random1 = np.random.default_rng().integers(partisi)
            random2 = np.random.default_rng().integers(partisi)
            while random2 == random1:
                random2 = np.random.default_rng().integers(partisi)
            new_gen1 = parent1[:random1] + parent2[random1:random2] + parent1[random2:]
            new_gen2 = parent2[:random1] + parent1[random1:random2] + parent2[random2:]
        new_gen1.append(1)
        new_gen2.append(1)
        return new_gen1, new_gen2
    
    def mutasi(self, newgen, partisi):
        np.random.seed(self.random_state)
        key_random = np.random.default_rng().integers(partisi)
        random_replace = np.random.default_rng().integers(self.n_clusters)
        newgen[key_random] = random_replace
        return newgen
    
    def elistisme(self, populasi, new_gen,x:np.array):
        new_populasi = []
        for sublist in populasi:
            sublist[-1] += 1
        populasi = populasi + new_gen
        while len(populasi) > 0:
            mini = 0
            for i in range(len(populasi[1:])):
                if self.fitness_function(populasi[i + 1],x) < self.fitness_function(populasi[mini],x):
                    mini = i + 1
                elif self.fitness_function(populasi[i + 1],x) == self.fitness_function(populasi[mini],x) and populasi[i + 1][-1] < populasi[mini][-1]:
                    mini = i + 1
            new_populasi.append(populasi[mini])
            populasi.pop(mini)
        populasi = sorted(populasi, key=lambda individu: self.fitness_function(individu,x))
        new_populasi = new_populasi+populasi
        if len(new_populasi) != self.n_pop:
            elimi = len(new_populasi) - self.n_pop
            new_populasi = new_populasi[:-elimi]
        return new_populasi
    
    def fit(self, x:np.array,crossover="single"):
        np.random.seed(self.random_state)
        partisi = x.shape[0]
        populasi = self.init_kromosom(partisi)
        iterasi = self.iterasi
        prev_avg_fitness = None
        gen = 0
        count = 0
        if crossover == 'double' and self.partisi_kromosom <=2:
            raise Exception("Partisi kromosom harus lebih dari 2")
        while True:
            max_gen = min([self.fitness_function(individu,x) for individu in populasi])
            print(f"gen-{gen} - best fitnes : {max_gen}")
            parent_index = self.select_parent(populasi,x)
            parent = [populasi[i] for i in parent_index]
            new_gen = self.crossover(crossover, parent,partisi)
            new_gen = [self.mutasi(new_gen[i],partisi) for i in range(2)]
            new_populasi = self.elistisme(populasi, new_gen,x)
            populasi = new_populasi
            avg_fitness = sum(self.fitness_function(individu,x) for individu in populasi) / len(populasi)
            if prev_avg_fitness is not None and abs(avg_fitness - prev_avg_fitness) < 0.001:
                break
            prev_avg_fitness = avg_fitness
           
            count += 1
            gen += 1
            if iterasi != 0 and count >= iterasi:
                break
        return populasi[0][:-1]
    
    
    
        
        
        

