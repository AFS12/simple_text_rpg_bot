import requests
import time
from array import *

class itens:
  armas = [["Espada simples", 5], ["Espada de Aço", 10]]
  armaduras = [["Armadura simples", 20], ["Armadura de Aço", 40]]


def listarItens(self):
  resposta = ''
  for i in armas:
    resposta += f'{armas[i][0]}\n'
  return resposta
