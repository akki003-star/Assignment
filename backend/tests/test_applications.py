from backend.app.models.job import Job


def test_apply_to_job_below_threshold(client, auth_headers, db_session):
    """User with no matching skills should get below-threshold error."""
    job = Job(
        title="Rust Developer",
        company="Systems Inc",
        requirements=["rust", "systems-programming", "c++"],
        description="Senior Rust developer needed",
    )
    db_session.add(job)
    db_session.commit()

    response = client.post(
        "/api/v1/applications/apply",
        headers=auth_headers,
        json={"job_id": job.id},
    )
    assert response.status_code == 400
    assert "threshold" in response.json()["detail"].lower()


def test_apply_to_nonexistent_job(client, auth_headers):
    response = client.post(
        "/api/v1/applications/apply",
        headers=auth_headers,
        json={"job_id": 9999},
    )
    assert response.status_code == 400
    assert "not found" in response.json()["detail"].lower()


def test_list_applications_empty(client, auth_headers):
    response = client.get("/api/v1/applications/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_get_dashboard_stats(client, auth_headers):
    response = client.get("/api/v1/applications/dashboard", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_applications"] == 0
    assert data["pending"] == 0
    assert data["applied"] == 0
