from random import uniform, randint
from Monster import monster
import requests
import time


class Rpg:
    def comandos(self):
        return '1 - "/Comandos" [Mostra comandos disponiveis]\n2 - "/editarNome" [Edita o nome do heroi]\n3 - "/status" [Mostra o status do heroi]\n4 - "/dungeon" [Inicia combate a criaturas]\n5 - "/meditar" [Recupera a sua vida]\n6 - "/tutorial" [Exibe um tutorial basico do jogo]\n7 - "/loja" [Exibe a loja]'

    def combate(self, nivelD, url_base, player):
        criatura = monster(nivelD)

        criatura.life = uniform(5 + criatura.lvl, 9 * criatura.lvl)
        criatura.dano = uniform(2 + criatura.lvl, 3 * criatura.lvl)
        criatura.gold = randint(-1 + criatura.lvl, 1 * criatura.lvl)
        criatura.exp = randint(9 + criatura.lvl, 100 + (5 * criatura.lvl))

        resposta = f'Você encontrou uma criatura\nStatus da criatura:\n\nVida:{"{:.{}f}".format( criatura.life, 2 )}\nDano:{"{:.{}f}".format( criatura.dano, 2 )}'

        self.responder(url_base, player.id, resposta)

        resposta = f'Iniciando combate...'
        self.responder(url_base, player.id, resposta)
        time.sleep(1)

        while player.life > 0 and criatura.life > 0:
            resposta = ''
            dano = uniform((player.dano * 0.7), player.dano)
            if uniform(0, 10) > 7:
                dano = dano * 2
                resposta = 'Critico!\n'
            criatura.life = criatura.life - dano
            resposta = resposta + f'Voce deu: {"{:.{}f}".format( dano, 2 )} de dano\nVida da criatura: {"{:.{}f}".format( criatura.life, 2 )}'
            self.responder(url_base, player.id, resposta)
            time.sleep(0.5)

            if criatura.life <= 0:
                break

            resposta = ''
            dano = uniform((criatura.dano * 0.7), criatura.dano)
            if uniform(0, 10) > 9:
                dano = dano * 2
                resposta = 'Critico!\n'
            player.life = player.life - dano
            resposta = resposta + f'Voce recebeu: {"{:.{}f}".format( dano, 2 )} de dano\nSua vida: {"{:.{}f}".format( player.life, 2 )}/{"{:.{}f}".format( player.maxLife, 2 )}'
            self.responder(url_base, player.id, resposta)
            time.sleep(0.5)

        if player.life <= 0:
            player.dead = True
            player.reiniciar()
            resposta = 'Você morreu e seus status voltaram para o lvl 1, tome cuidado aventureiro!!!'
            self.responder(url_base, player.id, resposta)
            return player

        player.gold += criatura.gold
        player.exp += criatura.exp

        if player.exp >= player.maxExp:
            player.upar()
            resposta = 'Parabéns voce subiu de nivel!!! confira seu novo status em "/status"'
            self.responder(url_base, player.id, resposta)
        resposta = f'Resultado:\n\nExp ganho: {criatura.exp}\nGold: {criatura.gold}'
        self.responder(url_base, player.id, resposta)
        return player

    def responder(self, url_base, chat_id, resposta):
        link_requisicao = f'{url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_requisicao)
        return
