from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

class TestAPI:
    # Please update the token before running the tests
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHBpcmVzIjoxNzIwNTQ1NDgzLjA0MTQ5ODR9.MzlkGryvL3Tm-sShodDyVV1FRMs0yAQmkXsyOYPx9bo"

    def test_create_user(self):
        response = client.post(
            "/register/",
            json={"username": "pytest", "password": "password"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "message": "User has been successfully registered."
        }

    def test_create_exist_user(self):
        response = client.post(
            "/register/",
            json={"username": "pytest", "password": "password"},
        )
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Username has already been registered"
        }

    def test_user_login(self):
        response = client.post(
            "/login/",
            json={"username": "pytest", "password": "password"},
        )
        assert response.status_code == 200

    def test_user_login_wrong_password(self):
        response = client.post(
            "/login/",
            json={"username": "pytest", "password": "password1"},
        )
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Wrong login details!"
        }

    def test_get_tasks(self):
        response = client.get(
            "/tasks/",
            headers={"Authorization": "Bearer "+self.token},
        )
        assert response.status_code == 200

    def test_add_task(self):
        response = client.post(
            "/tasks/",
            headers={"Authorization": "Bearer "+self.token},
            json={"title": "Test APIs", "description": "Use Pytest to test APIs", "completed": 0},
        )
        assert response.status_code == 200

    def test_get_single_task(self):
        response = client.get(
            "/tasks/1",
            headers={"Authorization": "Bearer "+self.token},
        )
        assert response.status_code == 200

    def test_update_single_task(self):
        response = client.put(
            "/tasks/1",
            headers={"Authorization": "Bearer "+self.token},
            json={"title": "Test APIs", "description": "Use Pytest to test APIs", "completed": 1},
        )
        assert response.status_code == 200

    def test_delete_single_task(self):
        response = client.delete(
            "/tasks/1",
            headers={"Authorization": "Bearer "+self.token},
        )
        assert response.status_code == 200
        assert response.json() == {
            "message": "Task successfully deleted"
        }
        
        
