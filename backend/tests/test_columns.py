def test_delete_column_cascades(client, db, column, task, auth_headers):
    response = client.delete(f"/columns/{column.id}", headers=auth_headers)
    # Empty the identity map so get has to query the database.
    # Otherwise it looks in the identity map and still finds the deleted tasks,
    # returning 200
    db.expunge_all()
    assert response.status_code == 204
    get_task_response = client.get(f"/tasks/{task.id}", headers=auth_headers)

    assert get_task_response.status_code == 404
    assert get_task_response.json()["detail"] == "Task not found"
