from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserRegisterForm, UserLoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///user_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secret-secret-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
toolbar = DebugToolbarExtension(app)

@app.route("/") 
def home_page():
    return redirect("/register")

@app.route("/register", methods=["GET","POST"])
def show_register_form():

    form = UserRegisterForm()

    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data
        email = form.email.data 
        first_name = form.first_name.data 
        last_name = form.last_name.data 

        new_user = User.register(username,password,email,first_name,last_name)

        db.session.add(new_user)

        try:
            db.session.commit()
            session["username"] = new_user.username
            flash("Registered successfully! Welcome!")
            return redirect(f"/users/{new_user.username}")
        except IntegrityError:
            form.username.errors.append("Username taken. Please pick a different one")
            return render_template("register.html", form=form)
        
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET","POST"])
def show_login_form():
    form = UserLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)
        if user:
            flash(f"Welcome Back, {user.username}!")
            session["username"] = user.username 
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password"]
    return render_template("login.html", form=form)            

@app.route("/logout")
def logout_user():
         session.pop("username")
         flash("Logged out!")
         return redirect("/")

@app.route("/users/<username>")
def show_secret(username):
    if "username" not in session:
        flash("Please login or register first!")
        return redirect("/")
    
    if username != session["username"]:
        flash("You do not have access there")
        return redirect(f"/users/{session['username']}")

    user = User.query.get_or_404(username)
    feedback = user.feedback 
    return render_template("user.html", user=user, feedback=feedback)   

@app.route("/users/<username>/delete", methods=["GET","POST"])
def delete_user(username):
    if "username" not in session:
        flash("Please login or register first!")
        return redirect("/")
    user = User.query.get_or_404(username)
    if user.username == session["username"]:
        db.session.delete(user)
        db.session.commit()
        session.pop("username")
        flash("User deleted!")
        return redirect("/")
    else:
        flash("You dont have permission to do that!")   
        return redirect(f"/users/{session['username']}")    
        

@app.route("/users/<username>/feedback/add", methods=["GET","POST"])
def show_feedback_form(username):
    if "username" not in session:
        flash("Please login first!")
        return redirect("/")

    if username != session["username"]:
        flash("You do not have access here")
        return redirect(f"/users/{session['username']}")

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data 
        content = form.content.data 
        new_feedback = Feedback(title=title, content=content, username=session["username"])
        db.session.add(new_feedback)
        db.session.commit()
        flash("Feedback submitted!")
        return redirect(f"/users/{username}")

    return render_template("feedback.html", form=form) 

@app.route("/feedback/<int:feedback_id>/update", methods=["GET","POST"])
def update_feedback(feedback_id):
    if "username" not in session:
        flash("Please login first!")
        return redirect("/")

    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.username

    if user != session["username"]:
        flash("You do not have access here")
        return redirect(f"/users/{session['username']}")

    form = FeedbackForm()
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash("Feedback has been updated")
        return redirect(f"/users/{user}")

    return render_template("update_feedback.html",form=form, feedback=feedback)  

@app.route("/feedback/<int:feedback_id>/delete", methods=["GET","POST"])
def delete_feedback(feedback_id):
    if "username" not in session:
        flash("Please login first!")
        return redirect("/")

    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.username

    if user != session["username"]:
        flash("You do not have access here")
        return redirect(f"/users/{session['username']}")

    db.session.delete(feedback) 
    db.session.commit()
    flash("Feedback deleted!")
    return redirect(f"/users/{user}")   



