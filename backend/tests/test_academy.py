from fastapi.testclient import TestClient


def test_list_academy_courses(client: TestClient) -> None:
    response = client.get("/api/v1/academy/courses")
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) == 5
    slugs = {course["slug"] for course in courses}
    assert "rf-fundamentos" in slugs
    assert "hackrf-responsable" in slugs


def test_get_course_detail(client: TestClient) -> None:
    response = client.get("/api/v1/academy/courses/rf-fundamentos")
    assert response.status_code == 200
    course = response.json()
    assert course["title"] == "Fundamentos de Radiofrecuencia"
    assert len(course["lessons"]) == 3


def test_enroll_and_track_progress(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    enroll_response = client.post(
        "/api/v1/academy/courses/rf-fundamentos/enroll",
        headers=auth_headers,
    )
    assert enroll_response.status_code == 200
    assert enroll_response.json()["progress_percent"] == 0.0

    course_response = client.get(
        "/api/v1/academy/courses/rf-fundamentos",
        headers=auth_headers,
    )
    lesson_id = course_response.json()["lessons"][0]["id"]

    progress_response = client.put(
        f"/api/v1/academy/lessons/{lesson_id}/progress",
        headers=auth_headers,
        json={"status": "in_progress"},
    )
    assert progress_response.status_code == 200
    assert progress_response.json()["status"] == "in_progress"

    complete_response = client.put(
        f"/api/v1/academy/lessons/{lesson_id}/progress",
        headers=auth_headers,
        json={"status": "completed", "quiz_score": 100},
    )
    assert complete_response.status_code == 200
    assert complete_response.json()["status"] == "completed"

    learning_response = client.get(
        "/api/v1/academy/me/learning",
        headers=auth_headers,
    )
    assert learning_response.status_code == 200
    learning = learning_response.json()
    assert learning["enrolled_courses"] == 1
    assert learning["completed_lessons"] == 1
    assert learning["overall_progress_percent"] > 0


def test_quiz_fails_below_passing_score(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    client.post(
        "/api/v1/academy/courses/hackrf-responsable/enroll",
        headers=auth_headers,
    )
    course_response = client.get(
        "/api/v1/academy/courses/hackrf-responsable",
        headers=auth_headers,
    )
    lesson_id = course_response.json()["lessons"][0]["id"]

    response = client.put(
        f"/api/v1/academy/lessons/{lesson_id}/progress",
        headers=auth_headers,
        json={"status": "completed", "quiz_score": 50},
    )
    assert response.status_code == 400
