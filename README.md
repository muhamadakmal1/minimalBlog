<div id="top"></div>

<div align="center" class="text-center">

<h1>📝 minimalBlog — A Minimal Flask Blog Platform</h1>
<p><em>Clean, Lightweight & JSON-powered Blogging</em></p>

<img alt="last-commit" src="https://img.shields.io/github/last-commit/muhamadakmal1/minimalBlog?style=flat-square"/>
<img alt="repo-size" src="https://img.shields.io/github/repo-size/muhamadakmal1/minimalBlog?style=flat-square"/>
<img alt="license" src="https://img.shields.io/github/license/muhamadakmal1/minimalBlog?style=flat-square"/>

</div>

---

## 📌 Overview

**minimalBlog** is a clean and lightweight blog platform built using Flask and JSON for data storage. It's ideal for learning purposes, quick setups, and personal blogging with minimal dependencies.

---

## 📂 Dataset & Storage

- Blog posts are stored in: `posts.json`
- User profile info in: `profile.json`
- Saved/draft posts in: `save_post.json`

This removes the need for a full database setup, making the project portable and easy to manage.

---

## 🧠 Project Structure

```bash
minimalBlog/
├── static/             # CSS, JS, and image assets
├── templates/          # Jinja2 HTML templates
├── app.py              # Flask app main file
├── posts.json          # Blog posts data
├── profile.json        # User profile
├── save_post.json      # Saved/draft posts
└── requirements.txt    # Python dependencies


# 1. Clone the repository
git clone https://github.com/muhamadakmal1/minimalBlog.git
cd minimalBlog

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

# 3. Install required packages
pip install -r requirements.txt

# 4. Run the Flask server
python app.py
```
------
Features
📝 Create and display blog posts

🧑‍💼 Update profile via profile.json

💾 Save or draft posts

📄 Static template rendering

🌐 No database required (fully file-based)


#🤝 Contribution<br>
Pull requests are welcome! Please fork this repo and submit a PR for improvements or new features.

#📬 Contact<br>
Muhamad Akmal<br>
📧 mohammadakmal152@gmail.com
🌐 <a href='https://github.com/muhamadakmal1/'>GitHub Profile</a>


