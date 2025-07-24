from app.security.security import create_access_token, SECRET_KEY, ALGORITHM
from jwt import decode

def test_jwt_token():
    data = {"test": "teste@teste.com"}
    token = create_access_token(data)
    decoded_token = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["test"] == data["test"]
   

# def test_verify_password():
#     plain_password = "123456"
#     hashed_password = get_password_hash(plain_password)
#     assert verify_password(plain_password, hashed_password)