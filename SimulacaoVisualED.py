
#  ============================================================================
#  Nome      : Simulador de Estruturas de Dados
#  Autor     : Vito Elias de Queiroga
#  Versao    : 2.0
#  Copyright : 
#  Descricao : Representacao visual do funcionamento de algumas 
#              estruturas de dados
#  ============================================================================

import pygame
from pygame.locals import *
from sys import exit
import time
import math
import copy

pygame.init() 

largura = 1280
altura = 960

tela = pygame.display.set_mode((largura, altura))
tela.fill((255, 255, 255))
pygame.display.set_caption('Listas') 

#FONTES

COLOR_INACTIVE = pygame.Color('grey')
COLOR_ACTIVE = pygame.Color('black')
FONT = pygame.font.Font(None, 32)
FONT2 = pygame.font.Font(None, 42)
FONT3 = pygame.font.Font(None, 48)

#################################################################################################################################################
##############################################################      CLASSES      ################################################################
#################################################################################################################################################

def draw_arrow(screen, colour, start, end):
    pygame.draw.line(screen,colour,start,end,2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen, colour, ((end[0], end[1]), (end[0]+20*math.sin(math.radians(rotation-150)), end[1]+20*math.cos(math.radians(rotation-150))), (end[0]+20*math.sin(math.radians(rotation+150)), end[1]+20*math.cos(math.radians(rotation+150)))))

class NoS:
    def __init__(self, conteudo = None, posicao = (100, 100), prox = (None, None)):
        self.conteudo = conteudo
        self.prox = prox
        self.posicao = posicao
        self.color = "black"

    def printarNo(self, offsetx):
        if self.posicao != (None, None):
            if self.prox != (None, None):
                draw_arrow(tela, "red", (self.posicao[0] + offsetx, self.posicao[1]), (self.prox[0] + offsetx, self.prox[1]))

            txt = FONT3.render(str(self.conteudo), True, "red")

            if self.posicao[0] + offsetx >= 0:
                pygame.draw.circle(tela, self.color, (self.posicao[0] + offsetx, self.posicao[1]), 60)

            if self.conteudo != None:
                tela.blit(txt, (self.posicao[0] - str(self.conteudo).__len__()*9 + offsetx, self.posicao[1] - 15))

class NoD:
    def __init__(self, conteudo = None, posicao = (100, 100), prox = (None, None), ant = (None, None)):
        self.conteudo = conteudo
        self.prox = prox
        self.ant = ant
        self.posicao = posicao
        self.color = "black"

    def printarNo(self, offsetx):
        if self.posicao != (None, None):
            if self.prox != (None, None):
                draw_arrow(tela, "red", (self.posicao[0] + offsetx, self.posicao[1]-10), (self.prox[0] + offsetx, self.prox[1]-10))

            if self.ant != (None, None):
                draw_arrow(tela, "green", (self.posicao[0] + offsetx, self.posicao[1]+10), (self.ant[0] + offsetx, self.ant[1]+10))

            txt = FONT3.render(str(self.conteudo), True, "red")

            if self.posicao[0] + offsetx >= 0:
                pygame.draw.circle(tela, self.color, (self.posicao[0] + offsetx, self.posicao[1]), 60)

            if self.conteudo != None:
                tela.blit(txt, (self.posicao[0] - str(self.conteudo).__len__()*9 + offsetx, self.posicao[1] - 15))

class listaSE:

    def __init__(self):
        self.nElementos = 0
        self.coordenadasCabeca = (100, 550)
        self.dados = []
        self.distancia_proximo = 240
        self.distancia_proxima_seta = 180

    def vazia(self):
        if self.nElementos == 0:
            return True
        else:
            return False
        
    def imprimirLista(self, offsetx=0):
        if not self.vazia():
            i = 1

            for no in self.dados:
                if i == self.nElementos:
                    no.prox = (None, None)
                no.printarNo(offsetx)

                i += 1

    def retornarDados(self):
        return self.dados

    def tamanho(self):
        return self.nElementos

    def elemento(self, pos):
        if self.vazia():
            return -1

        if pos < 1 or pos > self.tamanho():
            return -1

        i = 0

        for no in self.dados:
            if i == pos:
                return no.conteudo

    def posicao(self, dado):
        if self.vazia():
            return -1

        i = 1

        for no in self.dados:
            if no.conteudo == dado:
                return i

            i += 1

    def insereInicioLista(self, valor):
        if self.vazia():
            novoNo = NoS(valor, self.coordenadasCabeca)

            self.dados.append(novoNo)
        else:
            for no in self.dados:
                no.posicao = (no.posicao[0] + self.distancia_proximo, no.posicao[1])
                no.prox = (no.posicao[0] + self.distancia_proxima_seta, no.posicao[1])

            novoNo = NoS(valor, self.coordenadasCabeca, (self.coordenadasCabeca[0] + self.distancia_proxima_seta, self.coordenadasCabeca[1]))

            self.dados.insert(0, novoNo)

        self.nElementos += 1

        return True

    def insereMeioLista(self, pos, valor):
        novoNo = NoS(valor, self.dados[pos-1].posicao, (self.dados[pos-1].posicao[0] + self.distancia_proxima_seta, self.dados[pos-1].posicao[1]))

        for i in range (pos-1, self.nElementos):
            self.dados[i].posicao = (self.dados[i].posicao[0] + self.distancia_proximo, self.dados[i].posicao[1])
            self.dados[i].prox = (self.dados[i].posicao[0] + self.distancia_proxima_seta, self.dados[i].posicao[1])

        self.dados.insert(pos-1, novoNo)

        self.nElementos += 1

        return True
    
    def insereFinalLista(self, valor):
        novoNo = NoS(valor, (self.dados[self.nElementos-1].posicao[0] + self.distancia_proximo, self.dados[self.nElementos-1].posicao[1]))

        self.dados[self.nElementos-1].prox = (self.dados[self.nElementos-1].posicao[0] + self.distancia_proxima_seta, self.dados[self.nElementos-1].posicao[1])

        self.dados.append(novoNo)

        self.nElementos += 1

        return True
    
    def insere(self, valor, pos):
        if self.vazia() and pos != 1:
            return False
        
        if pos <= 0 or pos > self.nElementos + 1:
            return False
        
        if pos == 1:
            return self.insereInicioLista(valor)
        elif pos <= self.nElementos:
            return self.insereMeioLista(pos, valor)
        else:
            return self.insereFinalLista(valor)
        
    def removeInicioLista(self):
        self.dados.pop(0)
        self.nElementos -= 1

        for i in range(0, self.nElementos):
            self.dados[i].posicao = (self.coordenadasCabeca[0] + i*self.distancia_proximo, self.coordenadasCabeca[1])
            self.dados[i].prox = (self.dados[i].posicao[0] + self.distancia_proxima_seta, self.dados[i].posicao[1])

    def removeNaLista(self, pos):
        self.dados.pop(pos-1)
        self.nElementos -= 1

        for i in range(1, self.nElementos):
            self.dados[i].posicao = (self.dados[i-1].posicao[0] + self.distancia_proximo, self.dados[i].posicao[1])
            self.dados[i].prox = (self.dados[i].posicao[0] + self.distancia_proxima_seta, self.dados[i].posicao[1])

    def remove(self, pos):
        if self.vazia():
            return -1
        
        if pos <= 0 or pos > self.nElementos:
            return -1
        
        if pos == 1:
            self.removeInicioLista()
        else:
            self.removeNaLista(pos)

    def procurar(self, valor, mode = 0):
        offsetx = 0

        i = 0

        for no in self.dados:
            i += 1

            if no.posicao[0] > largura:
                offsetx -= 240

            if (no.conteudo == valor and mode == 0) or (i == valor and mode == 1):
                no.color = "green"

                tela.blit(tela2, (0, 0))

                if mode == 0:
                    txt = FONT2.render(str(i), True, "blue")
                    tela.blit(txt, (965, 200))
                if mode == 1:
                    txt = FONT2.render(str(no.conteudo), True, "blue")
                    tela.blit(txt, (965, 200))

                if flag_erro4 == 1:
                    tela.blit(txt_erro, (200, 200))

                if flag_erro5 == 1:
                    tela.blit(txt_erro, (610, 200))

                if flag_erro6 == 1:
                    tela.blit(txt_erro, (965, 200))

                self.imprimirLista(offsetx) 

                pygame.draw.rect(tela, color2, (185, 415, 83, 32))
                pygame.draw.rect(tela, "grey", (186, 416, 81, 30))
                tela.blit(txt_inserir, (191, 421))
                pygame.draw.rect(tela, color3, (585, 415, 100, 32))
                pygame.draw.rect(tela, "grey", (586, 416, 98, 30))
                tela.blit(txt_remover, (591, 421))
                pygame.draw.rect(tela, color4, (955, 415, 115, 32))
                pygame.draw.rect(tela, "grey", (956, 416, 113, 30))
                tela.blit(txt_consultar, (961, 421))

                for box in input_boxes2:
                    box.draw(tela)

                pygame.display.update()

                time.sleep(3)

                no.color = "black"

                break
            else:
                no.color = "blue"

                tela.blit(tela2, (0, 0))

                if flag_erro4 == 1:
                    tela.blit(txt_erro, (200, 200))

                if flag_erro5 == 1:
                    tela.blit(txt_erro, (610, 200))

                if flag_erro6 == 1:
                    tela.blit(txt_erro, (965, 200))

                pygame.draw.rect(tela, color2, (185, 415, 83, 32))
                pygame.draw.rect(tela, "grey", (186, 416, 81, 30))
                tela.blit(txt_inserir, (191, 421))
                pygame.draw.rect(tela, color3, (585, 415, 100, 32))
                pygame.draw.rect(tela, "grey", (586, 416, 98, 30))
                tela.blit(txt_remover, (591, 421))
                pygame.draw.rect(tela, color4, (955, 415, 115, 32))
                pygame.draw.rect(tela, "grey", (956, 416, 113, 30))
                tela.blit(txt_consultar, (961, 421))

                for box in input_boxes2:
                    box.draw(tela)

                self.imprimirLista(offsetx)   

                pygame.display.update()

                no.color = "black"

                time.sleep(0.5)

class listaDE:

    def __init__(self):
        self.nElementos = 0
        self.coordenadasCabeca = (100, 550)
        self.dados = []
        self.distancia_proximo = 240
        self.distancia_proxima_seta = 180

    def vazia(self):
        if self.nElementos == 0:
            return True
        else:
            return False
        
    def imprimirLista(self, offsetx=0):
        if not self.vazia():
            i = 1

            for no in self.dados:
                if i == self.nElementos:
                    no.prox = (None, None)
                no.printarNo(offsetx)

                i += 1

    def retornarDados(self):
        return self.dados

    def tamanho(self):
        return self.nElementos

    def elemento(self, pos):
        if self.vazia():
            return -1

        if pos < 1 or pos > self.tamanho():
            return -1

        i = 0

        for no in self.dados:
            if i == pos:
                return no.conteudo

    def posicao(self, dado):
        if self.vazia():
            return -1

        i = 1

        for no in self.dados:
            if no.conteudo == dado:
                return i

            i += 1

    def insereInicioLista(self, valor):
        if self.vazia():
            novoNo = NoD(valor, self.coordenadasCabeca)

            self.dados.append(novoNo)
        else:
            for no in self.dados:
                no.posicao = (no.posicao[0] + self.distancia_proximo, no.posicao[1])
                no.prox = (no.posicao[0] + self.distancia_proxima_seta, no.posicao[1])
                no.ant = (no.posicao[0] - self.distancia_proxima_seta, no.posicao[1])

            novoNo = NoD(valor, self.coordenadasCabeca, (self.coordenadasCabeca[0] + self.distancia_proxima_seta, self.coordenadasCabeca[1]))

            self.dados.insert(0, novoNo)

        self.nElementos += 1

        return True

    def insereMeioLista(self, pos, valor):
        novoNo = NoD(valor, self.dados[pos-1].posicao, (self.dados[pos-1].posicao[0] + self.distancia_proxima_seta, self.dados[pos-1].posicao[1]), (self.dados[pos-1].posicao[0] - self.distancia_proxima_seta, self.dados[pos-1].posicao[1]))

        for i in range (pos-1, self.nElementos):
            self.dados[i].posicao = (self.dados[i].posicao[0] + self.distancia_proximo, self.dados[i].posicao[1])
            self.dados[i].prox = (self.dados[i].posicao[0] + self.distancia_proxima_seta, self.dados[i].posicao[1])
            self.dados[i].ant = (self.dados[i].posicao[0] - self.distancia_proxima_seta, self.dados[i].posicao[1])

        self.dados.insert(pos-1, novoNo)

        self.nElementos += 1

        return True
    
    def insereFinalLista(self, valor):
        novoNo = NoD(valor, (self.dados[self.nElementos-1].posicao[0] + self.distancia_proximo, self.dados[self.nElementos-1].posicao[1]), (None, None), (self.dados[self.nElementos-1].posicao[0] + 60, self.dados[self.nElementos-1].posicao[1]))

        self.dados[self.nElementos-1].prox = (self.dados[self.nElementos-1].posicao[0] + self.distancia_proxima_seta, self.dados[self.nElementos-1].posicao[1])

        self.dados.append(novoNo)

        self.nElementos += 1

        return True
    
    def insere(self, valor, pos):
        if self.vazia() and pos != 1:
            return False
        
        if pos <= 0 or pos > self.nElementos + 1:
            return False
        
        if pos == 1:
            return self.insereInicioLista(valor)
        elif pos <= self.nElementos:
            return self.insereMeioLista(pos, valor)
        else:
            return self.insereFinalLista(valor)
        
    def removeInicioLista(self):
        if self.tamanho() == 1:
            self.dados.pop(0)
            self.nElementos -= 1
        else:
            self.dados.pop(0)
            self.nElementos -= 1

            for i in range(0, self.nElementos):
                self.dados[i].posicao = (self.coordenadasCabeca[0] + i*self.distancia_proximo, self.coordenadasCabeca[1])
                self.dados[i].prox = (self.dados[i].posicao[0] + self.distancia_proxima_seta, self.dados[i].posicao[1])
                self.dados[i].ant = (self.dados[i].posicao[0] - self.distancia_proxima_seta, self.dados[i].posicao[1])

            self.dados[0].ant = (None, None)

    def removeNaLista(self, pos):
        self.dados.pop(pos-1)
        self.nElementos -= 1

        for i in range(1, self.nElementos):
            self.dados[i].posicao = (self.dados[i-1].posicao[0] + self.distancia_proximo, self.dados[i].posicao[1])
            self.dados[i].prox = (self.dados[i].posicao[0] + self.distancia_proxima_seta, self.dados[i].posicao[1])
            self.dados[i].ant = (self.dados[i].posicao[0] - self.distancia_proxima_seta, self.dados[i].posicao[1])

    def remove(self, pos):
        if self.vazia():
            return -1
        
        if pos <= 0 or pos > self.nElementos:
            return -1
        
        if pos == 1:
            self.removeInicioLista()
        else:
            self.removeNaLista(pos)

    def procurar(self, valor, mode = 0):
        def printar_tela():
            if flag_erro4 == 1:
                tela.blit(txt_erro, (200, 200))

            if flag_erro5 == 1:
                tela.blit(txt_erro, (610, 200))

            if flag_erro6 == 1:
                tela.blit(txt_erro, (965, 200))

            self.imprimirLista(offsetx) 

            pygame.draw.rect(tela, color2, (185, 415, 83, 32))
            pygame.draw.rect(tela, "grey", (186, 416, 81, 30))
            tela.blit(txt_inserir, (191, 421))
            pygame.draw.rect(tela, color3, (585, 415, 100, 32))
            pygame.draw.rect(tela, "grey", (586, 416, 98, 30))
            tela.blit(txt_remover, (591, 421))
            pygame.draw.rect(tela, color4, (955, 415, 115, 32))
            pygame.draw.rect(tela, "grey", (956, 416, 113, 30))
            tela.blit(txt_consultar, (961, 421))

            for box in input_boxes3:
                box.draw(tela)

        offsetx = 0

        i = 0

        if mode == 0:
            for no in self.dados:
                i += 1

                if no.posicao[0] > largura:
                    offsetx += 240

                if no.conteudo == valor:
                    no.color = "green"

                    tela.blit(tela3, (0, 0))

                    if mode == 0:
                        txt = FONT2.render(str(i), True, "blue")
                        tela.blit(txt, (965, 200))
                    if mode == 1:
                        txt = FONT2.render(str(no.conteudo), True, "blue")
                        tela.blit(txt, (965, 200))

                    printar_tela()

                    pygame.display.update()

                    time.sleep(3)

                    no.color = "black"

                    break
                else:
                    no.color = "blue"

                    tela.blit(tela3, (0, 0))

                    printar_tela()   

                    pygame.display.update()

                    no.color = "black"

                    time.sleep(0.5)
        elif mode == 1:
            if valor == self.nElementos:
                if self.dados[valor-1].posicao[0] > largura:
                    offsetx -= 240*(valor-5)

                self.dados[valor-1].color = "green"

                tela.blit(tela3, (0, 0))

                if mode == 0:
                    txt = FONT2.render(str(i), True, "blue")
                    tela.blit(txt, (965, 200))
                if mode == 1:
                    txt = FONT2.render(str(self.dados[valor-1].conteudo), True, "blue")
                    tela.blit(txt, (965, 200))

                printar_tela()

                pygame.display.update()

                time.sleep(3)

                self.dados[valor-1].color = "black"
            elif valor > self.nElementos/2:
                if self.dados[self.nElementos-1].posicao[0] > largura:
                    offsetx -= 240*(self.nElementos-5)
                
                for pos in range(self.nElementos-1, valor-1, -1):
                    if self.dados[pos].posicao[0] + offsetx < 0:
                        offsetx += 240

                    self.dados[pos].color = "blue"

                    tela.blit(tela3, (0, 0))

                    printar_tela()   

                    pygame.display.update()

                    self.dados[pos].color = "black"

                    time.sleep(0.5)

                    if pos != valor:
                        continue

                    if self.dados[pos-1].posicao[0] + offsetx < 0:
                        offsetx += 240

                    self.dados[pos-1].color = "green"

                    tela.blit(tela3, (0, 0))

                    if mode == 0:
                        txt = FONT2.render(str(i), True, "blue")
                        tela.blit(txt, (965, 200))
                    if mode == 1:
                        txt = FONT2.render(str(self.dados[pos-1].conteudo), True, "blue")
                        tela.blit(txt, (965, 200))

                    printar_tela()

                    pygame.display.update()

                    time.sleep(3)

                    self.dados[pos-1].color = "black"
            else:
                for no in self.dados:
                    i += 1

                    if no.posicao[0] > largura:
                        offsetx -= 240

                    if (no.conteudo == valor and mode == 0) or (i == valor and mode == 1):
                        no.color = "green"

                        tela.blit(tela3, (0, 0))

                        if mode == 0:
                            txt = FONT2.render(str(i), True, "blue")
                            tela.blit(txt, (965, 200))
                        if mode == 1:
                            txt = FONT2.render(str(no.conteudo), True, "blue")
                            tela.blit(txt, (965, 200))

                        printar_tela()

                        pygame.display.update()

                        time.sleep(3)

                        no.color = "black"

                        break
                    else:
                        no.color = "blue"

                        tela.blit(tela3, (0, 0))

                        printar_tela()   

                        pygame.display.update()

                        no.color = "black"

                        time.sleep(0.5)

class listaSeq:

    def __init__(self):
        self.dados = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        self.nElementos = 0

    def vazia(self):
        if self.nElementos == 0:
            return True
        else:
            return False
        
    def cheia(self):
        if self.nElementos == 22:
            return True
        else:
            return False
        
    def tamanho(self):
        return self.nElementos
    
    def elemento(self, pos):
        if pos > 22 or pos <= 0:
            return -1
        else:
            return self.dados[pos-1]
        
    def posicao(self, valor):
        i = 0

        for elemento in self.dados:
            if elemento == valor:
                return i + 1
            
            i += 1

        return -1
    
    def insere(self, valor, pos):
        if  self.cheia() or pos > self.nElementos+1 or pos <= 0:
            return False
        
        if self.dados[pos - 1] == None:
            self.dados[pos - 1] = valor
            self.nElementos += 1
            return True
        
        i = 21
        
        while i >= pos:
            self.dados[i] = self.dados[i-1]

            i -= 1

        self.dados[pos - 1] = valor

        self.nElementos += 1

        return True
    
    def remove(self, pos):
        if pos > self.nElementos or pos <= 0:
            return -1
        
        if pos == 22:
            self.dados[21] = None
        
        aux = self.dados[pos - 1]

        for i in range(pos - 1, 21):
            self.dados[i] = self.dados[i+1]

        self.nElementos -= 1

        self.dados[21] = None

        return aux
    
class imprimeListaSeq:
    def __init__(self, lista):
        self.X = [110, 210, 320, 420, 520, 625, 725, 830, 935, 1035, 1140]
        self.Ycima = 605
        self.Ybaixo = 810
        self.lista = lista

    def imprimir(self):
        i = 0

        for elemento in self.lista:
            if elemento != None:
                txt = FONT.render(str(elemento), True, "red")
                x = self.X[i % 11]
                if i > 10:
                    y = self.Ybaixo
                else:
                    y = self.Ycima
                
                tela.blit(txt, (x - str(elemento).__len__()*6, y))

            i += 1

    def procurar(self, enable, mode, valor):
        i = 0
        
        if enable:
            if mode == 1:
                for elemento in self.lista:
                    if elemento != None:
                        tela.blit(tela1, (0, 0))

                        for box in input_boxes1:
                            box.draw(tela)

                        if flag_erro1 == 1:
                            tela.blit(txt_erro, (200, 200))

                        if flag_erro2 == 1:
                            tela.blit(txt_erro, (610, 200))

                        if flag_erro3 == 1:
                            tela.blit(txt_erro, (965, 200))

                        pygame.draw.rect(tela, "grey", (185, 415, 83, 32))
                        pygame.draw.rect(tela, "grey", (186, 416, 81, 30))
                        tela.blit(txt_inserir, (191, 421))

                        pygame.draw.rect(tela, "grey", (585, 415, 100, 32))
                        pygame.draw.rect(tela, "grey", (586, 416, 98, 30))
                        tela.blit(txt_remover, (591, 421))

                        pygame.draw.rect(tela, "grey", (955, 415, 115, 32))
                        pygame.draw.rect(tela, "grey", (956, 416, 113, 30))
                        tela.blit(txt_consultar, (961, 421))

                        self.imprimir()
                    
                        x = self.X[i % 11] + 10
                        if i > 10:
                            y = self.Ybaixo + 10
                        else:
                            y = self.Ycima + 10

                        pygame.draw.circle(tela, "red", (x, y), 50, 2)

                    pygame.display.update()

                    if elemento == int(valor):
                        pygame.draw.circle(tela, "blue", (x, y), 50, 5)

                        txt = FONT2.render(str(i+1), True, "blue")
                        tela.blit(txt, (965, 200))

                        pygame.display.update()

                        time.sleep(3)
                        break
                    else: 
                        time.sleep(0.5)

                    if elemento == None:
                        break                    

                    i += 1
            elif mode == 2:
                elemento = listaseq.dados[int(valor)-1]

                x = self.X[(int(valor)-1) % 11] + 10
                if int(valor) > 11:
                    y = self.Ybaixo + 10
                else:
                    y = self.Ycima + 10

                pygame.draw.circle(tela, "blue", (x, y), 50, 5)

                txt = FONT2.render(str(elemento), True, "blue")
                tela.blit(txt, (965, 200))

                pygame.display.update()

                time.sleep(3)

class InputBox: 

    def __init__(self, x, y, w, h, text=''):
        self.minW = w
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def returnText(self):
        try:
            int(self.text)
            return self.text
        except:
            return ""

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.minW, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Node:
    def __init__(self, data):
        self.left_child = None
        self.right_child = None
        self.data = data
        self.parent = None
        self.color = "black"
        self.x = 0
        self.y = 0

def print_tela_arvore():
    tela.blit(tela6, (0, 0))

    for box in input_boxes4:
        box.draw(tela)

    if 375 <= mouse[0] <= 458 and 327 <= mouse[1] <= 359: #INSERIR
        color2 = "black"

    else:
        color2 = "white"

    pygame.draw.rect(tela, color2, (375, 327, 83, 32))
    pygame.draw.rect(tela, "grey", (376, 328, 81, 30))
    tela.blit(txt_inserir, (381, 333))

    if 778 <= mouse[0] <= 878 and 328 <= mouse[1] <= 358: #REMOVER
        color3 = "black"

    else:
        color3 = "white"

    pygame.draw.rect(tela, color3, (778, 328, 100, 32))
    pygame.draw.rect(tela, "grey", (779, 329, 98, 30))
    tela.blit(txt_remover, (784, 334))

    if 20 <= mouse[0] <= 110 and 20 <= mouse[1] <= 105:
        color1 = "black"

    else:
        color1 = "white"

    pygame.draw.rect(tela, color1, (20, 20, 90, 85), 2)

def insert(root_node, value):
    new_node = Node(value)
    if root_node is None:
        root_node = new_node
    else:
        current_node = root_node
        while True:
            current_node.color = "blue"
            space = pow(2, get_height(root)-2) * node_radius
            print_tela_arvore()
            draw_tree(root, 600, 435, space)
            pygame.display.update()
            time.sleep(0.8)
            current_node.color = "black"

            if value < current_node.data:
                if current_node.left_child is None:
                    current_node.left_child = new_node
                    new_node.parent = current_node
                    break
                else:
                    current_node = current_node.left_child
            else:
                if current_node.right_child is None:
                    current_node.right_child = new_node
                    new_node.parent = current_node
                    break
                else:
                    current_node = current_node.right_child
    for event in pygame.event.get():
        pass

    return root_node

def find_node(value, root_node):
    current_node = root_node
    while current_node is not None:
        current_node.color = "blue"
        space = pow(2, get_height(root)-2) * node_radius
        print_tela_arvore()
        draw_tree(root, 600, 435, space)
        pygame.display.update()
        time.sleep(0.8)
        current_node.color = "black"

        if value == current_node.data:
            return current_node
        elif value < current_node.data:
            current_node = current_node.left_child
        else:
            current_node = current_node.right_child
    return None

def find_min_node(node):
    while node.left_child is not None:
        node = node.left_child
    return node

def remove_tree(value, root_node):
    node_to_remove = find_node(value, root_node)
    if node_to_remove is None:
        return root_node
    
    if node_to_remove.left_child is None and node_to_remove.right_child is None:
        if node_to_remove.parent is None:
            root_node = None
        elif node_to_remove.parent.left_child == node_to_remove:
            node_to_remove.parent.left_child = None
        else:
            node_to_remove.parent.right_child = None
            
    elif node_to_remove.left_child is None:
        if node_to_remove.parent is None:
            root_node = node_to_remove.right_child
            root_node.parent = None
        elif node_to_remove.parent.left_child == node_to_remove:
            node_to_remove.parent.left_child = node_to_remove.right_child
            node_to_remove.right_child.parent = node_to_remove.parent
        else:
            node_to_remove.parent.right_child = node_to_remove.right_child
            node_to_remove.right_child.parent = node_to_remove.parent
            
    elif node_to_remove.right_child is None:
        if node_to_remove.parent is None:
            root_node = node_to_remove.left_child
            root_node.parent = None
        elif node_to_remove.parent.left_child == node_to_remove:
            node_to_remove.parent.left_child = node_to_remove.left_child
            node_to_remove.left_child.parent = node_to_remove.parent
        else:
            node_to_remove.parent.right_child = node_to_remove.left_child
            node_to_remove.left_child.parent = node_to_remove.parent
            
    else:
        successor = find_min_node(node_to_remove.right_child)
        remove_tree(successor.data, node_to_remove.right_child)
        node_to_remove.data = successor.data
    
    for event in pygame.event.get():
        pass
    
    return root_node

node_radius = 25
height_difference = 100

def draw_tree(node, x, y, space):
    if node is not None:
        pygame.draw.circle(tela, node.color, (x, y), node_radius)
        node.x = x
        node.y = y
        font = pygame.font.Font(None, 25)
        text = font.render(str(node.data), 1, "red")
        textpos = text.get_rect(centerx=x, centery=y)
        tela.blit(text, textpos)
        if node.left_child is not None:
            draw_arrow(tela, "red", (x, y+node_radius), (x-space, y+height_difference-node_radius))
            draw_tree(node.left_child, x-space, y+height_difference, space/2)
        if node.right_child is not None:
            draw_arrow(tela, "red", (x, y+node_radius), (x+space, y+height_difference-node_radius))
            draw_tree(node.right_child, x+space, y+height_difference, space/2)

def get_height(root):
    if root is None:
        return 0
    else:
        left_height = get_height(root.left_child)
        right_height = get_height(root.right_child)
        return max(left_height, right_height) + 1

#################################################################################################################################################
################################################              VARIAVEIS              ############################################################
#################################################################################################################################################

txt_inserir = FONT.render("inserir", True, "black")
txt_remover = FONT.render("remover", True, "black")
txt_consultar = FONT.render("consultar", True, "black")
txt_erro = FONT.render("ERRO", True, "red")

input_box1 = InputBox(145, 310, 170, 32)
input_box2 = InputBox(145, 360, 170, 32)
input_box3 = InputBox(550, 320, 190, 32)
input_box4 = InputBox(910, 310, 200, 32)
input_box5 = InputBox(910, 360, 200, 32)
input_boxes1 = [input_box1, input_box2, input_box3, input_box4, input_box5]

input_box6 = InputBox(145, 310, 170, 32)
input_box7 = InputBox(145, 360, 170, 32)
input_box8 = InputBox(550, 320, 190, 32)
input_box9 = InputBox(910, 310, 200, 32)
input_box10 = InputBox(910, 360, 200, 32)
input_boxes2 = [input_box6, input_box7, input_box8, input_box9, input_box10]

input_box11 = InputBox(145, 310, 170, 32)
input_box12 = InputBox(145, 360, 170, 32)
input_box13 = InputBox(550, 320, 190, 32)
input_box14 = InputBox(910, 310, 200, 32)
input_box15 = InputBox(910, 360, 200, 32)
input_boxes3 = [input_box11, input_box12, input_box13, input_box14, input_box15]

input_box16 = InputBox(335, 260, 170, 32)
input_box17 = InputBox(735, 260, 190, 32)
input_boxes4 = [input_box16, input_box17]

offset_increment = 0
offset_decrement = 0
offsetx = 0

content1 = ''
content2 = ''
content3 = ''
content4 = ''
content5 = ''
flag_erro1 = 0
flag_erro2 = 0
flag_erro3 = 0

content6 = ''
content7 = ''
content8 = ''
content9 = ''
content10 = ''
flag_erro4 = 0
flag_erro5 = 0
flag_erro6 = 0

content11 = ''
content12 = ''
content13 = ''
content14 = ''
content15 = ''
flag_erro7 = 0
flag_erro8 = 0
flag_erro9 = 0

content16 = ''
content17 = ''

listaseq = listaSeq()
imp = imprimeListaSeq(listaseq.dados)
enable_procurar = 0
valor_procurar = None
mode_procurar = 0

listaS = listaSE()

listade = listaDE()

root = None

tela0 = pygame.image.load('tela0.png')
tela1 = pygame.image.load('tela1.png')
tela2 = pygame.image.load('tela2.png')
tela3 = pygame.image.load('tela3.png')
tela6 = pygame.image.load('tela6.png')

pagina = 0

relogio = pygame.time.Clock()

def movimento_adicionar_no(pos, valor):
    offsetx1 = 0

    def printTela():
        tela.blit(tela2, (0, 0))

        if flag_erro4 == 1:
            tela.blit(txt_erro, (200, 200))

        if flag_erro5 == 1:
            tela.blit(txt_erro, (610, 200))

        if flag_erro6 == 1:
            tela.blit(txt_erro, (965, 200))

        pygame.draw.rect(tela, color2, (185, 415, 83, 32))
        pygame.draw.rect(tela, "grey", (186, 416, 81, 30))
        tela.blit(txt_inserir, (191, 421))
        pygame.draw.rect(tela, color3, (585, 415, 100, 32))
        pygame.draw.rect(tela, "grey", (586, 416, 98, 30))
        tela.blit(txt_remover, (591, 421))
        pygame.draw.rect(tela, color4, (955, 415, 115, 32))
        pygame.draw.rect(tela, "grey", (956, 416, 113, 30))
        tela.blit(txt_consultar, (961, 421))

        for box in input_boxes2:
            box.draw(tela)

    listaTemp = copy.deepcopy(listaS)

    if listaTemp.tamanho() == 0:
        return

    if pos == listaTemp.tamanho() + 1:
        offsetx1 = 0

        for no in listaTemp.dados:
            if no.posicao[0] > 1280:
                offsetx1 -= 240

                if no == listaTemp.dados[pos-2]:
                    offsetx1 -= 240

            no.color = "blue"
            printTela()
            listaTemp.imprimirLista(offsetx1)
            pygame.display.update()
            time.sleep(0.8)
            no.color = "black"

        listaTemp.insere(valor, pos)
        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)

        return

    novoNo = NoS(valor, (listaTemp.dados[pos-1].posicao[0], listaTemp.dados[pos-1].posicao[1] + 170))

    finished = 0
    final_pos = listaTemp.dados[pos-1].posicao[0] + 240
    final_pos2 = listaTemp.dados[pos-1].posicao[1]

    offsetx1 = 0

    if listaTemp.dados[pos-1].posicao[0] > 1280:
        offsetx1 = -240*(pos-3)

    while not finished:
        for i in range(pos-1, listaTemp.nElementos):
            listaTemp.dados[i].posicao = (listaTemp.dados[i].posicao[0] + 0.5, listaTemp.dados[i].posicao[1])

            if listaTemp.dados[i].prox != (None, None):
                listaTemp.dados[i].prox = (listaTemp.dados[i].prox[0] + 0.5, listaTemp.dados[i].prox[1])

            listaTemp.dados[pos-2].prox = (listaTemp.dados[pos-1].posicao[0] - 60, listaTemp.dados[pos-2].prox[1])
        
        printTela()

        novoNo.printarNo(offsetx1)
        listaTemp.imprimirLista(offsetx1)
            
        pygame.display.update()

        if listaTemp.dados[pos-1].posicao[0] == final_pos:
            finished = 1

    time.sleep(0.5)

    offsetx1 = 0

    if pos != 1:
        for i in range(0, pos):
            if listaTemp.dados[i].posicao[0] > 1280:
                if i == pos-1:
                    offsetx1 -= 480
                else:
                    offsetx1 -= 240
        
            listaTemp.dados[i].color = "blue"
            printTela()
            listaTemp.imprimirLista(offsetx1)
            novoNo.printarNo(offsetx1)
            pygame.display.update()
            time.sleep(0.8)

            if i < pos-1:
                listaTemp.dados[i].color = "black"

    if pos == 1:
        delay = 0
    else:
        delay = 1

    novoNo.prox = (listaTemp.dados[pos-1].posicao[0] - 60, listaTemp.dados[pos-1].posicao[1])
    novoNo.printarNo(offsetx1)
    pygame.display.update()
    time.sleep(0.8)

    listaTemp.dados[pos-2].prox = (novoNo.posicao[0] - 60, novoNo.posicao[1])
    printTela()
    listaTemp.imprimirLista(offsetx1)
    novoNo.printarNo(offsetx1)
    pygame.display.update()
    time.sleep(delay)

    finished = 0

    listaTemp.dados[pos-1].color = "black"

    while not finished:
        novoNo.posicao = (novoNo.posicao[0], novoNo.posicao[1] - 1)
        listaTemp.dados[pos-2].prox = (novoNo.posicao[0] - 60, novoNo.posicao[1])
        printTela()
        novoNo.printarNo(offsetx1)
        listaTemp.imprimirLista(offsetx1)

        if novoNo.posicao[1] == final_pos2:
            finished = 1

        pygame.display.update()

    for event in pygame.event.get():
        pass

def movimento_adicionar_no_2(pos, valor):
    offsetx1 = 0

    def printTela():
        tela.blit(tela3, (0, 0))

        if flag_erro7 == 1:
            tela.blit(txt_erro, (200, 200))

        if flag_erro8 == 1:
            tela.blit(txt_erro, (610, 200))

        if flag_erro9 == 1:
            tela.blit(txt_erro, (965, 200))

        pygame.draw.rect(tela, color2, (185, 415, 83, 32))
        pygame.draw.rect(tela, "grey", (186, 416, 81, 30))
        tela.blit(txt_inserir, (191, 421))
        pygame.draw.rect(tela, color3, (585, 415, 100, 32))
        pygame.draw.rect(tela, "grey", (586, 416, 98, 30))
        tela.blit(txt_remover, (591, 421))
        pygame.draw.rect(tela, color4, (955, 415, 115, 32))
        pygame.draw.rect(tela, "grey", (956, 416, 113, 30))
        tela.blit(txt_consultar, (961, 421))

        for box in input_boxes3:
            box.draw(tela)

    listaTemp = copy.deepcopy(listade)

    if listaTemp.tamanho() == 0:
        return

    if pos == listaTemp.tamanho() + 1:
        offsetx1 = 0

        if listaTemp.dados[listaTemp.tamanho()-1].posicao[0] > largura:
            offsetx1 -= 240*(listaTemp.tamanho()-6)

        listaTemp.dados[listaTemp.tamanho()-1].color = "blue"
        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)
        listaTemp.dados[listaTemp.tamanho()-1].color = "black"

        listaTemp.insere(valor, pos)
        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)

        return

    novoNo = NoD(valor, (listaTemp.dados[pos-1].posicao[0], listaTemp.dados[pos-1].posicao[1] + 170))

    finished = 0
    final_pos = listaTemp.dados[pos-1].posicao[0] + 240
    final_pos2 = listaTemp.dados[pos-1].posicao[1]

    offsetx1 = 0

    if listaTemp.dados[pos-1].posicao[0] > 1280:
        offsetx1 = -240*(pos-3)

    while not finished:
        for i in range(pos-1, listaTemp.nElementos):
            listaTemp.dados[i].posicao = (listaTemp.dados[i].posicao[0] + 0.5, listaTemp.dados[i].posicao[1])

            if listaTemp.dados[i].prox != (None, None):
                listaTemp.dados[i].prox = (listaTemp.dados[i].prox[0] + 0.5, listaTemp.dados[i].prox[1])

            if listaTemp.dados[i].ant != (None, None) and listaTemp.dados[i] != listaTemp.dados[pos-1]:
                listaTemp.dados[i].ant = (listaTemp.dados[i].ant[0] + 0.5, listaTemp.dados[i].ant[1])

            listaTemp.dados[pos-2].prox = (listaTemp.dados[pos-1].posicao[0] - 60, listaTemp.dados[pos-2].prox[1])
        
        printTela()

        novoNo.printarNo(offsetx1)
        listaTemp.imprimirLista(offsetx1)
            
        pygame.display.update()

        if listaTemp.dados[pos-1].posicao[0] == final_pos:
            finished = 1

    time.sleep(0.5)

    offsetx1 = 0

    if pos != 1:
        if pos > listaTemp.tamanho()/2:
            if listaTemp.dados[pos-1].posicao[0] > largura:
                offsetx1 -= 240*(listaTemp.tamanho()-3)

            for i in range(listaTemp.tamanho()-1, pos-2, -1):
                if listaTemp.dados[i].posicao[0] + offsetx1 < 0:
                        offsetx1 += 240
            
                listaTemp.dados[i].color = "blue"
                printTela()
                listaTemp.imprimirLista(offsetx1)
                novoNo.printarNo(offsetx1)
                pygame.display.update()
                time.sleep(0.8)

                if i > pos-1:
                    listaTemp.dados[i].color = "black"
        else:
            for i in range(0, pos):
                if listaTemp.dados[i].posicao[0] > 1280:
                    if i == pos-1:
                        offsetx1 -= 480
                    else:
                        offsetx1 -= 240
            
                listaTemp.dados[i].color = "blue"
                printTela()
                listaTemp.imprimirLista(offsetx1)
                novoNo.printarNo(offsetx1)
                pygame.display.update()
                time.sleep(0.8)

                if i < pos-1:
                    listaTemp.dados[i].color = "black"

    novoNo.prox = (listaTemp.dados[pos-1].posicao[0] - 60, listaTemp.dados[pos-1].posicao[1])
    if pos != 1:
        novoNo.ant = (listaTemp.dados[pos-2].posicao[0] + 60, listaTemp.dados[pos-2].posicao[1])
    novoNo.printarNo(offsetx1)
    pygame.display.update()
    time.sleep(0.8)

    listaTemp.dados[pos-2].prox = (novoNo.posicao[0] - 60, novoNo.posicao[1])
    listaTemp.dados[pos-1].ant = (novoNo.posicao[0] + 60, novoNo.posicao[1])
    printTela()
    listaTemp.imprimirLista(offsetx1)
    novoNo.printarNo(offsetx1)
    pygame.display.update()
    time.sleep(0.8)

    finished = 0

    listaTemp.dados[pos-1].color = "black"

    while not finished:
        novoNo.posicao = (novoNo.posicao[0], novoNo.posicao[1] - 1)
        listaTemp.dados[pos-2].prox = (novoNo.posicao[0] - 60, novoNo.posicao[1])
        listaTemp.dados[pos-1].ant = (novoNo.posicao[0] + 60, novoNo.posicao[1])
        printTela()
        novoNo.printarNo(offsetx1)
        listaTemp.imprimirLista(offsetx1)

        if novoNo.posicao[1] == final_pos2:
            finished = 1

        pygame.display.update()

    for event in pygame.event.get():
        pass

def movimento_remover_no(pos):
    offsetx1 = 0

    def printTela():
        tela.blit(tela2, (0, 0))

        if flag_erro4 == 1:
            tela.blit(txt_erro, (200, 200))

        if flag_erro5 == 1:
            tela.blit(txt_erro, (610, 200))

        if flag_erro6 == 1:
            tela.blit(txt_erro, (965, 200))

        pygame.draw.rect(tela, color2, (185, 415, 83, 32))
        pygame.draw.rect(tela, "grey", (186, 416, 81, 30))
        tela.blit(txt_inserir, (191, 421))
        pygame.draw.rect(tela, color3, (585, 415, 100, 32))
        pygame.draw.rect(tela, "grey", (586, 416, 98, 30))
        tela.blit(txt_remover, (591, 421))
        pygame.draw.rect(tela, color4, (955, 415, 115, 32))
        pygame.draw.rect(tela, "grey", (956, 416, 113, 30))
        tela.blit(txt_consultar, (961, 421))

        for box in input_boxes2:
            box.draw(tela)

    listaTemp = copy.deepcopy(listaS)

    if pos == 1 and listaTemp.tamanho() == 1:
        return
    elif pos == 1:
        offsetx1 = 0

        printTela()  
        listaTemp.dados[0].color = "blue"
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)

        listaTemp.dados[0].color = "black"
        listaTemp.dados[1].color = "blue"
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(1)
        
        final_pos = listaTemp.dados[0].posicao[0]

        listaTemp.remove(1)

        for no in listaTemp.dados:
            no.posicao = (no.posicao[0] + 240, no.posicao[1])
            no.prox = (no.prox[0] + 240, no.prox[1])

        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)

        while listaTemp.dados[0].posicao[0] != final_pos:
            for no in listaTemp.dados:
                no.posicao = (no.posicao[0] - 1, no.posicao[1])
                if no.prox != (None, None):
                    no.prox = (no.prox[0] - 1, no.prox[1])

            printTela()
            listaTemp.imprimirLista(offsetx1)
            pygame.display.update()

    elif pos < listaTemp.tamanho():
        offsetx1 = 0

        final_pos = listaTemp.dados[pos-1].posicao[1] + 170
        final_pos2 = listaTemp.dados[pos-1].posicao[0]

        if listaTemp.dados[pos-1].posicao[0] > 1280:
            offsetx1 = -240*(pos-4)

        while listaTemp.dados[pos-1].posicao[1] != final_pos:
            listaTemp.dados[pos-1].posicao = (listaTemp.dados[pos-1].posicao[0], listaTemp.dados[pos-1].posicao[1] + 1)
            listaTemp.dados[pos-2].prox = (listaTemp.dados[pos-1].posicao[0] - 60, listaTemp.dados[pos-1].posicao[1])
            printTela()
            listaTemp.imprimirLista(offsetx1)
            pygame.display.update()

        offsetx1 = 0

        time.sleep(0.8)

        for i in range(0, pos+1):
            if listaTemp.dados[i].posicao[0] > 1280:
                offsetx1 -= 240

            listaTemp.dados[i].color = "blue"
            printTela()
            listaTemp.imprimirLista(offsetx1)
            pygame.display.update()
            time.sleep(0.8)
            if i != pos+1:
                listaTemp.dados[i].color = "black"

        listaTemp.dados[pos-2].prox = (listaTemp.dados[pos].posicao[0] - 60, listaTemp.dados[pos].posicao[1])
        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)

        listaTemp.remove(pos)

        for i in range(pos-1, listaTemp.tamanho()):
            listaTemp.dados[i].posicao = (listaTemp.dados[i].posicao[0] + 240, listaTemp.dados[i].posicao[1])
            listaTemp.dados[i].prox = (listaTemp.dados[i].prox[0] + 240, listaTemp.dados[i].prox[1])
        
        listaTemp.dados[pos-2].prox = (listaTemp.dados[pos-1].posicao[0] - 60, listaTemp.dados[pos-1].posicao[1])
        
        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)

        while listaTemp.dados[pos-1].posicao[0] != final_pos2:
            for i in range(pos-1, listaTemp.tamanho()):
                listaTemp.dados[i].posicao = (listaTemp.dados[i].posicao[0] - 1, listaTemp.dados[i].posicao[1])
                if listaTemp.dados[i].prox != (None, None):
                    listaTemp.dados[i].prox = (listaTemp.dados[i].prox[0] - 1, listaTemp.dados[i].prox[1])

            listaTemp.dados[pos-2].prox = (listaTemp.dados[pos-2].prox[0] - 1, listaTemp.dados[pos-2].prox[1])

            printTela()
            listaTemp.imprimirLista(offsetx1)
            pygame.display.update()

    elif pos == listaTemp.tamanho():
        offsetx1 = 0

        for i in range(0, listaTemp.tamanho() - 1):
            if listaTemp.dados[i].posicao[0] > 1280:
                offsetx1 -= 240
                if i == listaTemp.tamanho() - 2:
                    offsetx1 -= 140

            listaTemp.dados[i].color = "blue"
            printTela()
            listaTemp.imprimirLista(offsetx1)
            pygame.display.update()
            time.sleep(0.8)
            if i != listaTemp.tamanho() - 2:
                listaTemp.dados[i].color = "black"

        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        
        time.sleep(0.5)

        listaTemp.dados[pos-2].prox = (None, None)
        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(1)

    for event in pygame.event.get():
        pass

def movimento_remover_no_2(pos):
    offsetx1 = 0

    def printTela():
        tela.blit(tela3, (0, 0))

        if flag_erro4 == 1:
            tela.blit(txt_erro, (200, 200))

        if flag_erro5 == 1:
            tela.blit(txt_erro, (610, 200))

        if flag_erro6 == 1:
            tela.blit(txt_erro, (965, 200))

        pygame.draw.rect(tela, color2, (185, 415, 83, 32))
        pygame.draw.rect(tela, "grey", (186, 416, 81, 30))
        tela.blit(txt_inserir, (191, 421))
        pygame.draw.rect(tela, color3, (585, 415, 100, 32))
        pygame.draw.rect(tela, "grey", (586, 416, 98, 30))
        tela.blit(txt_remover, (591, 421))
        pygame.draw.rect(tela, color4, (955, 415, 115, 32))
        pygame.draw.rect(tela, "grey", (956, 416, 113, 30))
        tela.blit(txt_consultar, (961, 421))

        for box in input_boxes3:
            box.draw(tela)

    listaTemp = copy.deepcopy(listade)
    if pos == listaTemp.tamanho():
        if listaTemp.dados[pos-1].posicao[0] > largura:
            offsetx1 = -240*(pos-4)

        printTela()  
        listaTemp.dados[pos-1].color = "blue"
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)

        printTela()  
        listaTemp.dados[pos-1].color = "black"
        listaTemp.dados[pos-2].color = "blue"
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)

        return
    elif pos == 1 and listaTemp.tamanho() == 1:
        return
    elif pos == 1:
        offsetx1 = 0

        printTela()  
        listaTemp.dados[0].color = "blue"
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)

        listaTemp.dados[0].color = "black"
        listaTemp.dados[1].color = "blue"
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(1)
        
        final_pos = listaTemp.dados[0].posicao[0]

        listaTemp.remove(1)
        for no in listaTemp.dados:
            if no.ant != (None, None):
                no.ant = (no.ant[0] + listaTemp.distancia_proxima_seta + 60, no.ant[1])

        for no in listaTemp.dados:
            no.posicao = (no.posicao[0] + 240, no.posicao[1])
            no.prox = (no.prox[0] + 240, no.prox[1])

        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)

        while listaTemp.dados[0].posicao[0] != final_pos:
            for no in listaTemp.dados:
                no.posicao = (no.posicao[0] - 1, no.posicao[1])
                if no.prox != (None, None):
                    no.prox = (no.prox[0] - 1, no.prox[1])
                if no.ant != (None, None):
                    no.ant = (no.ant[0] - 1, no.ant[1])

            printTela()
            listaTemp.imprimirLista(offsetx1)
            pygame.display.update()

    elif pos < listaTemp.tamanho():
        offsetx1 = 0

        final_pos = listaTemp.dados[pos-1].posicao[1] + 170
        final_pos2 = listaTemp.dados[pos-1].posicao[0]

        if listaTemp.dados[pos-1].posicao[0] > 1280:
            offsetx1 = -240*(pos-3)

        while listaTemp.dados[pos-1].posicao[1] != final_pos:
            listaTemp.dados[pos-1].posicao = (listaTemp.dados[pos-1].posicao[0], listaTemp.dados[pos-1].posicao[1] + 1)
            listaTemp.dados[pos-2].prox = (listaTemp.dados[pos-1].posicao[0] - 60, listaTemp.dados[pos-1].posicao[1])
            if pos < listaTemp.tamanho():
                listaTemp.dados[pos].ant = (listaTemp.dados[pos-1].posicao[0] + 60, listaTemp.dados[pos-1].posicao[1])
            printTela()
            listaTemp.imprimirLista(offsetx1)
            pygame.display.update()

        time.sleep(0.8)

        if pos > listaTemp.tamanho()/2:
            for i in range(listaTemp.tamanho()-1, pos-3, -1):
                if listaTemp.dados[i].posicao[0] > 1280:
                    offsetx1 += 240

                listaTemp.dados[i].color = "blue"
                printTela()
                listaTemp.imprimirLista(offsetx1)
                pygame.display.update()
                time.sleep(0.8)
                if i != pos-2:
                    listaTemp.dados[i].color = "black"
        else:
            for i in range(0, pos+1):
                if listaTemp.dados[i].posicao[0] > 1280:
                    offsetx1 -= 240

                listaTemp.dados[i].color = "blue"
                printTela()
                listaTemp.imprimirLista(offsetx1)
                pygame.display.update()
                time.sleep(0.8)
                if i != pos+1:
                    listaTemp.dados[i].color = "black"

        listaTemp.dados[pos-2].prox = (listaTemp.dados[pos].posicao[0] - 60, listaTemp.dados[pos].posicao[1])
        if pos < listaTemp.tamanho():
            listaTemp.dados[pos].ant = (listaTemp.dados[pos-2].posicao[0] + 60, listaTemp.dados[pos-2].posicao[1])
        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)

        listaTemp.remove(pos)

        for i in range(pos-1, listaTemp.tamanho()):
            listaTemp.dados[i].posicao = (listaTemp.dados[i].posicao[0] + 240, listaTemp.dados[i].posicao[1])
            listaTemp.dados[i].prox = (listaTemp.dados[i].prox[0] + 240, listaTemp.dados[i].prox[1])
            listaTemp.dados[i].ant = (listaTemp.dados[i].ant[0] + 240, listaTemp.dados[i].ant[1])
        
        listaTemp.dados[pos-2].prox = (listaTemp.dados[pos-1].posicao[0] - 60, listaTemp.dados[pos-1].posicao[1])
        listaTemp.dados[pos-1].ant = (listaTemp.dados[pos-2].posicao[0] + 60, listaTemp.dados[pos-2].posicao[1])
        
        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(0.8)

        while listaTemp.dados[pos-1].posicao[0] != final_pos2:
            for i in range(pos-1, listaTemp.tamanho()):
                listaTemp.dados[i].posicao = (listaTemp.dados[i].posicao[0] - 1, listaTemp.dados[i].posicao[1])
                if listaTemp.dados[i].prox != (None, None):
                    listaTemp.dados[i].prox = (listaTemp.dados[i].prox[0] - 1, listaTemp.dados[i].prox[1])
                if listaTemp.dados[i].ant != (None, None):
                    listaTemp.dados[i].ant = (listaTemp.dados[i].ant[0] - 1, listaTemp.dados[i].ant[1])

            listaTemp.dados[pos-2].prox = (listaTemp.dados[pos-2].prox[0] - 1, listaTemp.dados[pos-2].prox[1])
            listaTemp.dados[pos-1].ant = (listaTemp.dados[pos-2].posicao[0] + 60, listaTemp.dados[pos-2].posicao[1])

            printTela()
            listaTemp.imprimirLista(offsetx1)
            pygame.display.update()

    elif pos == listaTemp.tamanho():
        offsetx1 = 0

        for i in range(0, listaTemp.tamanho() - 1):
            if listaTemp.dados[i].posicao[0] > 1280:
                offsetx1 -= 240
                if i == listaTemp.tamanho() - 2:
                    offsetx1 -= 140

            listaTemp.dados[i].color = "blue"
            printTela()
            listaTemp.imprimirLista(offsetx1)
            pygame.display.update()
            time.sleep(0.8)
            if i != listaTemp.tamanho() - 2:
                listaTemp.dados[i].color = "black"

        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        
        time.sleep(0.5)

        listaTemp.dados[pos-2].prox = (None, None)
        printTela()
        listaTemp.imprimirLista(offsetx1)
        pygame.display.update()
        time.sleep(1)

    for event in pygame.event.get():
        pass

def highlight_button(cd1, cd2, cd3, cd4):
    if cd1 <= mouse[0] <= cd2 and cd3 <= mouse[1] <= cd4:
        color = "black"
    else:
        color = "white"
    
    return color

def highlight_boxes(b_arrows, b_consultar, b_pagina6 = 0):
    if b_pagina6:
        color2 = highlight_button(375, 458, 327, 359) #INSERIR

        pygame.draw.rect(tela, color2, (375, 327, 83, 32))
        pygame.draw.rect(tela, "grey", (376, 328, 81, 30))
        tela.blit(txt_inserir, (381, 333))

        color3 = highlight_button(778, 878, 328, 358) #INSERIR

        pygame.draw.rect(tela, color3, (778, 328, 100, 32))
        pygame.draw.rect(tela, "grey", (779, 329, 98, 30))
        tela.blit(txt_remover, (784, 334))

    else:
        color2 = highlight_button(186, 269, 416, 446) #INSERIR

        pygame.draw.rect(tela, color2, (185, 415, 83, 32))
        pygame.draw.rect(tela, "grey", (186, 416, 81, 30))
        tela.blit(txt_inserir, (191, 421))

        color3 = highlight_button(586, 684, 416, 446) #REMOVER

        pygame.draw.rect(tela, color3, (585, 415, 100, 32))
        pygame.draw.rect(tela, "grey", (586, 416, 98, 30))
        tela.blit(txt_remover, (591, 421))

    if b_consultar:
        color4 = highlight_button(956, 1069, 416, 446) #CONSULTAR

        pygame.draw.rect(tela, color4, (955, 415, 115, 32))
        pygame.draw.rect(tela, "grey", (956, 416, 113, 30))
        tela.blit(txt_consultar, (961, 421))

    if b_arrows:
        color5 = highlight_button(473, 601, 790, 875) #SETA ESQUERDA

        pygame.draw.rect(tela, color5, (473, 790, 128, 85), 2)

        color6 = highlight_button(601, 729, 790, 875) #SETA DIREITA

        pygame.draw.rect(tela, color6, (601, 790, 128, 85), 2)

    color1 = highlight_button(20, 110, 20, 105) #VOLTAR PRA O MENU

    pygame.draw.rect(tela, color1, (20, 20, 90, 85), 2)

#################################################################################################################################################
################################################      LOOP      DO     JOGO      ################################################################
#################################################################################################################################################

while True:
    relogio.tick(60)

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get(): #EVENTOS
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN: 
            if event.key == K_LEFT: #INICIO DA LISTA SE
                offsetx = 0
            if event.key == K_RIGHT: #FINAL DA LISTA SE 
                if pagina == 2:
                    offsetx = -240*(listaS.tamanho()-5)
                elif pagina == 3:
                    offsetx = -240*(listade.tamanho()-5)
        # if event.type == MOUSEBUTTONDOWN:
        #     print("X: ", mouse[0])
        #     print("Y: ", mouse[1])
        if event.type == MOUSEBUTTONDOWN and 210 <= mouse[0] <= 685 and 270 <= mouse[1] <= 345 and pagina == 0: #BOTAO PAGINA 1
            pagina = 1
        if event.type == MOUSEBUTTONDOWN and 210 <= mouse[0] <= 1045 and 365 <= mouse[1] <= 440 and pagina == 0: #BOTAO PAGINA 2
            pagina = 2
            offsetx = 0
        if event.type == MOUSEBUTTONDOWN and 210 <= mouse[0] <= 1010 and 470 <= mouse[1] <= 545 and pagina == 0: #BOTAO PAGINA 3
            pagina = 3
            offsetx = 0
        if event.type == MOUSEBUTTONDOWN and 210 <= mouse[0] <= 850 and 765 <= mouse[1] <= 840 and pagina == 0: #BOTAO PAGINA 6
            pagina = 6
        if event.type == MOUSEBUTTONDOWN and 20 <= mouse[0] <= 110 and 20 <= mouse[1] <= 105 and (pagina == 1 or pagina == 2 or pagina == 3 or pagina == 6): #BOTAO VOLTAR MENU
            pagina = 0
        if event.type == MOUSEBUTTONDOWN and 186 <= mouse[0] <= 269 and 416 <= mouse[1] <= 446 and pagina == 1: #INSERIR PAGINA 1
            content1 = input_box1.returnText()
            content2 = input_box2.returnText()

            if content1 != "" and content2 != "":
                if listaseq.insere(int(content1), int(content2)) == False:
                    flag_erro1 = 1
                else:
                    flag_erro1 = 0

                    content1 = ''
                    content2 = ''
        if event.type == MOUSEBUTTONDOWN and 186 <= mouse[0] <= 269 and 416 <= mouse[1] <= 446 and pagina == 2: #INSERIR PAGINA 2
            content6 = input_box6.returnText()
            content7 = input_box7.returnText()

            if content6 != "" and content7 != "":
                if 0 < int(content7) <= listaS.tamanho() + 1:
                    movimento_adicionar_no(int(content7), int(content6))
                
                if listaS.insere(int(content6), int(content7)) == False:
                    flag_erro4 = 1
                else:
                    flag_erro4 = 0

                    content6 = ''
                    content7 = ''
        if event.type == MOUSEBUTTONDOWN and 186 <= mouse[0] <= 269 and 416 <= mouse[1] <= 446 and pagina == 3: #INSERIR PAGINA 3
            content11 = input_box11.returnText()
            content12 = input_box12.returnText()

            if content11 != "" and content12 != "":
                if 0 < int(content12) <= listade.tamanho() + 1:
                    movimento_adicionar_no_2(int(content12), int(content11))

                if listade.insere(int(content11), int(content12)) == False:
                    flag_erro7 = 1
                else:
                    flag_erro7 = 0

                    content11 = ''
                    content12 = ''
        if event.type == MOUSEBUTTONDOWN and 375 <= mouse[0] <= 458 and 327 <= mouse[1] <= 359 and pagina == 6: #INSERIR PAGINA 6
            content16 = input_box16.returnText()
            if content16 != "":
                root = insert(root, int(content16))
                content16 = ''
        if event.type == MOUSEBUTTONDOWN and 586 <= mouse[0] <= 684 and 416 <= mouse[1] <= 446 and pagina == 1: #REMOVER PAGINA 1
            content3 = input_box3.returnText()

            if content3 != "":
                if listaseq.remove(int(content3)) == -1:
                    flag_erro2 = 1
                else:
                    flag_erro2 = 0

                    content3 = ''
        if event.type == MOUSEBUTTONDOWN and 586 <= mouse[0] <= 684 and 416 <= mouse[1] <= 446 and pagina == 2: #REMOVER PAGINA 2
            content8 = input_box8.returnText()

            if content8 != "":
                if 0 < int(content8) < listaS.tamanho() + 1:
                    flag_erro5 = 0

                    movimento_remover_no(int(content8))

                if listaS.remove(int(content8)) == -1:
                    flag_erro5 = 1
                else:
                    flag_erro5 = 0

                    content8 = ''
        if event.type == MOUSEBUTTONDOWN and 586 <= mouse[0] <= 684 and 416 <= mouse[1] <= 446 and pagina == 3: #REMOVER PAGINA 3
            content13 = input_box13.returnText()

            if content13 != "":
                if 0 < int(content13) < listade.tamanho() + 1:
                    flag_erro8 = 0

                    movimento_remover_no_2(int(content13))

                if listade.remove(int(content13)) == -1:
                    flag_erro8 = 1
                else:
                    flag_erro8 = 0

                    content13 = ''
        if event.type == MOUSEBUTTONDOWN and 778 <= mouse[0] <= 878 and 328 <= mouse[1] <= 358 and pagina == 6: #REMOVER PAGINA 6
            content17 = input_box17.returnText()

            if content17 != "":
                root = remove_tree(int(content17), root)
        if event.type == MOUSEBUTTONDOWN and 956 <= mouse[0] <= 1069 and 416 <= mouse[1] <= 446 and pagina == 1: #CONSULTAR PAGINA 1
            content4 = input_box4.returnText()
            content5 = input_box5.returnText()

            if (content4 != "" and content5 == "") or (content4 == "" and content5 != ""):
                if content4 != "":
                    if listaseq.nElementos == 0:
                        flag_erro3 = 1
                    else:
                        valor_procurar = content4
                        mode_procurar = 1
                        enable_procurar = 1
                        flag_erro3 = 0
                elif int(content5) > listaseq.nElementos or int(content5) < 1:
                    flag_erro3 = 1
                else:
                    valor_procurar = content5
                    mode_procurar = 2
                    enable_procurar = 1
                    flag_erro3 = 0
            elif content4 == "" and content5 == "":
                flag_erro3 = 0
            else:
                flag_erro3 = 1

            if not flag_erro3:
                input_box4.text = ''
                input_box4.txt_surface = FONT.render(input_box4.text, True, input_box4.color)
                input_box5.text = ''
                input_box5.txt_surface = FONT.render(input_box5.text, True, input_box5.color)

        if event.type == MOUSEBUTTONDOWN and 956 <= mouse[0] <= 1069 and 416 <= mouse[1] <= 446 and pagina == 2: #CONSULTAR PAGINA 2
            content9 = input_box9.returnText()
            content10 = input_box10.returnText()

            if (content9 != "" and content10 == "") or (content9 == "" and content10 != ""):
                if content9 != "":
                    if listaS.nElementos == 0:
                        flag_erro6 = 1
                    else:
                        valor_procurar = content9
                        flag_erro6 = 0
                        listaS.procurar(int(valor_procurar))
                elif int(content10) > listaS.nElementos or int(content10) < 1:
                    flag_erro6 = 1
                else:
                    valor_procurar = content10
                    flag_erro6 = 0
                    listaS.procurar(int(valor_procurar), 1)
            elif content9 == "" and content10 == "":
                flag_erro6 = 0
            else:
                flag_erro6 = 1

            if not flag_erro6:
                input_box9.text = ''
                input_box9.txt_surface = FONT.render(input_box9.text, True, input_box9.color)
                input_box10.text = ''
                input_box10.txt_surface = FONT.render(input_box10.text, True, input_box10.color)
        if event.type == MOUSEBUTTONDOWN and 956 <= mouse[0] <= 1069 and 416 <= mouse[1] <= 446 and pagina == 3: #CONSULTAR PAGINA 3
            content14 = input_box14.returnText()
            content15 = input_box15.returnText()

            if (content14 != "" and content15 == "") or (content14 == "" and content15 != ""):
                if content14 != "":
                    if listade.nElementos == 0:
                        flag_erro9 = 1
                    else:
                        valor_procurar = content14
                        flag_erro9 = 0
                        listade.procurar(int(valor_procurar))
                elif int(content15) > listade.nElementos or int(content15) < 1:
                    flag_erro9 = 1
                else:
                    valor_procurar = content15
                    flag_erro9 = 0
                    listade.procurar(int(valor_procurar), 1)
            elif content14 == "" and content15 == "":
                flag_erro9 = 0
            else:
                flag_erro9 = 1

            if not flag_erro9:
                input_box14.text = ''
                input_box14.txt_surface = FONT.render(input_box14.text, True, input_box14.color)
                input_box15.text = ''
                input_box15.txt_surface = FONT.render(input_box15.text, True, input_box15.color)

        if event.type == MOUSEBUTTONDOWN and 601 <= mouse[0] <= 729 and 790 <= mouse[1] <= 875 and (pagina == 2 or pagina == 3): #MOVER A LISTA PARA DIREITA
            offset_increment = 1
        if event.type == MOUSEBUTTONDOWN and 473 <= mouse[0] <= 601 and 790 <= mouse[1] <= 875 and (pagina == 2 or pagina == 3): #MOVER A LISTA PARA ESQUERDA
            offset_decrement = 1

        if event.type == MOUSEBUTTONUP and (pagina == 2 or pagina == 3): #PARAR DE MOVER A LISTA
            offset_increment = 0
        if event.type == MOUSEBUTTONUP and (pagina == 2 or pagina == 3): #PARAR DE MOVER A LISTA
            offset_decrement = 0

        for box in input_boxes1:
            if pagina == 1:
                box.handle_event(event)

        for box in input_boxes2:
            if pagina == 2:
                box.handle_event(event)

        for box in input_boxes3:
            if pagina == 3:
                box.handle_event(event)

        for box in input_boxes4:
            if pagina == 6:
                box.handle_event(event)

    for box in input_boxes1:
        box.update()
    
    for box in input_boxes2:
        box.update()

    for box in input_boxes3:
        box.update()

    for box in input_boxes4:
        box.update()

    if offset_increment:
        offsetx -= 4
    if offset_decrement:
        offsetx += 4

#################################################################################################################################################
##############################################################      PAGINAS      ################################################################
#################################################################################################################################################
    match pagina:
        case 0: #MENU
            tela.blit(tela0, (0, 0))

            color1 = highlight_button(210, 685, 270, 345)

            color2 = highlight_button(210, 1045, 365, 440)

            color3 = highlight_button(210, 1010, 470, 545)

            color4 = highlight_button(210, 850, 765, 840)

            pygame.draw.rect(tela, color1, (210, 270, 475, 75), 2)

            pygame.draw.rect(tela, color2, (210, 365, 835, 75), 2)

            pygame.draw.rect(tela, color3, (210, 470, 800, 75), 2)

            pygame.draw.rect(tela, color4, (210, 765, 640, 75), 2)

        case 1: #LISTAS SEQUENCIAIS
            tela.blit(tela1, (0, 0))
            
            if flag_erro1 == 1:
                tela.blit(txt_erro, (200, 200))

            if flag_erro2 == 1:
                tela.blit(txt_erro, (610, 200))

            if flag_erro3 == 1:
                tela.blit(txt_erro, (965, 200))

            highlight_boxes(0, 1)

            for box in input_boxes1:
                box.draw(tela)

            imp.imprimir()
            imp.procurar(enable_procurar, mode_procurar, valor_procurar)
            enable_procurar = 0

        case 2: #LISTAS SIMPLESMENTE ENCADEADAS
            tela.blit(tela2, (0, 0))
            
            for box in input_boxes2:
                box.draw(tela)

            if flag_erro4 == 1:
                tela.blit(txt_erro, (200, 200))

            if flag_erro5 == 1:
                tela.blit(txt_erro, (610, 200))

            if flag_erro6 == 1:
                tela.blit(txt_erro, (965, 200))

            highlight_boxes(1, 1)

            listaS.imprimirLista(offsetx)

        case 3: #LISTA DUPLAMENTE ENCADEADA
            tela.blit(tela3, (0, 0))

            if flag_erro7 == 1:
                tela.blit(txt_erro, (200, 200))

            if flag_erro8 == 1:
                tela.blit(txt_erro, (610, 200))

            if flag_erro9 == 1:
                tela.blit(txt_erro, (965, 200))

            highlight_boxes(1, 1)

            listade.imprimirLista(offsetx)

            for box in input_boxes3:
                box.draw(tela)
        case 6:
            tela.blit(tela6, (0, 0))

            for box in input_boxes4:
                box.draw(tela)

            highlight_boxes(0, 0, 1)

            space = pow(2, get_height(root)-2) * node_radius

            # Desenha a árvore
            draw_tree(root, 600, 435, space)

    pygame.display.update()