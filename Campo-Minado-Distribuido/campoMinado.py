from random import seed, randint
from bottle import run, get, post, view, redirect, request 
import requests, bottle, json, threading, time, sys

tabuleiro = []
tabuleiroView = []
todasJogadas = []
jogadas = set([])

peers = sys.argv[2:]
porta = int(sys.argv[1])
#semente = int(sys.argv[3])
peers.append("http://localhost:"+str(sys.argv[1]))  

print(peers)


class VC:
    def __init__(self, name):
        self.name = name
        self.vClock = { self.name: 0 }

    def __repr__(self):
        return "V%s" % repr(self.vClock)

    def increment(self):
        self.vClock[self.name] += 1
        return self

    def update(self, t):
        self.increment()
        for k, v in t.items():
            if k not in vc.vClock or vc.vClock[k] < t[k]:
                vc.vClock[k] = v










vc = VC('http://localhost:' + sys.argv[1]);

@get('/')
@get('/cria_tabuleiro')
@view('campo_minado')
def criaCampoMinado():
    global tabuleiroView
    global tabuleiro
    
    global todasJogadas
    todasMsgs = list(jogadas)
    ordenacaoMsg()
    return dict(mens=list(todasMsgs))





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
    
    time.sleep(2)
    atualizaJogadas(jogadas)
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

    if x != None and y != None:
        vc.increment()
        m = (x, y, frozendict(vc.vClock))
        jogadas.add(m)
    
    #jogadas.append({'tipo': "jogada", 'x': x, 'y': y})

    #testaJogadas(x,y)

    #print(tabuleiroView)    
    redirect('/tabuleiro')

def testaJogadas(x,y):
    global tabuleiroView
    global tabuleiro
    if (tabuleiro[x][y] < 10 and tabuleiro[x][y] != 0):
        tabuleiroView[x][y] = tabuleiro[x][y]
    elif (tabuleiro[x][y] >= 10):
        for i in range(len(tabuleiro)):
            for j in range(len(tabuleiro)):
                if tabuleiro[i][j] >= 10:
                    tabuleiroView[i][j] = '*'
        redirect('/perdeu')

    elif (tabuleiro[x][y] == 0):
        verificaVizinho(x,y)


    

def atualizaJogadas(lista):
    global tabuleiro
    print('tabuleiro '+str(tabuleiro))
    for jogada in lista: #lista de jogadas
        if jogada['tipo'] == 'jogada':
            print ("encontrei jogada")
            testaJogadas(jogada['x'],jogada['y'])


    


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
    return json.dumps([(x, y, dict(tmp)) for (x, y, tmp) in jogadas])

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


# def clienteMessages():
#     global tabuleiro
#     time.sleep(5)
#     while True:
#         nm = []
#         for p in peers:
#             print("entrouuuuuuuuuuu")
#             m=requests.get(p + '/jogadas')
#             lista_jogadas = json.loads(m.text)
#             print(lista_jogadas)
#             if lista_jogadas and tabuleiro:
#                 atualizaJogadas(lista_jogadas)
                
            
#         time.sleep(2)
def clienteMessages():
    while True:
                time.sleep(2)
                global jogadas
                for p in peers:
                        time.sleep(2)
                        jog = recebeJogada(p)
                        for (x, y, tmp) in jog.difference(jogadas):
                            vc.update(tmp)
                            jogadas.add((x, y, tmp))

def recebeJogada(p):
    r = requests.get(p + "/jogadas")
    obj = json.loads(r.text)
    rm = set((a, b, frozendict(t)) for [a,b,t] in obj)
    return rm







    

t1 = threading.Thread(target=clientePeers)
t1.start()

t2 = threading.Thread(target=clienteMessages)
t2.start()


run(host='localhost', port=porta)
