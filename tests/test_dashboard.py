def test_dashboard_stats(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "dashboarduser",
            "email": "dashboarduser@gmail.com",
            "password": "Test@123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "dashboarduser",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create jobs with different statuses
    statuses = [
        "Applied",
        "Applied",
        "Shortlisted",
        "Assessment",
        "Interview",
        "Interview",
        "Selected",
        "Rejected",
        "Withdrawn"
    ]

    for index, status in enumerate(statuses):
        response = client.post(
            "/jobs",
            json={
                "company_name": f"Company {index}",
                "job_title": "Python Developer",
                "location": "Ahmedabad",
                "job_type": "Full-time",
                "salary": "600000",
                "application_date": "2026-09-21",
                "status": status,
                "job_url": "https://example.com/job",
                "company_website": "https://example.com",
                "description": "Python backend role",
                "remote": "False"
            },
            headers=headers
        )

        assert response.status_code == 201

    # Get dashboard statistics
    response = client.get(
        "/dashboard/stats",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_jobs"] == 9
    assert data["applied"] == 2
    assert data["shortlisted"] == 1
    assert data["assessment"] == 1
    assert data["interview"] == 2
    assert data["selected"] == 1
    assert data["rejected"] == 1
    assert data["withdrawn"] == 1
    assert data["total_interviews"] == 0