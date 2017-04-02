from bottle import run, get, post, view, request, redirect
historico_msgs = [("Bem Vindos","Chat Inciado")]
nome = ""


@get('/mensagens')
@view('hello_template')
def hello_template():
    # msgs = json.loads(name)
    # cliente = msgs['cl']
    # msg = msgs['msg']

    # historico_msgs.append({'cliente':cliente,'mensagem':msg})

    # return template('<b>Chat {{chat}}</b>!', chat=historico_msgs)
    return {'mensagens': historico_msgs, 'nome': nome}



@post('/mensagens/enviar')

def mensagemEnviar():

    global nome

    msg = request.forms.get('mensagem')
    n = request.forms.get('nome')
    historico_msgs.append([n,msg])
    nome = n

    redirect('/mensagens')

    # msgs = json.loads(name)
    # cliente = msgs['cl']
    # msg = msgs['msg']

    # historico_msgs.append({'cliente':cliente,'mensagem':msg})

    # return template('<b>Chat {{chat}}</b>!', chat=historico_msgs)

run(host='localhost', port=8080)