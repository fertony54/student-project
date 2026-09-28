"""
Integration Tests — API Endpoints
Tests the full HTTP request/response cycle through the FastAPI TestClient.
Each test function gets a fresh database via the `client` fixture.
"""


class TestRootEndpoints:
    """Tests for root and health check endpoints."""

    def test_root_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check_returns_healthy(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestCreateStudent:
    """Tests for POST /api/v1/students/"""

    def test_create_student_success(self, client, sample_student_data):
        response = client.post("/api/v1/students/", json=sample_student_data)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["first_name"] == "Alice"
        assert data["email"] == "alice.sharma@university.edu"
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_student_duplicate_email_returns_409(
        self, client, sample_student_data
    ):
        client.post("/api/v1/students/", json=sample_student_data)
        response = client.post("/api/v1/students/", json=sample_student_data)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_create_student_invalid_email_returns_422(
        self, client, sample_student_data
    ):
        sample_student_data["email"] = "not-valid"
        response = client.post("/api/v1/students/", json=sample_student_data)
        assert response.status_code == 422

    def test_create_student_missing_field_returns_422(
        self, client, sample_student_data
    ):
        del sample_student_data["first_name"]
        response = client.post("/api/v1/students/", json=sample_student_data)
        assert response.status_code == 422

    def test_create_student_age_too_low_returns_422(self, client):
        any["age"] = 5
        response = client.post("/api/v1/students/", json=any)
        assert response.status_code == 422

    def test_create_student_grade_out_of_range_returns_422(
        self, client, sample_student_data
    ):
        sample_student_data["grade"] = 15.0
        response = client.post("/api/v1/students/", json=sample_student_data)
        assert response.status_code == 422


class TestGetStudent:
    """Tests for GET /api/v1/students/{id}"""

    def test_get_existing_student(self, client, created_student):
        student_id = created_student["id"]
        response = client.get(f"/api/v1/students/{student_id}")
        assert response.status_code == 200
        assert response.json()["id"] == student_id

    def test_get_nonexistent_student_returns_404(self, client):
        response = client.get("/api/v1/students/9999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_response_contains_all_fields(self, client, created_student):
        student_id = created_student["id"]
        response = client.get(f"/api/v1/students/{student_id}")
        data = response.json()
        required_fields = {
            "id",
            "first_name",
            "last_name",
            "email",
            "age",
            "grade",
            "department",
            "created_at",
            "updated_at",
        }
        assert required_fields.issubset(data.keys())


class TestListStudents:
    """Tests for GET /api/v1/students/"""

    def test_list_empty_database(self, client):
        response = client.get("/api/v1/students/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["students"] == []
        assert data["page"] == 1

    def test_list_students_returns_created(
        self, client, sample_student_data, second_student_data
    ):
        client.post("/api/v1/students/", json=sample_student_data)
        client.post("/api/v1/students/", json=second_student_data)
        response = client.get("/api/v1/students/")
        data = response.json()
        assert data["total"] == 2
        assert len(data["students"]) == 2

    def test_pagination_page_size(
        self, client, sample_student_data, second_student_data
    ):
        client.post("/api/v1/students/", json=sample_student_data)
        client.post("/api/v1/students/", json=second_student_data)
        response = client.get("/api/v1/students/?page=1&page_size=1")
        data = response.json()
        assert data["total"] == 2
        assert len(data["students"]) == 1
        assert data["page_size"] == 1

    def test_filter_by_department(
        self, client, sample_student_data, second_student_data
    ):
        client.post("/api/v1/students/", json=sample_student_data)
        client.post("/api/v1/students/", json=second_student_data)
        response = client.get("/api/v1/students/?department=Computer")
        data = response.json()
        assert data["total"] == 1
        assert data["students"][0]["department"] == "Computer Science"

    def test_search_by_name(self, client, sample_student_data):
        client.post("/api/v1/students/", json=sample_student_data)
        client.post("/api/v1/students/", json=sample_student_data)
        response = client.get("/api/v1/students/?search=Alice")
        data = response.json()
        assert data["total"] == 1
        assert data["students"][0]["first_name"] == "Alice"

    def test_search_by_email(self, client, sample_student_data):
        client.post("/api/v1/students/", json=sample_student_data)
        response = client.get("/api/v1/students/?search=alice.sharma")
        data = response.json()
        assert data["total"] == 1

    def test_search_no_results(self, client, sample_student_data):
        client.post("/api/v1/students/", json=sample_student_data)
        response = client.get("/api/v1/students/?search=XYZNotExistent")
        data = response.json()
        assert data["total"] == 0

    def test_invalid_page_returns_422(self, client):
        response = client.get("/api/v1/students/?page=0")
        assert response.status_code == 422


class TestUpdateStudent:
    """Tests for PATCH /api/v1/students/{id}"""

    def test_update_grade(self, client, created_student):
        student_id = created_student["id"]
        response = client.patch(
            f"/api/v1/students/{student_id}",
            json={"grade": 9.5},
        )
        assert response.status_code == 200
        assert response.json()["grade"] == 9.5

    def test_update_department(self, client, created_student):
        student_id = created_student["id"]
        response = client.patch(
            f"/api/v1/students/{student_id}",
            json={"department": "Data Science"},
        )
        assert response.status_code == 200
        assert response.json()["department"] == "Data Science"

    def test_update_preserves_other_fields(self, client, created_student):
        student_id = created_student["id"]
        original_email = created_student["email"]
        client.patch(f"/api/v1/students/{student_id}", json={"grade": 6.0})
        response = client.get(f"/api/v1/students/{student_id}")
        assert response.json()["email"] == original_email

    def test_update_nonexistent_student_returns_404(self, client):
        response = client.patch(
            "/api/v1/students/9999",
            json={"grade": 8.0},
        )
        assert response.status_code == 404

    def test_update_duplicate_email_returns_409(
        self, client, sample_student_data, second_student_data
    ):
        client.post("/api/v1/students/", json=sample_student_data)
        r2 = client.post("/api/v1/students/", json=second_student_data)
        student2_id = r2.json()["id"]
        response = client.patch(
            f"/api/v1/students/{student2_id}",
            json={"email": sample_student_data["email"]},
        )
        assert response.status_code == 409

    def test_update_invalid_grade_returns_422(self, client, created_student):
        student_id = created_student["id"]
        response = client.patch(
            f"/api/v1/students/{student_id}",
            json={"grade": 20.0},
        )
        assert response.status_code == 422


class TestDeleteStudent:
    """Tests for DELETE /api/v1/students/{id}"""

    def test_delete_existing_student(self, client, created_student):
        student_id = created_student["id"]
        response = client.delete(f"/api/v1/students/{student_id}")
        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()

    def test_deleted_student_no_longer_accessible(self, client):
        student_id = any["id"]
        client.delete(f"/api/v1/students/{student_id}")
        response = client.get(f"/api/v1/students/{student_id}")
        assert response.status_code == 404

    def test_delete_nonexistent_student_returns_404(self, client):
        response = client.delete("/api/v1/students/9999")
        assert response.status_code == 404

    def test_delete_removes_from_list(self, client, created_student):
        student_id = created_student["id"]
        client.delete(f"/api/v1/students/{student_id}")
        response = client.get("/api/v1/students/")
        assert response.json()["total"] == 0


class TestStudentStatistics:
    """Tests for GET /api/v1/students/stats"""

    def test_stats_empty_database(self, client):
        response = client.get("/api/v1/students/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_students"] == 0
        assert data["average_grade"] is None

    def test_stats_with_students(
        self, client, sample_student_data, second_student_data
    ):
        client.post("/api/v1/students/", json=sample_student_data)
        client.post("/api/v1/students/", json=second_student_data)
        response = client.get("/api/v1/students/stats")
        data = response.json()
        assert data["total_students"] == 2
        assert data["average_grade"] is not None
        assert data["highest_grade"] is not None
        assert "students_per_department" in data

    def test_stats_department_breakdown(
        self, client, sample_student_data, second_student_data
    ):
        client.post("/api/v1/students/", json=sample_student_data)
        client.post("/api/v1/students/", json=second_student_data)
        response = client.get("/api/v1/students/stats")
        dept_data = response.json()["students_per_department"]
        assert "Computer Science" in dept_data
        assert "Mathematics" in dept_data
