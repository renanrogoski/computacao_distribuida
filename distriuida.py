from bottle import route, run, template
import json
historico_msgs = []

@route('/hello/<name>')
def index(name):
    msgs = json.loads(name)
    cliente = msgs['cl']
    msg = msgs['msg']

    historico_msgs.append({'cliente':cliente,'mensagem':msg})

    return template('<b>Chat {{chat}}</b>!', chat=historico_msgs)

run(host='localhost', port=8080)