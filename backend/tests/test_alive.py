# project/tests/test_alive.py


from app import main


def test_alive(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"Welcome from the API"}