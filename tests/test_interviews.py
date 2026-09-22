def test_create_interview(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "interviewuser",
            "email": "interviewuser@gmail.com",
            "password": "Test@123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "interviewuser",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create job
    job_response = client.post(
        "/jobs",
        json={
            "company_name": "Infosys",
            "job_title": "Python Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "600000",
            "application_date": "2026-09-21",
            "status": "Interview",
            "job_url": "https://example.com/job",
            "company_website": "https://www.infosys.com",
            "description": "Python backend position",
            "remote": "False"
        },
        headers=headers
    )

    assert job_response.status_code == 201

    job_id = job_response.json()["id"]

    # Create interview
    response = client.post(
        f"/jobs/{job_id}/interviews",
        json={
            "interview_date": "2026-09-25",
            "round": "Technical",
            "interviewer": "Rahul Sharma",
            "mode": "Online",
            "result": "Pending",
            "notes": "Prepare Python, SQL and FastAPI"
        },
        headers=headers
    )

    assert response.status_code == 201

    data = response.json()

    assert data["job_id"] == job_id
    assert data["round"] == "Technical"
    assert data["interviewer"] == "Rahul Sharma"
    assert data["mode"] == "Online"


def test_get_interviews(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "getinterviewuser",
            "email": "getinterviewuser@gmail.com",
            "password": "Test@123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "getinterviewuser",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create job
    job_response = client.post(
        "/jobs",
        json={
            "company_name": "TCS",
            "job_title": "Python Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "600000",
            "application_date": "2026-09-21",
            "status": "Interview",
            "job_url": "https://example.com/job",
            "company_website": "https://www.tcs.com",
            "description": "Python backend role",
            "remote": "False"
        },
        headers=headers
    )

    assert job_response.status_code == 201

    job_id = job_response.json()["id"]

    # Create interview
    interview_response = client.post(
        f"/jobs/{job_id}/interviews",
        json={
            "interview_date": "2026-09-25",
            "round": "Technical",
            "interviewer": "Rahul Sharma",
            "mode": "Online",
            "result": "Pending",
            "notes": "Prepare Python and SQL"
        },
        headers=headers
    )

    assert interview_response.status_code == 201

    # Get interviews
    response = client.get(
        f"/jobs/{job_id}/interviews",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["job_id"] == job_id
    assert data[0]["round"] == "Technical"
    assert data[0]["mode"] == "Online"


def test_update_interview(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "updateinterviewuser",
            "email": "updateinterviewuser@gmail.com",
            "password": "Test@123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "updateinterviewuser",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create job
    job_response = client.post(
        "/jobs",
        json={
            "company_name": "Wipro",
            "job_title": "Python Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "600000",
            "application_date": "2026-09-21",
            "status": "Interview",
            "job_url": "https://example.com/job",
            "company_website": "https://www.wipro.com",
            "description": "Python backend role",
            "remote": "False"
        },
        headers=headers
    )

    assert job_response.status_code == 201

    job_id = job_response.json()["id"]

    # Create interview
    interview_response = client.post(
        f"/jobs/{job_id}/interviews",
        json={
            "interview_date": "2026-09-25",
            "round": "Technical",
            "interviewer": "Rahul Sharma",
            "mode": "Online",
            "result": "Pending",
            "notes": "Prepare Python"
        },
        headers=headers
    )

    assert interview_response.status_code == 201

    interview_id = interview_response.json()["id"]

    # Update interview
    response = client.put(
        f"/interviews/{interview_id}",
        json={
            "round": "HR",
            "mode": "Offline",
            "result": "Passed",
            "notes": "HR round completed"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == interview_id
    assert data["round"] == "HR"
    assert data["mode"] == "Offline"
    assert data["result"] == "Passed"
    assert data["notes"] == "HR round completed"



def test_delete_interview(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "deleteinterviewuser",
            "email": "deleteinterviewuser@gmail.com",
            "password": "Test@123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "deleteinterviewuser",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create job
    job_response = client.post(
        "/jobs",
        json={
            "company_name": "Accenture",
            "job_title": "Python Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "700000",
            "application_date": "2026-09-21",
            "status": "Interview",
            "job_url": "https://example.com/job",
            "company_website": "https://www.accenture.com",
            "description": "Python backend role",
            "remote": "False"
        },
        headers=headers
    )

    assert job_response.status_code == 201

    job_id = job_response.json()["id"]

    # Create interview
    interview_response = client.post(
        f"/jobs/{job_id}/interviews",
        json={
            "interview_date": "2026-09-25",
            "round": "Technical",
            "interviewer": "Rahul Sharma",
            "mode": "Online",
            "result": "Pending",
            "notes": "Technical interview"
        },
        headers=headers
    )

    assert interview_response.status_code == 201

    interview_id = interview_response.json()["id"]

    # Delete interview
    response = client.delete(
        f"/interviews/{interview_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Interview deleted successfully"

    # Verify interview is gone
    get_response = client.get(
        f"/jobs/{job_id}/interviews",
        headers=headers
    )

    assert get_response.status_code == 200
    assert get_response.json() == []


def test_user_cannot_access_another_users_interview(client):
    # -------------------------
    # Create User A
    # -------------------------
    client.post(
        "/auth/register",
        json={
            "username": "interviewusera",
            "email": "interviewusera@gmail.com",
            "password": "Test@123"
        }
    )

    login_a = client.post(
        "/auth/login",
        data={
            "username": "interviewusera",
            "password": "Test@123"
        }
    )

    assert login_a.status_code == 200

    token_a = login_a.json()["access_token"]

    headers_a = {
        "Authorization": f"Bearer {token_a}"
    }

    # User A creates a job
    job_response = client.post(
        "/jobs",
        json={
            "company_name": "TCS",
            "job_title": "Python Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "600000",
            "application_date": "2026-09-21",
            "status": "Interview",
            "job_url": "https://example.com/job",
            "company_website": "https://www.tcs.com",
            "description": "User A job",
            "remote": "False"
        },
        headers=headers_a
    )

    assert job_response.status_code == 201

    job_id = job_response.json()["id"]

    # User A creates an interview
    interview_response = client.post(
        f"/jobs/{job_id}/interviews",
        json={
            "interview_date": "2026-09-25",
            "round": "Technical",
            "interviewer": "Rahul Sharma",
            "mode": "Online",
            "result": "Pending",
            "notes": "User A interview"
        },
        headers=headers_a
    )

    assert interview_response.status_code == 201

    interview_id = interview_response.json()["id"]

    # -------------------------
    # Create User B
    # -------------------------
    client.post(
        "/auth/register",
        json={
            "username": "interviewuserb",
            "email": "interviewuserb@gmail.com",
            "password": "Test@123"
        }
    )

    login_b = client.post(
        "/auth/login",
        data={
            "username": "interviewuserb",
            "password": "Test@123"
        }
    )

    assert login_b.status_code == 200

    token_b = login_b.json()["access_token"]

    headers_b = {
        "Authorization": f"Bearer {token_b}"
    }

    # User B tries to update User A's interview
    update_response = client.put(
        f"/interviews/{interview_id}",
        json={
            "result": "Passed"
        },
        headers=headers_b
    )

    assert update_response.status_code == 404

    # User B tries to delete User A's interview
    delete_response = client.delete(
        f"/interviews/{interview_id}",
        headers=headers_b
    )

    assert delete_response.status_code == 404