from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)
r = client.post(f"{settings.API_V1_STR}/private/users/", json={"email":"pollo@listo.com","password":"password123","full_name":"Pollo Listo"})
print('status', r.status_code)
print('json', r.json())
print('id type', type(r.json().get('id')))
