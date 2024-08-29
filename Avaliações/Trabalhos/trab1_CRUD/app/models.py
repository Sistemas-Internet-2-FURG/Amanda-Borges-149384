from app import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    agendamentos = db.relationship('Agendamento', backref='cliente', lazy=True)

class Funcionario(db.Model):
    __tablename__ = 'funcionarias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    agendamentos = db.relationship('Agendamento', backref='funcionario', lazy=True)

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    funcionaria_id = db.Column(db.Integer, db.ForeignKey('funcionarias.id'), nullable=False)
    servico = db.Column(db.String(100), nullable=False)
