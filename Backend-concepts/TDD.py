from flask import Flask, jsonify, request
from datetime import date

app = Flask(__name__)

# --- User class ---
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def __repr__(self):
        return f"User({self.name}, {len(self.tasks)} tasks)"

# --- Database ---
user_db = {}

alice = User("alice", "alice@company.com")
bob = User("bob", "bob@company.com")

alice.add_task({"title": "Fix login bug", "due": date(2025, 1, 1), "done": False})
alice.add_task({"title": "Write docs",    "due": date(2026, 12, 1), "done": False})
bob.add_task({"title": "Deploy service", "due": date(2025, 3, 1), "done": True})

user_db["alice@company.com"] = alice
user_db["bob@company.com"] = bob


# --- Routes ---
@app.route("/users", methods=["GET"])
def get_users():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 2, type=int)
    
    all_users = list(user_db.values())
    start = (page - 1) * limit
    end = start + limit
    results = all_users[start:end]
    
    return jsonify({
        "page": page,
        "limit": limit,
        "total": len(user_db),
        "users": [{"name": u.name, "email": u.email} for u in results]
    }), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or "email" not in data or "name" not in data:
        return jsonify({"error": "name and email are required"}), 400

    email = data["email"]
    name = data["name"] # this will crash if the user doesnt send name. We need INPUT VALIDATION 

    if email in user_db:
        return jsonify({"error": "User already exists"}), 400
    
    new_user = User(name, email)
    user_db[email] = new_user
    return jsonify({"name": name, "email": email}), 201



# ====== TESTS ======

def test_create_user():
    client = app.test_client()
    response = client.post("/users", json={
        "name": "charlie",
        "email": "charlie@company.com"
    })
    assert response.status_code == 201
    assert "charlie@company.com" in user_db
    print("✅ test_create_user passed")


test_create_user()


def test_create_user_missing_fields():
    client = app.test_client()
    response = client.post("/users", json={
        "email": "charlie@company.com"
    })
    assert response.status_code == 400
    print("✅ test_create_user_missing_fields passed")


test_create_user_missing_fields()


# ===== ASYNC ======

async def create_user2(email, name):
    existing = await user_db.find_user(email)
    if existing:
        raise ValueError("User already exists")
    user = await user_db.insert_user(email, name)
    return user


# ===== APP RUN ======

if __name__ == "__main__":
    app.run(debug=True)
