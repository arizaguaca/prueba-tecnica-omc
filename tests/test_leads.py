import pytest

def test_create_lead(client):
    response = client.post(
        "/api/v1/leads/",
        json={
            "nombre": "Test User",
            "email": "test@example.com",
            "telefono": "123456789",
            "fuente": "facebook",
            "producto_interes": "Test Product",
            "presupuesto": 1000.0
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_read_leads(client):
    # Ensure there is at least one lead
    client.post(
        "/api/v1/leads/",
        json={
            "nombre": "Lead 1",
            "email": "lead1@example.com",
            "fuente": "instagram"
        }
    )
    
    response = client.get("/api/v1/leads/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_read_lead_by_id(client):
    post_response = client.post(
        "/api/v1/leads/",
        json={
            "nombre": "Unique User",
            "email": "unique@example.com"
        }
    )
    lead_id = post_response.json()["id"]
    
    get_response = client.get(f"/api/v1/leads/{lead_id}")
    assert get_response.status_code == 200
    assert get_response.json()["nombre"] == "Unique User"

def test_update_lead(client):
    post_response = client.post(
        "/api/v1/leads/",
        json={
            "nombre": "Before Update",
            "email": "update@example.com"
        }
    )
    lead_id = post_response.json()["id"]
    
    patch_response = client.patch(
        f"/api/v1/leads/{lead_id}",
        json={"nombre": "After Update", "presupuesto": 500.0}
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["nombre"] == "After Update"
    assert patch_response.json()["presupuesto"] == 500.0

def test_soft_delete_lead(client):
    post_response = client.post(
        "/api/v1/leads/",
        json={
            "nombre": "Delete Me",
            "email": "delete@example.com"
        }
    )
    lead_id = post_response.json()["id"]
    
    delete_response = client.delete(f"/api/v1/leads/{lead_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["deleted_at"] is not None
    
    # Verify it doesn't show in list
    list_response = client.get("/api/v1/leads/")
    ids = [l["id"] for l in list_response.json()]
    assert lead_id not in ids

def test_get_stats(client):
    client.post(
        "/api/v1/leads/",
        json={
            "nombre": "Stats User",
            "email": "stats@example.com",
            "presupuesto": 100.0
        }
    )
    response = client.get("/api/v1/leads/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_leads" in data
    assert "average_budget" in data

def test_get_ai_summary(client):
    # Ensure there's data
    client.post(
        "/api/v1/leads/",
        json={
            "nombre": "AI User",
            "email": "ai@example.com"
        }
    )
    response = client.post("/api/v1/leads/ai/summary")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "is_mock" in data
