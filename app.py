import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Credit to Flask Task Manager Mini-Project videos
# Default home page
@app.route("/")
@app.route("/home")
def home():
    recipes = list(mongo.db.recipes.find().limit(6).sort("_id", -1))
    recipe = list(mongo.db.recipes.find())
    return render_template(
        "home.html", recipes=recipes, recipe=recipe)


# Credit to https://gist.github.com/mozillazg/69fb40067ae6d80386e10e105e6803c9
# for pagination.

users = list(range(100))


def get_users(offset=0, per_page=10):
    return users[offset: offset + per_page]


@app.route("/all_recipes")
def all_recipes():
    page, per_page, offset = get_page_args(
        page_parameter='page',
        per_page_parameter='per_page',
        offset_parameter='offset')
    per_page = 9
    offset = (page - 1) * per_page
    total = mongo.db.recipes.find().count()
    recipes = list(mongo.db.recipes.find().sort("_id", -1))
    recipes_paginated = recipes[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='materializecss')
    return render_template(
        "all_recipes.html", recipes=recipes_paginated, page=page,
        per_page=per_page, pagination=pagination)


# Function for when clicking a recipe card.
@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("view_recipe.html", recipe=recipe)


# Credit to Flask Task Manager Mini-Project videos
# Search function with pagination
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    page, per_page, offset = get_page_args(
        page_parameter='page',
        per_page_parameter='per_page',
        offset_parameter='offset')
    per_page = 9
    offset = (page - 1) * per_page
    total = mongo.db.recipes.find().count()
    recipes_page = list(mongo.db.recipes.find())
    recipes_paginated = recipes_page[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='materializecss')
    return render_template(
        "search.html", recipes=recipes,
        recipes_page=recipes_paginated, page=page,
        per_page=per_page, pagination=pagination)


# Sort category function, from home page.
@app.route("/sort_category_home", methods=["GET", "POST"])
def sort_category_home():
    category = request.args.get("category_name")
    recipes = list(
                mongo.db.recipes.find(
                    {"category_name": category}))
    flash(category)
    return render_template("home.html", recipes=recipes, category=category)


# Sort category function, from all recipes page.
@app.route("/sort_category_all", methods=["GET", "POST"])
def sort_category_all():
    page, per_page, offset = get_page_args(
        page_parameter='page',
        per_page_parameter='per_page',
        offset_parameter='offset')
    per_page = 9
    offset = (page - 1) * per_page
    total = mongo.db.recipes.find().count()
    recipes_page = list(mongo.db.recipes.find().sort("_id", -1))
    recipes_paginated = recipes_page[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='materializecss')
    category = request.args.get("category_name")
    recipes = list(
                mongo.db.recipes.find(
                    {"category_name": category}))
    flash(category)
    return render_template("search.html", recipes=recipes,
                           category=category, recipes_page=recipes_paginated,
                           page=page, per_page=per_page, pagination=pagination)


# Credit to Flask Task Manager Mini-Project videos
# Register function for register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)
        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


# Credit to Flask Task Manager Mini-Project videos
# Login function for login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return render_template("errors/403.html")
    if request.method == "POST":
        # checks if username exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                        request.form.get("username")))
                return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # password does not match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


# Partly credited to Flask Task Manager Mini-Project videos
# Profile function for my profile page
@app.route("/profile/<username>")
def profile(username):
    # uses the session user's username from database
    # check if a user is logged in
    # Only users can acces profile
    if not session.get("user"):
        return render_template("errors/403.html")
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        recipes = list(
            mongo.db.recipes.find(
                {"liked_by": session["user"]}).sort("_id", -1))
        real_recipes = list(
            mongo.db.recipes.find(
                {"created_by": session["user"]}).sort("_id", -1))
        created_recipes = mongo.db.recipes.find_one(
            {"created_by": session["user"]},
            {"created_by": 1, "_id": 0})
        return render_template(
            "profile.html", username=username, recipes=recipes,
            created_recipes=created_recipes, real_recipes=real_recipes)


# Login to like function, sends user to login page if user tries to
# like a recipe without being logged in
@app.route("/login")
def login_to_like():
    if not session["user"]:
        flash("Please log in in order to like recipes")
        return render_template("login.html")


# Adds to favorites, redirects to profile page if added while on profile
# page or view_recipe page.
@app.route("/profile/<username>/<recipe_id>", methods=["GET", "POST"])
def add_favorite_from_profile(username, recipe_id):
    if request.method == "POST":
        mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)},
            {"$push": {"liked_by": session["user"]}})
    if session["user"]:
        flash("Recipe Successfully Added to Favorites")
        return redirect(url_for('profile', username=session['user']))


# Adds to favorites, redirects to all_recipes page if added while
# on all_recipes page.
@app.route("/all_recipes/<username>/<recipe_id>", methods=["GET", "POST"])
def add_favorite_from_all(username, recipe_id):
    if request.method == "POST":
        mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)},
            {"$push": {"liked_by": session["user"]}})
    if session["user"]:
        flash("Recipe Successfully Added to Favorites")
        return redirect(url_for('all_recipes', username=session['user']))


# Adds to favorites, redirects to home page if added while on home page.
@app.route("/<username>/<recipe_id>", methods=["GET", "POST"])
def add_favorite_from_home(username, recipe_id):
    if request.method == "POST":
        mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)},
            {"$push": {"liked_by": session["user"]}})
    if session["user"]:
        flash("Recipe Successfully Added to Favorites")
        return redirect(url_for('home', username=session['user']))


# Removes favorite, redirects to profile page if removing while
# on profile page or view_recipe page.
@app.route("/profile/<recipe_id>", methods=["GET", "POST"])
def remove_favorite_from_profile(recipe_id):
    if request.method == "POST":
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)},
            {"$pull": {"liked_by": session["user"]}})
        flash("Recipe Successfully Removed From Favorites")
        return redirect(url_for('profile', username=session['user']))


# Removes favorite, redirects to home page if removing while on home page.
@app.route("/get_recipes/<recipe_id>", methods=["GET", "POST"])
def remove_favorite_from_home(recipe_id):
    if request.method == "POST":
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)},
            {"$pull": {"liked_by": session["user"]}})
        flash("Recipe Successfully Removed From Favorites")
        return redirect(url_for('home', username=session['user']))


# Removes favorite, redirects to home page if removing while on home page.
@app.route("/all_recipes/<recipe_id>", methods=["GET", "POST"])
def remove_favorite_from_all(recipe_id):
    if request.method == "POST":
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)},
            {"$pull": {"liked_by": session["user"]}})
        flash("Recipe Successfully Removed From Favorites")
        return redirect(url_for('all_recipes', username=session['user']))


# Credit to Flask Task Manager Mini-Project videos
@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have successfully logget out")
    session.pop("user")
    return redirect(url_for("login"))


# Credit to Flask Task Manager Mini-Project videos
# Adding a recipe function
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if not session.get("user"):
        return render_template("errors/403.html")

    if request.method == "POST":
        recipe = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_img": request.form.get("recipe_img"),
            "recipe_description": request.form.get("recipe_description"),
            "difficulty_name": request.form.get("difficulty_name"),
            "ingredients": request.form.getlist("ingredients"),
            "instructions": request.form.getlist("instructions"),
            "created_by": session["user"],
            "liked_by": request.form.getlist("")
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added")
        return redirect(url_for("home"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    difficulties = mongo.db.difficulties.find()
    return render_template(
        "add_recipes.html", categories=categories, difficulties=difficulties)


# Credit to Flask Task Manager Mini-Project videos
# editing a recipe function
@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    find_author = mongo.db.recipes.find_one(
        {"_id": ObjectId(recipe_id)},
        {"created_by": 1, "_id": 0})
    created_by = find_author.get("created_by")
    if session.get("user") != created_by:
        return render_template("errors/403.html")

    if request.method == "POST":
        submit_recipe = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_img": request.form.get("recipe_img"),
            "recipe_description": request.form.get("recipe_description"),
            "difficulty_name": request.form.get("difficulty_name"),
            "ingredients": request.form.getlist("ingredients"),
            "instructions": request.form.getlist("instructions"),
            "created_by": session["user"],
            "liked_by": request.form.getlist("")
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit_recipe)
        flash("Recipe Successfully Updated")

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    difficulties = mongo.db.difficulties.find()
    return render_template(
        "edit_recipes.html", recipe=recipe,
        categories=categories, difficulties=difficulties)


# Credit to Flask Task Manager Mini-Project videos
# Deleting a recipe function
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    find_author = mongo.db.recipes.find_one(
        {"_id": ObjectId(recipe_id)},
        {"created_by": 1, "_id": 0})
    created_by = find_author.get("created_by")
    if session.get("user") != created_by:
        return render_template("errors/403.html")

    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("home"))


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")))
