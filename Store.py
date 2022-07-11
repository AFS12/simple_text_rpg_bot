import requests
import time


class store:
    def listarItens(self, lvl):
        return f'1 - Melhorar Arma [/UParma] - Aumenta o dano (Gold: {7 * lvl})\n2 - Melhorar Armadura [/UParmadura] - Aumenta a vida (Gold: {7 * lvl})'

    def upgrade(self, url_base, mensagem, player):
        custo = 7 * player.lvl

        if mensagem == "/UParma" and player.gold >= custo:
            player.gold -= custo
            up = player.dano * 0.35
            player.dano += up
            resposta = f'Seu dano aumentou em: {"{:.{}f}".format( up, 2 )}\nDano atual: {"{:.{}f}".format( player.dano, 2 )}'
            self.responder(url_base, player.id, resposta)
            return player
        elif mensagem == "/UParmadura" and player.gold >= custo:
            player.gold -= custo
            up = player.maxLife * 0.15
            player.maxLife += up
            resposta = f'Sua vida maxima aumentou em: {"{:.{}f}".format( up, 2 )}\nVida Maxima atual: {"{:.{}f}".format( player.maxLife, 2 )}'
            self.responder(url_base, player.id, resposta)
            return player
        else:
            resposta = 'Você não tem Gold suficiente'
            self.responder(url_base, player.id, resposta)
            return player

    def responder(self, url_base, chat_id, resposta):
        link_requisicao = f'{url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_requisicao)
        return
