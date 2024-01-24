from fastapi.testclient import TestClient
from main import api
import pytest

client = TestClient(api)

def test_subscribe(auth_user):
  response = client.get("/stripe/subscribe", headers={'Authorization': f"Bearer {auth_user['access_token']}"})
  assert response.status_code == 200

def test_already_subscribed(subscribed_user):
  response = client.get("/stripe/subscribe", headers={'Authorization': f"Bearer {subscribed_user['access_token']}"})
  assert response.status_code == 400

def test_unsubscribe(subscribed_user):
  response = client.get("/stripe/unsubscribe", headers={'Authorization': f"Bearer {subscribed_user['access_token']}"})
  assert response.status_code == 200

def test_no_active_subscription(auth_user):
  response = client.get("/stripe/unsubscribe", headers={"Authorization": f"Bearer {auth_user['access_token']}"})
  assert response.status_code == 401
  assert response.json()['detail'] == "user not subscribed"
  
@pytest.mark.parametrize("route,method,body", [
  ("/stripe/subscribe", 'GET', None),
  ("/stripe/unsubscribe", 'GET', None)
])
def test_unauthorized(route, method, body):
  if (method == "GET"):
    response = client.get(route)
  elif (method == "POST"):
    response = client.post(route, json=body)
  elif (method == "PUT"):
    response = client.put(route, json=body)
  elif (method == "PATCH"):
    response = client.patch(route, json=body)
  elif (method == "DELETE"):
    response = client.delete(route)
  
  assert response.status_code == 401
