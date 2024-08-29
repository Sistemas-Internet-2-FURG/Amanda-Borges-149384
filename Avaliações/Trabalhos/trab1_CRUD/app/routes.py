from flask import Blueprint, Flask, render_template, redirect, url_for, request, jsonify
from app.models import Cliente, Funcionario, Agendamento
from app import db

main = Blueprint('main', __name__)
#main = Flask('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        senha = data['senha']
        tipo_usuario = data['tipo_usuario']  # Pode ser 'cliente' ou 'funcionaria'

        if tipo_usuario == 'cliente':
            usuario = Cliente.query.filter_by(nome=username).first()
        elif tipo_usuario == 'funcionaria':
            usuario = Funcionario.query.filter_by(nome=username).first()
        else:
            return jsonify({'message': 'Tipo de usuário inválido'}), 400 #AO INVES DE APRESENTAR SÓ A IMAGEM, VAMOS RECARREGAR A TELA DE LOGIN/REGISTRO E APRESENTAR POPUP COM ERRO

        if usuario and usuario.senha == senha:
            return redirect(url_for('main.show_agendamento'))
        else:
            return jsonify({'message': 'Credenciais inválidas'}), 401

    return render_template('login.html')


@main.route('/register_func', methods=['GET','POST'])
def register_func():
    if request.method == 'POST':
        print('request.form = ', request.form)
        data = request.form
        print('data[nome] = ', data['username'])
        novo_func = Funcionario(
            nome=data['username'],
            especialidade=data['espec'],
            senha=data['senha']
        )
        db.session.add(novo_func)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register_func.html')


@main.route('/register_user', methods=['GET','POST'])
def register_user():
    print("request.method = ", request.method)
    print("São iguais? ", (request.method == 'POST'))
    if request.method == 'POST':
        print('request.form = ', request.form)
        data = request.form
        print('data[nome] = ', data['username'])
        novo_cliente = Cliente(
            nome=data['username'],
            senha=data['senha'] 
        )
        db.session.add(novo_cliente)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register_user.html')

@main.route('/agenda', methods=['GET', 'POST'])
def show_agendamento():
    if request.method == 'POST':
        data = request.form
        novo_agendamento = Agendamento(
            data_hora=data['data_hora'],
            cliente_id=data['cliente_id'],
            funcionaria_id=data['funcionaria_id'],
            servico=data['servico']
        )
        db.session.add(novo_agendamento)
        db.session.commit()
        return redirect(url_for('main.show_agendamento'))
    
    # Para a requisição GET
    agendamentos = Agendamento.query.all()
    clientes = Cliente.query.all()
    funcionarias = Funcionario.query.all()
    
    return render_template('agenda.html', 
                           agendamentos=agendamentos,
                           clientes=clientes,
                           funcionarias=funcionarias)

@main.route('/update_agendamento/<int:id>', methods=['GET', 'POST'])
def update_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    
    if request.method == 'POST':
        data = request.form
        agendamento.data_hora = data['data_hora']
        agendamento.cliente_id = data['cliente_id']
        agendamento.funcionaria_id = data['funcionaria_id']
        agendamento.servico = data['servico']
        
        db.session.commit()
        return redirect(url_for('main.show_agendamento'))
    
    # Para a requisição GET, garantindo que vai apresentar todas as opcoes de clientes e funcionarias
    clientes = Cliente.query.all()
    funcionarias = Funcionario.query.all()
    
    # Renderiza o formulário de atualização com os dados atuais do agendamento
    return render_template('update_agendamento.html', agendamento=agendamento,  
                                                        clientes=clientes,
                                                        funcionarias=funcionarias)

@main.route('/delete_agendamento/<int:id>', methods=['GET', 'POST'])
def delete_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)

    if not agendamento:
        return jsonify({'message': 'Agendamento não encontrado'}), 404

    db.session.delete(agendamento)
    db.session.commit()
    #return jsonify({'message': 'Agendamento deletado com sucesso'}), 200
    return redirect(url_for('main.show_agendamento'))