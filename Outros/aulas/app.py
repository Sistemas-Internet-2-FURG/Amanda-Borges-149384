from flask import Flask, render_template, request
from markupsafe import escape
#import urllib.request, json

#terminal commands
#export FLASK_APP=app.py

#para rodar o script basta colocar isso no terminal
#flask run

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.secret_key = 'nao_sei'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/home/aluno/si2_prisco/paraAula/sessoes'
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)


#chamada = {12:'Joao', 13:'Pablo', 14:'Filipa', 1:'Amandinha'} #Global
chamada = {}

teste = []

@app.route("/")
def alo_mundo():
    nome = "Amanda"
    teste = ['a', 'b', 'c']
    return render_template("login.html", nome=nome, teste=teste)

'''@app.route("/sessao")
def usa_sessao():
    session['nome'] = 'Prisco'
    print(session)
    print(session.get('nome'))
    return (f"oi {session['nome']}")'''
    

@app.route("/cumprimenta/<nome>")
def diz_oi(nome):
    return ("oi, " + nome)

@app.route("/variaveis",methods=['POST','GET'])
def usando_variaveis():
    matricula = request.form.get('nova_matricula')
    aluno = request.form.get('novo_aluno')

    '''
    print('--------------')
    print(matricula, aluno)
    print('--------------')

    '''

    if (request.method == 'POST') and (len(matricula) > 0):
        chamada[matricula] = aluno #adicionei no dicionário

        with open("users.csv", "a") as csv_file:
            csv_file.write(str(matricula) + ";" + str(aluno) + "\n")
    
    # faltando ainda implementar os trechos que conseguem editar, exluir e/ou consultar dados específicos
    # no csv com os dados

    return render_template('variaveis.html', chamada=chamada)


@app.route("/sobre")
def sobre():
    saida = "<h1>OIOIOI</h1><br>"*10
    return(saida)

if __name__ == "__main__":
    app.run()
#app.get('/variaveis')


