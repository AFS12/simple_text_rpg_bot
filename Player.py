import time
import requests


class player:
    def __init__(self, nome, id):
        self.id = id
        self.nome = nome
        self.life = 100
        self.maxLife = 100
        self.dano = 10
        self.gold = 0
        self.exp = 0
        self.maxExp = 100
        self.lvl = 1
        self.arma = []
        self.armadura = []
        nameEdit = False
        dead = False
        dungeonStart = False

    def meditar(self, url_base):
        tempoMeditando = 1 + ((self.maxLife - self.life) / 10)
        resposta = f'O tempo Meditando será de {"{:.{}f}".format( tempoMeditando, 2 )} segundos\n\nIniciando meditação...'
        self.responder(url_base, resposta)
        time.sleep(tempoMeditando)
        self.life = self.maxLife
        return 'Você terminou de meditar e recuperou sua vida!'

    def responder(self, url_base, resposta):
        link_requisicao = f'{url_base}sendMessage?chat_id={self.id}&text={resposta}'
        requests.get(link_requisicao)
        return

    def reiniciar(self):
        self.life = 100
        self.maxLife = 100
        self.dano = 10
        self.gold = 0
        self.exp = 0
        self.maxExp = 100
        self.lvl = 1
        nameEdit = False
        dead = False

    def upar(self):
        self.maxLife += self.maxLife * 0.25
        self.life = self.maxLife
        self.exp -= self.maxExp
        self.maxExp += self.maxExp * 0.3
        self.dano += self.dano * 0.15
        self.lvl += 1
        return
