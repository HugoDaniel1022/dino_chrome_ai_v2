import torch
import torch.nn as nn

class Brain(nn.Module):
    def __init__(self, n_entradas, n_ocultas):
        super(Brain, self).__init__()
        self.oculta = nn.Linear(n_entradas, n_ocultas)
        self.salida = nn.Linear(n_ocultas, 1)
    
    def forward(self, x):
        x = torch.relu(self.oculta(x))
        x = torch.sigmoid(self.salida(x))  # salida sigmoide
        return x
    
    def asignar_pesos(self, pesos_dict):
        """
        pesos_dict debe ser un diccionario con las claves:
        'w1', 'b1', 'w2', 'b2'
        donde:
          w1: pesos entrada→oculta  (tensor [n_ocultas, n_entradas])
          b1: bias capa oculta       (tensor [n_ocultas])
          w2: pesos oculta→salida    (tensor [1, n_ocultas])
          b2: bias salida            (tensor [1])
        """
        with torch.no_grad():
            self.oculta.weight.copy_(pesos_dict['w1'])
            self.oculta.bias.copy_(pesos_dict['b1'])
            self.salida.weight.copy_(pesos_dict['w2'])
            self.salida.bias.copy_(pesos_dict['b2'])
