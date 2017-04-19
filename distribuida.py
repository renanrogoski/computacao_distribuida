from bottle import run, get, post, view, request, redirect
import requests, bottle, json, threading, time, sys

historico_msgs = [("Bem Vindos","Chat Inciado")]
peers = sys.argv[2:]

nome = ""

print(peers)

@get('/mensagens')
@view('hello_template')
def hello_template():    
    return {'mensagens': historico_msgs, 'nome': nome} #retorno o dicionario para template



@post('/mensagens/enviar')
def mensagemEnviar(): #se caso foi chamado o metodo enviar, significa que o action foi submetido ma template e as
                      # variaveis mensagens e nome foram transmitidas pelo POST.
    global nome

    msg = request.forms.get('mensagem') 
    n = request.forms.get('nome')
    historico_msgs.append([n,msg])
    nome = n

    redirect('/mensagens')


@get('/peers')
def index():
    return json.dumps(peers)

@get('/messages')
def index():
    return json.dumps(historico_msgs)



def searchPeers():
    time.sleep(5)
    while True:
        time.sleep(1)
        newPeers = []
        for p in peers:
            r = requests.get(p + '/peers')
            newPeers = newPeers + json.loads(r.text)
        peers[:] = list(set(newPeers + peers))
        print(peers)
        time.sleep(2)


def searchMessages():
    time.sleep(5)
    while True:
        newMs = []
        for p in peers:
            m = requests.get(p + '/messages')
            newMs = json.loads(m.text)
            for msg in newMs:
                if msg not in historico_msgs:
                    historico_msgs.append(msg)

        time.sleep(2)

tr1 = threading.Thread(target=searchPeers)
tr1.start()

tr2 = threading.Thread(target=searchMessages)
tr2.start()




run(host='localhost', port=int(sys.argv[1]))