import pytest
import requests

# CRUD
BASE_URL = "http://127.0.0.1:5000"
tasks = []

def test_create_task():
  new_task_data = {
    "title": "Nova tarefa",
    "description": "Descrição da nova tarefa"
  }
  response = requests.post(f"{BASE_URL}/tasks", json=new_task_data) 
  assert response.status_code == 200
  response_json = response.json()
  assert "message" in response_json
  assert "id" in response_json
  tasks.append(response_json['id'])

def test_get_tasks():
  response = requests.get(f"{BASE_URL}/tasks")
  assert response.status_code == 200
  response_json = response.json()
  assert "tasks" in response_json
  assert "total_tasks" in response_json

def test_get_task():
  if tasks:
    task_id = tasks[0]
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert "id" in response_json
    assert task_id == response_json['id']
    assert "completed" in response_json
    assert "description" in response_json
    assert "title" in response_json

def test_update_task() :
  if tasks:
    task_id = tasks[0]
    payload = {
      "completed": True,
      "description": "Nova descrição",
      "title": "Título atualizado"
    }
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    assert response.status_code == 200
    response_json = response.json()
    assert 'message' in response_json

    # Nova requisição a tarefa específica atualizada
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert "id" in response_json
    assert task_id == response_json['id']
    assert "completed" in response_json
    assert payload["completed"] == response_json["completed"]
    assert "description" in response_json
    assert payload["description"] == response_json["description"]
    assert "title" in response_json
    assert payload["title"] == response_json["title"]

def test_delete_task():
  if tasks:
    task_id = tasks[0]

    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json

    # Verificar se tarefa não existe mais
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    response.status_code == 404
    response_json = response.json()
    assert "message" in response_json