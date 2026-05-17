import requests

API = "http://localhost:8000"

# Login as adv1
r = requests.post(f"{API}/auth/jwt/login", data={"username": "adv1@bad.net", "password": "12345678"})
token = r.json()["access_token"]
print("Logged in as adv1")

# Delete the test post
d = requests.delete(f"{API}/posts/6b744577bbe5499498277e560841b015", headers={"Authorization": f"Bearer {token}"})
print(f"Delete status: {d.status_code}")
print(d.json())

# Verify feed is empty
f = requests.get(f"{API}/feed", headers={"Authorization": f"Bearer {token}"})
posts = f.json()["posts"]
print(f"Posts remaining: {len(posts)}")
