from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)


app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "development-secret-key"
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scholarship.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


# =========================================================
# LOGIN CONFIGURATION
# =========================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message = "Please login to continue."


# =========================================================
# USER MODEL
# =========================================================

class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    course = db.Column(
        db.String(100)
    )

    state = db.Column(
        db.String(100)
    )

    category = db.Column(
        db.String(100)
    )

    gender = db.Column(
        db.String(50)
    )

    family_income = db.Column(
        db.Integer
    )
    is_admin = db.Column(
    db.Boolean,
    default=False
)
# =========================================================
# SCHOLARSHIP MODEL
# =========================================================

class Scholarship(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(200),
        nullable=False
    )

    provider = db.Column(
        db.String(200)
    )

    description = db.Column(
        db.Text
    )

    amount = db.Column(
        db.String(100)
    )

    course = db.Column(
        db.String(200)
    )

    state = db.Column(
        db.String(100)
    )

    category = db.Column(
        db.String(100)
    )

    deadline = db.Column(
        db.String(100)
    )

    income_limit = db.Column(
        db.String(200)
    )

    application_link = db.Column(
        db.String(500)
    )
    gender = db.Column(
    db.String(50)
)
class SavedScholarship(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    scholarship_id = db.Column(
        db.Integer,
        db.ForeignKey("scholarship.id"),
        nullable=False
    )

# =========================================================
# LOAD USER
# =========================================================

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


# =========================================================
# HOME PAGE
# =========================================================

def calculate_match(user, scholarship):

    score = 0

    reasons = []


    # COURSE MATCH

    if user.course and scholarship.course:

        if user.course.lower() in scholarship.course.lower():

            score += 30

            reasons.append(
                "Your course matches"
            )


    # STATE MATCH

    if user.state and scholarship.state:

        if (
            user.state.lower()
            in scholarship.state.lower()
            or
            scholarship.state.lower()
            in user.state.lower()
        ):

            score += 20

            reasons.append(
                "Your state matches"
            )


    # CATEGORY MATCH

    if user.category:

        if scholarship.category:

            if (
                user.category.lower()
                in scholarship.category.lower()
            ):

                score += 20

                reasons.append(
                    "Your category matches"
                )


    # INCOME MATCH

    if user.family_income:

        if scholarship.income_limit:

            try:

                income_limit = int(
                    scholarship.income_limit
                    .replace(",", "")
                    .replace("₹", "")
                    .replace("Rs.", "")
                    .strip()
                )

                if user.family_income <= income_limit:

                    score += 20

                    reasons.append(
                        "Your family income is eligible"
                    )

            except ValueError:

                pass


    # GENERAL BONUS

    if score == 0:

        score = 10

        reasons.append(
            "Explore this scholarship for more details"
        )


    return score, reasons

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# SCHOLARSHIPS PAGE
# =========================================================

@app.route("/scholarships")
def scholarships():

    search = request.args.get(
        "search",
        ""
    ).strip()

    course = request.args.get(
        "course",
        ""
    ).strip()

    state = request.args.get(
        "state",
        ""
    ).strip()

    category = request.args.get(
        "category",
        ""
    ).strip()


    query = Scholarship.query


    if search:

        query = query.filter(
            db.or_(
                Scholarship.name.ilike(
                    f"%{search}%"
                ),
                Scholarship.provider.ilike(
                    f"%{search}%"
                )
            )
        )


    if course:

        query = query.filter(
            Scholarship.course.ilike(
                f"%{course}%"
            )
        )


    if state:

        query = query.filter(
            Scholarship.state.ilike(
                f"%{state}%"
            )
        )


    if category:

        query = query.filter(
            Scholarship.category.ilike(
                f"%{category}%"
            )
        )


    all_scholarships = query.all()


    return render_template(
        "scholarships.html",
        scholarships=all_scholarships,
        search=search,
        selected_course=course,
        selected_state=state,
        selected_category=category
    )


# =========================================================
# SCHOLARSHIP DETAILS
# =========================================================

@app.route(
    "/scholarship/<int:scholarship_id>"
)
def scholarship_details(scholarship_id):

    scholarship = Scholarship.query.get_or_404(
        scholarship_id
    )

    return render_template(
        "scholarship_details.html",
        scholarship=scholarship
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    # If already logged in
    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )


    # When form is submitted
    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        course = request.form.get(
            "course",
            ""
        )

        state = request.form.get(
            "state",
            ""
        )
        category = request.form.get(
            "category",
             ""
        )

        gender = request.form.get(
         "gender",
           ""
         )

        family_income_text = request.form.get(
            "family_income",
             ""
        )

        # Check required fields

        if not name or not email or not password:

            flash(
                "Please fill in all required fields.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        # Check existing email

        existing_user = User.query.filter_by(
            email=email
        ).first()


        if existing_user:

            flash(
                "An account with this email already exists.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        # Hash password

        hashed_password = generate_password_hash(
            password
        )


        # Create user
        try:

         family_income = int(
        family_income_text
         ) if family_income_text else None

        except ValueError:

         family_income = None

        new_user = User(

            name=name,

            email=email,

            password=hashed_password,

            course=course,

            state=state,

            category=category,

            gender=gender,

            family_income=family_income

        )


        db.session.add(
            new_user
        )

        db.session.commit()


        flash(
            "Account created successfully! Please login.",
            "success"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # Already logged in

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )


    # Form submitted

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        # Find user

        user = User.query.filter_by(
            email=email
        ).first()


        # Check password

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)


            return redirect(
                url_for("dashboard")
            )


        flash(
            "Invalid email or password.",
            "error"
        )


    return render_template(
        "login.html"
    )


# =========================================================
# DASHBOARD
# =========================================================
@app.route(
    "/save-scholarship/<int:scholarship_id>",
    methods=["POST"]
)
@login_required
def save_scholarship(scholarship_id):

    scholarship = Scholarship.query.get_or_404(
        scholarship_id
    )

    existing_save = SavedScholarship.query.filter_by(
        user_id=current_user.id,
        scholarship_id=scholarship.id
    ).first()

    if existing_save:

        db.session.delete(
            existing_save
        )

        db.session.commit()

        flash(
            "Scholarship removed from saved list.",
            "success"
        )

    else:

        new_save = SavedScholarship(

            user_id=current_user.id,

            scholarship_id=scholarship.id

        )

        db.session.add(
            new_save
        )

        db.session.commit()

        flash(
            "Scholarship saved successfully! ❤️",
            "success"
        )

    return redirect(
        url_for(
            "scholarship_details",
            scholarship_id=scholarship.id
        )
    )

@app.route(
    "/admin/add-scholarship",
    methods=["GET", "POST"]
)
@login_required
def add_scholarship():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        provider = request.form.get(
            "provider",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        amount = request.form.get(
            "amount",
            ""
        ).strip()

        course = request.form.get(
            "course",
            ""
        ).strip()

        state = request.form.get(
            "state",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        deadline = request.form.get(
            "deadline",
            ""
        ).strip()

        income_limit = request.form.get(
            "income_limit",
            ""
        ).strip()

        gender = request.form.get(
            "gender",
            ""
        ).strip()

        application_link = request.form.get(
            "application_link",
            ""
        ).strip()


        new_scholarship = Scholarship(

            name=name,

            provider=provider,

            description=description,

            amount=amount,

            course=course,

            state=state,

            category=category,

            deadline=deadline,

            income_limit=income_limit,

            gender=gender,

            application_link=application_link

        )


        db.session.add(
            new_scholarship
        )

        db.session.commit()


        flash(
            "Scholarship added successfully! 🎓",
            "success"
        )


        return redirect(
            url_for("scholarships")
        )


    return render_template(
        "add_scholarship.html"
    )
@app.route("/admin")
@login_required
def admin_dashboard():

    if not current_user.is_admin:

        flash(
            "You do not have administrator access.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )


    all_scholarships = Scholarship.query.all()

    total_scholarships = Scholarship.query.count()

    total_users = User.query.count()

    total_saved = SavedScholarship.query.count()


    return render_template(
        "admin_dashboard.html",
        scholarships=all_scholarships,
        total_scholarships=total_scholarships,
        total_users=total_users,
        total_saved=total_saved
    )

@app.route(
    "/admin/edit-scholarship/<int:scholarship_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_scholarship(scholarship_id):

    if not current_user.is_admin:

        flash(
            "You do not have administrator access.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )


    scholarship = Scholarship.query.get_or_404(
        scholarship_id
    )


    if request.method == "POST":

        scholarship.name = request.form.get(
            "name",
            ""
        ).strip()

        scholarship.provider = request.form.get(
            "provider",
            ""
        ).strip()

        scholarship.description = request.form.get(
            "description",
            ""
        ).strip()

        scholarship.amount = request.form.get(
            "amount",
            ""
        ).strip()

        scholarship.course = request.form.get(
            "course",
            ""
        ).strip()

        scholarship.state = request.form.get(
            "state",
            ""
        ).strip()

        scholarship.category = request.form.get(
            "category",
            ""
        ).strip()

        scholarship.deadline = request.form.get(
            "deadline",
            ""
        ).strip()

        scholarship.income_limit = request.form.get(
            "income_limit",
            ""
        ).strip()

        scholarship.gender = request.form.get(
            "gender",
            ""
        ).strip()

        scholarship.application_link = request.form.get(
            "application_link",
            ""
        ).strip()


        db.session.commit()


        flash(
            "Scholarship updated successfully!",
            "success"
        )


        return redirect(
            url_for("admin_dashboard")
        )


    return render_template(
        "edit_scholarship.html",
        scholarship=scholarship
    )

@app.route(
    "/admin/delete-scholarship/<int:scholarship_id>"
)
@login_required
def delete_scholarship(scholarship_id):

    if not current_user.is_admin:

        flash(
            "You do not have administrator access.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )


    scholarship = Scholarship.query.get_or_404(
        scholarship_id
    )


    SavedScholarship.query.filter_by(
        scholarship_id=scholarship.id
    ).delete()


    db.session.delete(
        scholarship
    )

    db.session.commit()


    flash(
        "Scholarship deleted successfully.",
        "success"
    )


    return redirect(
        url_for("admin_dashboard")
    )
@app.route("/dashboard")
@login_required
def dashboard():

    saved_items = SavedScholarship.query.filter_by(
        user_id=current_user.id
    ).all()

    saved_scholarships = []

    for item in saved_items:

        scholarship = Scholarship.query.get(
            item.scholarship_id
        )

        if scholarship:

            saved_scholarships.append(
                scholarship
            )

    return render_template(
        "dashboard.html",
        user=current_user,
        saved_scholarships=saved_scholarships
    )

@app.route("/matches")
@login_required
def matches():

    scholarships = Scholarship.query.all()

    matched_scholarships = []


    for scholarship in scholarships:

        score, reasons = calculate_match(
            current_user,
            scholarship
        )

        matched_scholarships.append({

            "scholarship": scholarship,

            "score": score,

            "reasons": reasons

        })


    matched_scholarships.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return render_template(
        "matches.html",
        matches=matched_scholarships
    )
# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(
        url_for("home")
    )


# =========================================================
# CREATE DATABASE
# =========================================================

with app.app_context():

    db.create_all()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )

