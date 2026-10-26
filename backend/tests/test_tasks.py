import pytest


def test_create_task(client, column, auth_headers):
    response = client.post(
        f"/columns/{column.id}/tasks",
        json={"title": "Write Tests"},
        headers=auth_headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write Tests"
    assert body["column_id"] == column.id
    assert body["description"] is None
    assert body["position"] == 0


def test_update_task_rejects_null_title(client, task, auth_headers):
    response = client.patch(
        f"/tasks/{task.id}", json={"title": None}, headers=auth_headers
    )

    assert response.status_code == 422


def test_update_task_description(client, task, auth_headers):
    response = client.patch(
        f"/tasks/{task.id}",
        json={"description": "Some description"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "Some description"
    assert body["title"] == "Test Task"


def test_two_tasks_positions(client, column, auth_headers):
    first_response = client.post(
        f"/columns/{column.id}/tasks",
        json={"title": "Write One Test"},
        headers=auth_headers,
    )
    second_response = client.post(
        f"/columns/{column.id}/tasks",
        json={"title": "Write Two Tests"},
        headers=auth_headers,
    )
    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert first_response.json()["position"] == 0
    assert second_response.json()["position"] == 1


def test_get_task(client, task, auth_headers):
    response = client.get(f"/tasks/{task.id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


def test_get_invalid_task(client, auth_headers):
    invalid_task_id = 9999999
    response = client.get(f"/tasks/{invalid_task_id}", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete(client, task, auth_headers):
    response = client.delete(f"/tasks/{task.id}", headers=auth_headers)

    assert response.status_code == 204

    deleted_task_response = client.get(f"/tasks/{task.id}", headers=auth_headers)

    assert deleted_task_response.status_code == 404


def test_delete_mmissing_task(client, auth_headers):
    invalid_task_id = 99999999
    response = client.delete(f"/tasks/{invalid_task_id}", headers=auth_headers)

    assert response.status_code == 404


@pytest.mark.parametrize(
    "title", ["", " ", "x" * 201], ids=["empty", "only_whitespace", "too_long"]
)
def test_create_task_rejects_invalid_title(client, column, auth_headers, title):
    response = client.post(
        f"/columns/{column.id}/tasks", json={"title": title}, headers=auth_headers
    )

    assert response.status_code == 422
