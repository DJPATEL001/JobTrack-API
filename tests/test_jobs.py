def test_create_job(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "jobuser",
            "email": "jobuser@gmail.com",
            "password": "Test@123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "jobuser",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Create job
    response = client.post(
        "/jobs",
        json={
            "company_name": "TCS",
            "job_title": "Python Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "500000",
            "application_date": "2026-09-21",
            "status": "Applied",
            "job_url": "https://example.com/job",
            "company_website": "https://www.tcs.com",
            "description": "Python backend developer role",
            "remote": "False"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    assert response.status_code == 201

    data = response.json()

    assert data["company_name"] == "TCS"
    assert data["job_title"] == "Python Developer"
    assert data["status"] == "Applied"
    assert "id" in data


def test_get_jobs(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "getjobsuser",
            "email": "getjobsuser@gmail.com",
            "password": "Test@123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "getjobsuser",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create a job
    create_response = client.post(
        "/jobs",
        json={
            "company_name": "Infosys",
            "job_title": "Python Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "600000",
            "application_date": "2026-09-21",
            "status": "Applied",
            "job_url": "https://example.com/job",
            "company_website": "https://www.infosys.com",
            "description": "Backend Python role",
            "remote": "False"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    # Get jobs
    response = client.get(
        "/jobs",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["company_name"] == "Infosys"
    assert data[0]["job_title"] == "Python Developer"


def test_get_single_job(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "singlejobuser",
            "email": "singlejobuser@gmail.com",
            "password": "Test@123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "singlejobuser",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create job
    create_response = client.post(
        "/jobs",
        json={
            "company_name": "eInfochips",
            "job_title": "Python Backend Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "700000",
            "application_date": "2026-09-21",
            "status": "Applied",
            "job_url": "https://example.com/job",
            "company_website": "https://www.einfochips.com",
            "description": "Python backend position",
            "remote": "False"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    job_id = create_response.json()["id"]

    # Get single job
    response = client.get(
        f"/jobs/{job_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job_id
    assert data["company_name"] == "eInfochips"
    assert data["job_title"] == "Python Backend Developer"


def test_update_job(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "updatejobuser",
            "email": "updatejobuser@gmail.com",
            "password": "Test@123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "updatejobuser",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create job
    create_response = client.post(
        "/jobs",
        json={
            "company_name": "Wipro",
            "job_title": "Python Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "600000",
            "application_date": "2026-09-21",
            "status": "Applied",
            "job_url": "https://example.com/job",
            "company_website": "https://www.wipro.com",
            "description": "Python developer position",
            "remote": "False"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    job_id = create_response.json()["id"]

    # Update job
    response = client.put(
        f"/jobs/{job_id}",
        json={
            "job_title": "Senior Python Developer",
            "salary": "800000",
            "location": "Gandhinagar"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["job_title"] == "Senior Python Developer"
    assert data["salary"] == "800000"
    assert data["location"] == "Gandhinagar"


def test_update_job_status(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "statususer",
            "email": "statususer@gmail.com",
            "password": "Test@123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "statususer",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create job
    create_response = client.post(
        "/jobs",
        json={
            "company_name": "Accenture",
            "job_title": "Python Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "700000",
            "application_date": "2026-09-21",
            "status": "Applied",
            "job_url": "https://example.com/job",
            "company_website": "https://www.accenture.com",
            "description": "Python backend role",
            "remote": "False"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    job_id = create_response.json()["id"]

    # Update status
    response = client.patch(
        f"/jobs/{job_id}/status",
        json={
            "status": "Interview"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Interview"


def test_delete_job(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "deleteuser",
            "email": "deleteuser@gmail.com",
            "password": "Test@123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "deleteuser",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create job
    create_response = client.post(
        "/jobs",
        json={
            "company_name": "IBM",
            "job_title": "Python Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "650000",
            "application_date": "2026-09-21",
            "status": "Applied",
            "job_url": "https://example.com/job",
            "company_website": "https://www.ibm.com",
            "description": "Python backend role",
            "remote": "False"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    job_id = create_response.json()["id"]

    # Delete job
    response = client.delete(
        f"/jobs/{job_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Job deleted successfully"

    # Verify job no longer exists
    get_response = client.get(
        f"/jobs/{job_id}",
        headers=headers
    )

    assert get_response.status_code == 404


def test_user_cannot_access_another_users_job(client):
    # -------------------------
    # Create User A
    # -------------------------
    client.post(
        "/auth/register",
        json={
            "username": "usera",
            "email": "usera@gmail.com",
            "password": "Test@123"
        }
    )

    login_a = client.post(
        "/auth/login",
        data={
            "username": "usera",
            "password": "Test@123"
        }
    )

    assert login_a.status_code == 200

    token_a = login_a.json()["access_token"]

    headers_a = {
        "Authorization": f"Bearer {token_a}"
    }

    # User A creates a job
    create_response = client.post(
        "/jobs",
        json={
            "company_name": "TCS",
            "job_title": "Python Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "600000",
            "application_date": "2026-09-21",
            "status": "Applied",
            "job_url": "https://example.com/job",
            "company_website": "https://www.tcs.com",
            "description": "User A job",
            "remote": "False"
        },
        headers=headers_a
    )

    assert create_response.status_code == 201

    job_id = create_response.json()["id"]

    # -------------------------
    # Create User B
    # -------------------------
    client.post(
        "/auth/register",
        json={
            "username": "userb",
            "email": "userb@gmail.com",
            "password": "Test@123"
        }
    )

    login_b = client.post(
        "/auth/login",
        data={
            "username": "userb",
            "password": "Test@123"
        }
    )

    assert login_b.status_code == 200

    token_b = login_b.json()["access_token"]

    headers_b = {
        "Authorization": f"Bearer {token_b}"
    }

    # -------------------------
    # User B tries to access
    # User A's job
    # -------------------------
    response = client.get(
        f"/jobs/{job_id}",
        headers=headers_b
    )

    assert response.status_code == 404

def test_get_nonexistent_job(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "nonexistent_user",
            "email": "nonexistent@example.com",
            "password": "password123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent_user",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    # Request a job that does not exist
    response = client.get(
        "/jobs/99999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404


def test_get_single_job(client):
    register_response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/jobs/99999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404


def test_user_cannot_update_another_users_job(client):
    # User 1
    client.post(
        "/auth/register",
        json={
            "username": "user_update_1",
            "email": "update1@example.com",
            "password": "password123"
        }
    )

    login1 = client.post(
        "/auth/login",
        data={
            "username": "user_update_1",
            "password": "password123"
        }
    )

    token1 = login1.json()["access_token"]

    # User 1 creates a job
    job_response = client.post(
        "/jobs",
        headers={"Authorization": f"Bearer {token1}"},
        json={
            "company_name": "Company A",
            "job_title": "Python Developer",
            "location": "Ahmedabad",
            "job_type": "Full-time",
            "salary": "500000",
            "application_date": "2026-09-21",
            "status": "Applied",
            "job_url": "https://example.com",
            "company_website": "https://example.com",
            "description": "Backend role",
            "remote": "False"
        }
    )

    job_id = job_response.json()["id"]

    # User 2
    client.post(
        "/auth/register",
        json={
            "username": "user_update_2",
            "email": "update2@example.com",
            "password": "password123"
        }
    )

    login2 = client.post(
        "/auth/login",
        data={
            "username": "user_update_2",
            "password": "password123"
        }
    )

    token2 = login2.json()["access_token"]

    # User 2 tries to update User 1's job
    response = client.put(
        f"/jobs/{job_id}",
        headers={"Authorization": f"Bearer {token2}"},
        json={
            "job_title": "Senior Python Developer"
        }
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_job(client):
    # User 1
    client.post(
        "/auth/register",
        json={
            "username": "user_delete_1",
            "email": "delete1@example.com",
            "password": "password123"
        }
    )

    login1 = client.post(
        "/auth/login",
        data={
            "username": "user_delete_1",
            "password": "password123"
        }
    )

    token1 = login1.json()["access_token"]

    # User 1 creates a job
    job_response = client.post(
        "/jobs",
        headers={"Authorization": f"Bearer {token1}"},
        json={
            "company_name": "Company B",
            "job_title": "Backend Developer",
            "location": "Gandhinagar",
            "job_type": "Full-time",
            "salary": "600000",
            "application_date": "2026-09-21",
            "status": "Applied",
            "job_url": "https://example.com",
            "company_website": "https://example.com",
            "description": "Python backend role",
            "remote": "False"
        }
    )

    job_id = job_response.json()["id"]

    # User 2
    client.post(
        "/auth/register",
        json={
            "username": "user_delete_2",
            "email": "delete2@example.com",
            "password": "password123"
        }
    )

    login2 = client.post(
        "/auth/login",
        data={
            "username": "user_delete_2",
            "password": "password123"
        }
    )

    token2 = login2.json()["access_token"]

    # User 2 tries to delete User 1's job
    response = client.delete(
        f"/jobs/{job_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )

    assert response.status_code == 404