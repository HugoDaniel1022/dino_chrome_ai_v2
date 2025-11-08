import torch
import random
import copy

class Genoma:
    def __init__(self, n_entradas, n_ocultas, rango=(-1.0, 1.0)):
        self.n_entradas = n_entradas
        self.n_ocultas = n_ocultas
        self.rango = rango
        self.genes = self.genesis()
        self._update_attributes()

    def genesis(self):
        """Genera tensores de pesos y biases aleatorios."""
        low, high = self.rango
        w1 = torch.empty(self.n_ocultas, self.n_entradas).uniform_(low, high)
        b1 = torch.empty(self.n_ocultas).uniform_(low, high)
        w2 = torch.empty(1, self.n_ocultas).uniform_(low, high)
        b2 = torch.empty(1).uniform_(low, high)
        return {'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2}

    def _update_attributes(self):
        """Sincroniza atributos w1,b1,w2,b2 con genes."""
        self.w1 = self.genes['w1']
        self.b1 = self.genes['b1']
        self.w2 = self.genes['w2']
        self.b2 = self.genes['b2']

    # ---------------- Métodos de flatten/unflatten ----------------
    def flatten_genes(self):
        """Convierte los genes en un vector 1D."""
        return torch.cat([self.genes['w1'].flatten(),
                          self.genes['b1'].flatten(),
                          self.genes['w2'].flatten(),
                          self.genes['b2'].flatten()])

    def unflatten_genes(self, flat):
        """Reconstruye el diccionario genes desde un vector 1D."""
        h, i = self.n_ocultas, self.n_entradas
        size_w1 = h * i
        size_b1 = h
        size_w2 = h * 1
        size_b2 = 1

        w1 = flat[:size_w1].reshape(h, i)
        b1 = flat[size_w1:size_w1+size_b1]
        start2 = size_w1 + size_b1
        w2 = flat[start2:start2+size_w2].reshape(1, h)
        b2 = flat[start2+size_w2:start2+size_w2+size_b2]

        self.genes = {'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2}
        self._update_attributes()

    # ---------------- Métodos AG ----------------
    def mutate(self, mutation_rate=0.05):
        """Mutación con tasa de mutación (probabilidad por gen)."""
        child = copy.deepcopy(self)
        flat = child.flatten_genes()
        low, high = self.rango

        for i in range(len(flat)):
            if random.random() < mutation_rate:
                flat[i] = random.uniform(low, high)

        child.unflatten_genes(flat)
        return child

    def crossover(self, other, crossover_rate=0.5):
        """Crossover con tasa de mezcla por gen."""
        child = copy.deepcopy(self)
        flat_self = self.flatten_genes()
        flat_other = other.flatten_genes()
        flat_child = flat_self.clone()

        for i in range(len(flat_child)):
            if random.random() < crossover_rate:
                flat_child[i] = flat_other[i]

        child.unflatten_genes(flat_child)
        return child
