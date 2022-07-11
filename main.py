import requests
import TelegramToken
from array import *
import time
import json
from Rpg import Rpg
from Player import player
from Store import store
from Itens import itens


class TelegramBot:
    def __init__(self):
        token = TelegramToken.getToken()
        self.url_base = f'https://api.telegram.org/bot{token}/'
        self.rpg = Rpg()
        self.store = store()
        self.player = []

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_novas_mensagens(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    nome = dado['message']['from']['first_name']
                    chat_id = dado["message"]["from"]["id"]
                    try:
                      mensagem = str(dado["message"]["text"])
                    except:
                        resposta = 'Isso não é um texto'
                        self.responder(resposta, chat_id)
                        break
                    
                    
                    eh_primeira_mensagem = int(
                        dado["message"]["message_id"]) == 1
                    resposta = self.criar_resposta(mensagem,
                                                   eh_primeira_mensagem, nome,
                                                   chat_id, self.url_base)
                    self.responder(resposta, chat_id)

    # Obter mensagens
    def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    # Criar uma resposta
    def criar_resposta(self, mensagem, eh_primeira_mensagem, nome, chat_id, url_base):
      
        index = self.idplay(self.player, chat_id)
        print(nome + ': ' + mensagem)
        if eh_primeira_mensagem == True or mensagem in ('inicio', 'Inicio',
                                                        "/start", "start"):
            newPlay = player(nome, chat_id)
            newPlay.arma = itens.armas[0]
            newPlay.armadura = itens.armaduras[0]
            self.player.append(newPlay)
            count = 0
            for i in self.player:

                if i.id == chat_id:
                    self.player[count].nameEdit = False
                    self.player[count].dungeonStart = False
                    self.player[count].nome = nome
                    count = 0
                    break
                count += 1

            return f'''Olá {nome}, bem vindo ao RPG BOT, digite "/tutorial" para o primeiro comando ou "/Comandos" para ver a lista de comandos gerais"'''
        elif index == None:
          return 'Opa parece que você ainda não criou seu Heroi, digite /start Para começar'    
        elif mensagem == '/status' or mensagem == '/Status':
            return f'O nome do seu heroi e: {self.player[index].nome} e seus status são:\nLife: {"{:.{}f}".format( self.player[index].life, 2 )}/{"{:.{}f}".format( self.player[index].maxLife, 2 )}\nDano: {"{:.{}f}".format( self.player[index].dano, 2 )}\nGold: {self.player[index].gold}\nLevel: {self.player[index].lvl} ({self.player[index].exp}/{self.player[index].maxExp})\n\nPara alterar o nome do heroi digite "/editarnome"'
        elif mensagem == '/comandos' or mensagem == '/Comandos':
            return self.rpg.comandos()
        elif mensagem == '/dungeon' or mensagem == '/Dungeon':
            self.player[index].dungeonStart = True
            return 'Digite o level da dungeon (quanto mais alto mais forte os monstros)'

        elif self.player[index].dungeonStart:
            self.player[index].dungeonStart = False
            dgLvl = int(mensagem)
            self. player[index] = self.rpg.combate(dgLvl, url_base, self.player[index])
            return 'Dungeon finalizada'
        elif mensagem == ('/editarnome'):
            self.player[index].nameEdit = True
            return 'Digite o novo nome do seu heroi'
        elif self.player[index].nameEdit:
            self.player[index].nameEdit = False
            self.player[index].nome = mensagem
            return 'Nome alterado com sucesso!! Digite "/status" para conferir'
        elif mensagem == '/meditar' or mensagem == '/Meditar':
            return self.player[index].meditar(url_base)

        elif mensagem == "/loja" or mensagem == "/Loja":
          return f'{self.store.listarItens(self.player[index].lvl)}'
        elif mensagem == "/UParma" or mensagem == "/UParmadura":
          self.player[index] = self.store.upgrade(url_base, mensagem, self.player[index])
          return 'Confira seu /status'
        elif mensagem == "/equipamentos":
          return f'Meus equipamentos\nArma: {self.player[index].arma[0]} | Dano: {self.player[index].arma[1]}\nArmadura: {self.player[index].armadura[0]} | Vida: {self.player[index].armadura[1]}'
        elif mensagem == '/tutorial' or mensagem == '/Tutorial':
            self.player[index].life = 1
            return 'Bem vindo ao text RPG bot, nesse mini universo você combate criaturas dentro de "/dungeon" para ganhar exp e gold e subir o nivel do seu "/status", oh veja sua vida!! medite um pouco para recuperar vida usando "/meditar" e tome cuidado, ao morrer você perde seu progresso, Visite a "/loja" para melhorar seus "/equipamentos", para outros comandos digite "/comandos"'
        else:
            return 'Comando desconhecido, para lista de comandos digite "/comandos" ou "/tutorial" para aprender o basico'

        # elif mensagem.lower() in ('s', 'sim'):
        #     return ''' Pedido Confirmado! '''
        # elif mensagem.lower() in ('n', 'não'):
        #     return ''' Pedido Confirmado! '''

    # Responder
    def responder(self, resposta, chat_id):
        link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_requisicao)

    def idplay(self, player, chat_id):
        count = 0
        for i in player:

            if i.id == chat_id:
                
                return count
            count += 1


bot = TelegramBot()
bot.Iniciar()
