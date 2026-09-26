# 🎓 Scholarship Finder

A full-stack web application that helps students discover, explore, match, and save scholarship opportunities in one place.

## 🌐 Links

🔗 **Live Website:**https://scholarship-finder-dvkw.onrender.com/

🔗 **GitHub Repository:** https://github.com/krithikaabbagoni111-dev/scholarship-finder.git

---

## 📌 About

Finding suitable scholarships can be difficult because information is often spread across different platforms.

**Scholarship Finder** provides a centralized platform where students can explore scholarship opportunities based on their education, course, category, state, and eligibility.

The application also includes an admin system for managing scholarship information.

---

## ✨ Features

### 👨‍🎓 Student Features

- 🔐 User registration and login
- 👤 Student profile
- 🎓 Browse scholarships
- 🔎 Search and explore opportunities
- ✨ Personalized scholarship matches
- 📋 View scholarship details
- ❤️ Save scholarships
- 📱 Mobile-responsive design
- 🚪 Secure logout

### 👑 Admin Features

- 🔐 Admin authentication
- 📊 Admin dashboard
- ➕ Add scholarships
- ✏️ Edit scholarships
- 🗑️ Delete scholarships
- 📋 Manage scholarship information

---

## 🛠️ Tech Stack

**Frontend**
- HTML5
- CSS3
- JavaScript
- Jinja2

**Backend**
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login

**Database**
- PostgreSQL

**Tools & Deployment**
- Visual Studio Code
- Git
- GitHub
- Render

---

## 🏗️ Project Structure

```text
Scholarship-Finder/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── navbar.html
│   ├── scholarships.html
│   ├── matches.html
│   └── ...
│
└── static/
    ├── css/
    │   ├── style.css
    │   └── dashboard.css
    └── ...
⚙️ Run Locally
1. Clone the repository
git clone https://github.com/krithikaabbagoni111-dev/scholarship-finder.git
2. Open the project
cd Scholarship-Finder
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment

Windows:

venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
6. Configure environment variables

Create a .env file locally and add the required environment variables for the application.

Do not upload .env to GitHub.

7. Run the application
python app.py

Open:

http://127.0.0.1:5000
🗄️ Database

The production application uses PostgreSQL.

The database stores:

User accounts
Student profiles
Scholarship information
Saved scholarships
Administrative information

Database credentials are stored using environment variables and are not included in the source code.

🚀 Deployment

The application is deployed using Render with PostgreSQL as the production database.

Local Development
       ↓
     Git
       ↓
    GitHub
       ↓
     Render
       ↓
  PostgreSQL
       ↓
 Live Website


🔐 Security

The project uses:

Password hashing
User authentication
Admin authorization
Environment variables for sensitive information
.gitignore for local secrets
PostgreSQL for production data

Sensitive credentials should never be committed to GitHub.

📱 Responsive Design

Scholarship Finder is designed for:

💻 Desktop
💻 Laptop
📱 Mobile
📲 Tablet

The application includes a mobile-friendly navigation menu for smaller screens.

🔮 Future Enhancements
🤖 AI-powered scholarship recommendations
🎯 Advanced eligibility matching
📧 Email deadline reminders
🔔 Scholarship deadline notifications
📊 Student application tracking
📱 Dedicated mobile application
🌐 Integration with more scholarship sources
👩‍💻 Developer

Krithika

B.Tech – Information Technology
Diploma – Cloud Computing & Big Data

📄 License

This project was developed as an educational and portfolio project.

