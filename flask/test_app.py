import pytest
from flask import Flask
from flask.testing import FlaskClient
from app import app  # Importa a aplicação principal

@pytest.fixture
def client():
    """Fixture para configurar o cliente de teste."""
    with app.test_client() as client:
        yield client

def test_listar_alunos(client: FlaskClient):
    """Testa a rota GET /alunos."""
    response = client.get('/alunos')
    assert response.status_code == 200, "O status code não é 200"
    assert isinstance(response.json, list), "A resposta não é uma lista"

def test_adicionar_aluno(client: FlaskClient):
    """Testa a rota POST /alunos."""
    novo_aluno = {
        "nome": "João",
        "sobrenome": "Silva",
        "turma": "1A",
        "disciplinas": "Matemática, Física",
        "ra": "12345"
    }
    response = client.post('/alunos', json=novo_aluno)
    assert response.status_code == 201, "O status code não é 201"
    assert response.json['message'] == 'Aluno adicionado com sucesso!', "Mensagem inesperada na resposta"
