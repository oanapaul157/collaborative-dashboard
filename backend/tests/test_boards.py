from app.models import Board, Column, Task


def test_delete_board_cascades(client, db, board, column, task, auth_headers):
    response = client.delete(f"/boards/{board.id}", headers=auth_headers)
    assert response.status_code == 204
    # Empty the identity map so get has to query the database.
    # Otherwise it looks in the identity map and still finds the deleted columns,
    # returning 200
    db.expunge_all()

    get_column_response = client.get(f"/columns/{column.id}", headers=auth_headers)

    assert get_column_response.status_code == 404
    assert get_column_response.json()["detail"] == "Column not found"
    get_task_response = client.get(f"/tasks/{task.id}", headers=auth_headers)

    assert get_task_response.status_code == 404
    assert get_task_response.json()["detail"] == "Task not found"


def test_creating_board_makes_you_member(client, user, auth_headers):
    response = client.post("/boards", json={"name": "My Board"}, headers=auth_headers)

    assert response.status_code == 201

    boards_response = client.get("/boards", headers=auth_headers)

    test_board = boards_response.json()[0]
    assert test_board["owner_id"] == user.id
    assert test_board["id"] == response.json()["id"]


def test_board_list_only_shows_users_own_boards(
    client, db, board, other_user, auth_headers
):
    db.add(Board(name="Not Mine", owner=other_user))
    db.flush()

    response = client.get("/boards", headers=auth_headers)

    assert response.status_code == 200
    # Comparing the whole list of ids, instead of checking that "Not mine" isn't there, also catches duplicates.
    assert [brd["id"] for brd in response.json()] == [board.id]


def test_board_returns_columns_in_order(client, db, board, auth_headers):
    db.add(Column(name="Done", board=board, position=2))
    db.add(Column(name="To Do", board=board, position=0))
    db.add(Column(name="In Progress", board=board, position=1))
    db.flush()
    db.expunge_all()

    response = client.get(f"/boards/{board.id}", headers=auth_headers)
    assert response.status_code == 200
    names = [col["name"] for col in response.json()["columns"]]
    assert names == ["To Do", "In Progress", "Done"]


def test_board_returns_tasks_nested_and_ordered(client, db, board, auth_headers):
    todo = Column(name="To Do", board=board, position=0)
    empty = Column(name="Empty", board=board, position=1)
    db.add_all([todo, empty])
    db.add(Task(title="Third", column=todo, position=2))
    db.add(Task(title="First", column=todo, position=0))
    db.add(Task(title="Second", column=todo, position=1))
    db.flush()
    db.expunge_all()

    response = client.get(f"/boards/{board.id}", headers=auth_headers)
    assert response.status_code == 200
    todo_json, empty_json = response.json()["columns"]
    assert [task["title"] for task in todo_json["tasks"]] == [
        "First",
        "Second",
        "Third",
    ]
    assert empty_json["tasks"] == []


def test_missing_board_returns_404(client, auth_headers):
    invalid_board_id = 99999999

    response = client.get(f"/boards/{invalid_board_id}", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Board not found"


def test_board_rename(client, board, auth_headers):
    response = client.patch(
        f"/boards/{board.id}", json={"name": "New Name"}, headers=auth_headers
    )
    assert response.status_code == 200
    new_response = client.get(f"/boards/{board.id}", headers=auth_headers)
    assert new_response.json()["name"] == "New Name"
