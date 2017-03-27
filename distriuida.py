from bottle import route, run, template
mensagens = []
@route('/hello/<name>')
def index(name):
    
    mensagens.append(name)
    print mensagens
    return mensagens

run(host='localhost', port=8080)
