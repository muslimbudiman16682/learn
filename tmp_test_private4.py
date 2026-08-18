import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.core.db import engine
from sqlmodel import Session, select
from app.models.auths.user import User

client = TestClient(app)
email = f"user-{uuid.uuid4().hex[:8]}@example.com"
r = client.post(f"{settings.API_V1_STR}/private/users/", json={"email":email,"password":"password123","full_name":"Pollo Listo"})
print('status', r.status_code)
data = r.json()
print('json', data)
print('id type', type(data.get('id')))

with Session(engine) as session:
    try:
        user = session.exec(select(User).where(User.id == data['id'])).first()
        print('query result', user)
    except Exception as e:
        print('query exception', repr(e))

