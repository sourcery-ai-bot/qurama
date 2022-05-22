from starlette.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_ping():
    response = client.get("/tools/")

    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_create_question():
    data = {
        "inquiry": "What about Scooby Doo?",
        "publish": False,
        "answers": [
            {
                "retort": "He cool.",
                "is_correct": False,
            },
            {
                "retort": "He nice.",
                "is_correct": False,
            },
            {
                "retort": "Cute pup.",
                "is_correct": False,
            },
            {
                "retort": "He smart too.",
                "is_correct": True,
            },
        ],
    }
    response = client.post("/questions/", json=data)

    assert response.status_code == 201


def test_too_many_correct_answers():
    data = {
        "inquiry": "What about Scooby Doo?",
        "publish": False,
        "answers": [
            {
                "retort": "He cool.",
                "is_correct": False,
            },
            {
                "retort": "He nice.",
                "is_correct": False,
            },
            {
                "retort": "He fantastic.",
                "is_correct": True,
            },
            {
                "retort": "He smart too.",
                "is_correct": True,
            },
        ],
    }
    response = client.post("/questions/", json=data)

    message = "Please select exactly one correct answer."

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == message


def test_incorrect_amount_of_answers():
    data = {
        "inquiry": "What about Scooby Doo?",
        "publish": False,
        "answers": [
            {
                "retort": "He cool.",
                "is_correct": False,
            },
            {
                "retort": "He nice.",
                "is_correct": False,
            },
            {
                "retort": "He fantastic.",
                "is_correct": True,
            },
        ],
    }
    response = client.post("/questions/", json=data)

    message = "Please provide 4 answers."

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == message
