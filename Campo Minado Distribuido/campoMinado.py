from random import seed, randint
from bottle import run, get, post, view, redirect, request 
import requests, bottle, json, threading, time, sys

tabuleiro = []
tabuleiroView = []
jogadas = []

peers = sys.argv[2:]
porta = int(sys.argv[1])
#semente = int(sys.argv[3])

print(peers)

#@get('/')
#@view('campo_minado')



@get('/')
@get('/cria_tabuleiro')
@view('campo_minado')
def criaCampoMinado():
    global tabuleiroView
    global tabuleiro
    seed(5)

    tabuleiroView  = [[ '-' for x in range(10)] for x in range(10)]
    tabuleiro  = [[ randint(0,3) for x in range(10)] for x in range(10)]
    #print (tabuleiroView)
    
    # print (len(tabuleiro))
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro)):
            if tabuleiro[i][j] != 1:
                tabuleiro[i][j] = 0

    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro)):
            if tabuleiro[i][j] == 1:
                tabuleiro[i][j] = 10

    # print (tabuleiro)
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro)):
            if tabuleiro[i][j] >= 10 and j > 0: #soma no lado esquerdo da bomba 
                tabuleiro[i][j-1]+=1

            if tabuleiro[i][j] >= 10 and j > 0 and i < 9: #soma no lado esquerdo pra baixo 
                tabuleiro[i+1][j-1]+=1

            if tabuleiro[i][j] >= 10 and j > 0 and i > 0: #soma no lado esquerdo pra cima
                tabuleiro[i-1][j-1]+=1

            if tabuleiro[i][j] >= 10 and j < 9: #soma na direita 
                tabuleiro[i][j+1]+=1

            if tabuleiro[i][j] >= 10 and j < 9 and i < 9: #soma na direita pra baixo 
                tabuleiro[i+1][j+1]+=1

            if tabuleiro[i][j] >= 10 and j < 9 and i > 0: #soma na direita pra cima 
                tabuleiro[i-1][j+1]+=1

            if tabuleiro[i][j] >= 10 and i > 0: #soma em cima
                tabuleiro[i-1][j]+=1

            if tabuleiro[i][j] >= 10 and i < 9: #soma embaixo
                tabuleiro[i+1][j]+=1


    #print ("\nTabuleiro com as Bombas e Aviso de Quantidades")
    #print ("Valores menores de 10 são as quantidades de bombas no entorno")
    #print ("valores maior ou igual a 10 são bombas somadas de quantidades no entorno")
    #for i in range(len(tabuleiro)):
        #print('\n')
        #for j in range(len(tabuleiro)):

            #print("  %d  " %tabuleiro[i][j], end = "")

    #print('\n')
    

    #print (tabuleiro)
    redirect('/tabuleiro')


@get('/tabuleiro')
@view('campo_minado')
def retornaTabuleiroview():
    return {'tabuleiroView': tabuleiroView, 'tabuleiro':tabuleiro}

@get('/perdeu')
@view('perdeu')
def retornaTabuleiroview():
    return {'tabuleiroView': tabuleiroView, 'porta': porta}


@post('/jogada')
def atualizaTabuleiroView():
    global jogadas

    x = int(request.forms.get('x'))-1
    y = int(request.forms.get('y'))-1
    
    jogadas.append({'tipo': "jogada", 'x': x, 'y': y})

    todosJoga(x,y)

    #print(tabuleiroView)    
    redirect('/tabuleiro')

def todosJoga(x,y):
    global tabuleiroView
    global tabuleiro
    if (tabuleiro[x][y] < 10 and tabuleiro[x][y] != 0):
        tabuleiroView[x][y] = tabuleiro[x][y]
    if (tabuleiro[x][y] >= 10):
        for i in range(len(tabuleiro)):
            for j in range(len(tabuleiro)):
                if tabuleiro[i][j] >= 10:
                    tabuleiroView[i][j] = '*'
        redirect('/perdeu')

    if (tabuleiro[x][y] == 0):
        verificaVizinho(x,y)
    

def atualizaJogadas(valor):
    for x in valor: #lista e jogadas
        if x['tipo'] == 'jogada':
            print ("encontrei jogada")
            todosJoga(x['x'],x['y'])

    


def verificaVizinho(x,y):
    if tabuleiro[x][y] == 0:
        tabuleiroView[x][y] = 0
        tabuleiro[x][y] = -1
        if y > 0:
            if tabuleiro[x][y-1] == 0:
                verificaVizinho(x,y-1)
        if y < 9:
            if tabuleiro[x][y+1] == 0:
                verificaVizinho(x,y+1)
        if x > 0:
            if tabuleiro[x-1][y] == 0:
                verificaVizinho(x-1,y)
        if x < 9:
            if tabuleiro[x+1][y] == 0:
                verificaVizinho(x+1,y)
        if x > 0 and y > 0:
            if tabuleiro[x-1][y-1] == 0:
                verificaVizinho(x-1,y-1)
        if x > 0 and y < 9:
            if tabuleiro[x-1][y+1] == 0:
                verificaVizinho(x-1,y+1)
        if x < 9 and y > 0:
            if tabuleiro[x+1][y-1] == 0: #aqui
                verificaVizinho(x+1,y-1)
        if x < 9 and y < 9:
            if tabuleiro[x+1][y+1] == 0:
                verificaVizinho(x+1,y+1)

@get('/peers')
def index():
    return json.dumps(peers)

@get('/jogadas')
def index():
    return json.dumps(jogadas)

def clientePeers():
    time.sleep(5)
    while True:
        time.sleep(1)
        np = []
        for p in peers:
            r = requests.get(p + '/peers')
            np = np + json.loads(r.text)
        peers[:] = list(set(np + peers))
        print(peers)
        time.sleep(2)


def clienteMessages():
    time.sleep(5)
    while True:
        nm = []
        for p in peers:
            print("entrouuuuuuuuuuu")
            m=requests.get(p + '/jogadas')
            valor = json.loads(m.text)
            print(valor)
            if valor:
                atualizaJogadas(valor)
                
            
        time.sleep(2)

    

t1 = threading.Thread(target=clientePeers)
t1.start()

t2 = threading.Thread(target=clienteMessages)
t2.start()


run(host='localhost', port=porta)
