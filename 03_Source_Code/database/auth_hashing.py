import sys
import os
import logging

# Set up professional logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Resolve backend path dynamically
backend_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', 'AgriCareer-Tracker-Progress-', 'backend')
)
if backend_path not in sys.path:
    sys.path.append(backend_path)

try:
    from fastapi.testclient import TestClient
    from app.main import app
    from app.models import user_repo, db_file
except ModuleNotFoundError as e:
    logger.error(f"Failed to load backend modules. Ensure the path is correct. Error: {e}")
    sys.exit(1)

client = TestClient(app)

def run_integration_tests():
    """
    Executes integration tests for the authentication endpoints.
    """
    logger.info(f"Starting authentication tests against DB: {db_file}")
    
    test_user = {
        "username": "test_auth_user",
        "password": "SecurePassword123!",
        "full_name": "Test Auth User",
        "email": "test_auth@students.ac.id",
        "nim": "J0403211099",
        "role": "mahasiswa"
    }

    # 1. Registration Test
    if not user_repo.get_user(test_user["username"]):
        response = client.post("/auth/register", json=test_user)
        assert response.status_code == 200, f"Registration failed: {response.text}"
        logger.info("Registration endpoint test passed.")
    else:
        logger.info("Test user already exists. Skipping registration.")

    # Display the structure of the hash and highlight the salt
    user_data = user_repo.get_user(test_user["username"])
    if user_data:
        full_hash = user_data["hashed_password"]
        parts = full_hash.split('$')
        # Typical passlib sha256_crypt hash: $5$rounds=535000$salt_string$checksum
        if len(parts) >= 5:
            logger.info("--- Hashing & Salting Breakdown ---")
            logger.info(f"Full String in DB : {full_hash}")
            logger.info(f"[1] Algorithm ID  : {parts[1]} (sha256_crypt)")
            logger.info(f"[2] Cost/Rounds   : {parts[2]}")
            logger.info(f"[3] SALT          : {parts[3]}  <-- Ini adalah Salt-nya")
            logger.info(f"[4] Checksum/Hash : {parts[4]}")
            logger.info("-----------------------------------")

    # Bypass email verification to proceed with login testing
    user_repo.update_is_verified(test_user["username"], True)

    # 2. Login Test (Valid Credentials)
    login_payload = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200, f"Login failed: {response.text}"
    
    data = response.json()
    assert "access_token" in data, "Token missing in response"
    logger.info("Login endpoint test (valid credentials) passed.")
    logger.info(f"Bearer Token: {data['access_token']}")

    # 3. Login Test (Invalid Credentials)
    invalid_login_payload = {
        "username": test_user["username"],
        "password": "WrongPassword123!"
    }
    response = client.post("/auth/login", json=invalid_login_payload)
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    logger.info("Login endpoint test (invalid credentials) passed.")

    logger.info("All integration tests executed successfully.")

if __name__ == '__main__':
    run_integration_tests()
