
from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)
app.secret_key = 'eureka_secret_key_2025'  # Change this in production
import copy

USERS_FILE = os.path.join("data", "users.json")

def load_users():
    with open(USERS_FILE) as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def get_user(username):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

def update_user(username, new_data):
    users = load_users()
    for i, user in enumerate(users):
        if user['username'] == username:
            users[i].update(new_data)
            save_users(users)
            return True
    return False
#home

# === AUTH & PROFILE ===
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('user'):
        # Not logged in: show login form
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            user = get_user(username)
            if user and user['password'] == password and user['role'] == role:
                session['user'] = {'username': user['username'], 'role': user['role']}
                return redirect(url_for('profile'))
            return render_template('profile.html', login_error='Invalid credentials', user=None)
        return render_template('profile.html', user=None)
    else:
        # Logged in: show dashboard
        user = get_user(session['user']['username'])
        return render_template('profile.html', user=user)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('profile'))

@app.route('/change_password', methods=['POST'])
def change_password():
    if not session.get('user'):
        return redirect(url_for('profile'))
    username = session['user']['username']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    if new_password != confirm_password or not new_password:
        user = get_user(username)
        return render_template('profile.html', user=user, pw_error='Passwords do not match')
    update_user(username, {'password': new_password})
    user = get_user(username)
    return render_template('profile.html', user=user, pw_success='Password changed successfully')

# === NOTES ===
@app.route('/add_note', methods=['POST'])
def add_note():
    if not session.get('user'):
        return redirect(url_for('profile'))
    username = session['user']['username']
    title = request.form['title']
    content = request.form['content']
    user = get_user(username)
    notes = user.get('notes', [])
    notes.append({'title': title, 'content': content})
    update_user(username, {'notes': notes})
    return redirect(url_for('profile'))

@app.route('/delete_note', methods=['POST'])
def delete_note():
    if not session.get('user'):
        return redirect(url_for('profile'))
    username = session['user']['username']
    title = request.form['title']
    user = get_user(username)
    notes = [n for n in user.get('notes', []) if n['title'] != title]
    update_user(username, {'notes': notes})
    return redirect(url_for('profile'))
CORS(app)



contact_submissions = []

# ===== ROUTES =====

def load_json(filename):
    with open(os.path.join("data", filename)) as f:
        return json.load(f)

#home
@app.route("/api/home", methods=["GET"])
def get_home():
    return jsonify(load_json("home.json"))




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/admissions")
def admissions():
    return render_template("admission.html")

@app.route("/programs")
def programs():
    return render_template("programs.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about/eureka")
def about_eureka():
    return render_template("about/eureka.html")

@app.route("/about/vision")
def about_vision():
    return render_template("about/vision.html")

@app.route("/about/achievements")
def about_achievements():
    return render_template("about/achievements.html")

@app.route("/about/faculty")
def about_faculty():
    return render_template("about/faculty.html")



if __name__ == "__main__":
    app.run(debug=True)
