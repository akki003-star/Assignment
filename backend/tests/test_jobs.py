from backend.app.models.job import Job


def test_search_jobs_empty(client, auth_headers):
    response = client.post(
        "/api/v1/jobs/search",
        headers=auth_headers,
        json={"keywords": ["python"]},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_search_jobs_with_results(client, auth_headers, db_session):
    job = Job(
        title="Python Developer",
        company="Tech Corp",
        location="Remote",
        salary_min=80000,
        salary_max=120000,
        description="We need a Python developer",
        requirements=["python", "fastapi", "sql"],
        source="linkedin",
    )
    db_session.add(job)
    db_session.commit()

    response = client.post(
        "/api/v1/jobs/search",
        headers=auth_headers,
        json={"keywords": ["Python"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Python Developer"


def test_search_jobs_by_location(client, auth_headers, db_session):
    job1 = Job(title="Dev", company="A", location="Remote")
    job2 = Job(title="Dev", company="B", location="NYC")
    db_session.add_all([job1, job2])
    db_session.commit()

    response = client.post(
        "/api/v1/jobs/search",
        headers=auth_headers,
        json={"location": "Remote"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["location"] == "Remote"


def test_get_job_by_id(client, auth_headers, db_session):
    job = Job(title="ML Engineer", company="AI Inc", location="SF")
    db_session.add(job)
    db_session.commit()

    response = client.get(f"/api/v1/jobs/{job.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "ML Engineer"


def test_get_job_not_found(client, auth_headers):
    response = client.get("/api/v1/jobs/999", headers=auth_headers)
    assert response.status_code == 404
