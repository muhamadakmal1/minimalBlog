import os
import json
import markdown
import plotly.graph_objs as go
import plotly.io as pio
from flask import Flask, render_template, request, redirect, url_for, abort, session, flash
from werkzeug.utils import secure_filename
from datetime import datetime
import re
app = Flask(__name__)
app.secret_key = "supersecretkey"


def generate_slug(title):
    slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug


# Configs
UPLOAD_FOLDER = "static/uploads"
PROFILE_FOLDER = "static/profile"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROFILE_FOLDER"] = PROFILE_FOLDER

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "pass123"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_posts():
    try:
        with open("posts.json", "r", encoding="utf-8") as f:
            posts = json.load(f)
    except (UnicodeDecodeError, FileNotFoundError):
        posts = []
    for idx, post in enumerate(posts, start=1):
        post['id'] = idx
        post.setdefault("reads", 0)
    return posts

def save_posts(posts):
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

def save_post(new_post):
    posts = load_posts()
    new_post['id'] = len(posts) + 1
    posts.append(new_post)
    save_posts(posts)

@app.template_filter('markdown')
def markdown_filter(text):
    return markdown.markdown(text)

def load_admin_profile():
    try:
        with open("profile.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("profile_image", None)
    except FileNotFoundError:
        return None

def save_admin_profile(filename):
    with open("profile.json", "w", encoding="utf-8") as f:
        json.dump({"profile_image": filename}, f, indent=2)

@app.route("/")
def index():
    posts = load_posts()
    return render_template("index.html", posts=posts)

@app.route("/post/<int:post_id>")
def post_detail(post_id):
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        abort(404)

    post['reads'] += 1
    save_posts(posts)
    post['content'] = markdown.markdown(post['content'], extensions=['fenced_code', 'codehilite'])
    return render_template("post_detail.html", post=post)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("admin_login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))

@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    
    if not session.get("admin"):
        
        return redirect(url_for("admin_login"))

    posts = load_posts()
    profile_image = load_admin_profile()

    if request.method == "POST":
        if "profile_image" in request.files:
            profile_img = request.files["profile_image"]
            if profile_img and allowed_file(profile_img.filename):
                filename = secure_filename(profile_img.filename)
                profile_img.save(os.path.join(app.config["PROFILE_FOLDER"], filename))
                save_admin_profile(filename)
                flash("Profile image updated!", "success")
                return redirect(url_for("admin_dashboard"))

        title = request.form.get("title")
        readTime = int(request.form.get("readTime", 0))
        excerpt = request.form.get("excerpt")
        content = request.form.get("content")

        image_filename = None
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename

        date = datetime.now().strftime("%B %d, %Y %H:%M:%S")

        post = {
            "title": title,
            "date": date,
            "readTime": readTime,
            "excerpt": excerpt,
            "content": content,
            "image": image_filename,
            "reads": 0
        }
        save_post(post)
        flash("Post published successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    titles = [post["title"] for post in posts]
    reads = [post["reads"] for post in posts]
    total_reads = sum(reads)

    fig = go.Figure([go.Bar(x=titles, y=reads, marker=dict(color="skyblue"))])
    fig.update_layout(
        title="\U0001F4CA Reads per Post",
        xaxis_title="Post Title",
        yaxis_title="Reads",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    graph_html = pio.to_html(fig, full_html=False)

    return render_template(
        "admin_dashboard.html",
        posts=posts,
        profile_image=profile_image,
        total_reads=total_reads,
        graph_html=graph_html
    )

@app.route("/admin/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        abort(404)

    if request.method == "POST":
        post['title'] = request.form["title"]
        post['readTime'] = int(request.form["readTime"])
        post['excerpt'] = request.form["excerpt"]
        post['content'] = request.form["content"]
        post['private'] = request.form.get("private") == "yes"

        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                post['image'] = filename

        save_posts(posts)
        flash("Post updated successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("edit_post.html", post=post)

@app.route("/admin/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    
    posts = load_posts()
    posts = [p for p in posts if p['id'] != post_id]
    
    # Reassign new IDs to maintain consistency
    for idx, post in enumerate(posts, start=1):
        post['id'] = idx
    
    save_posts(posts)
    flash("Post deleted successfully!", "success")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(PROFILE_FOLDER):
        os.makedirs(PROFILE_FOLDER)
    app.run(debug=True)
