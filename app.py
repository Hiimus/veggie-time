import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
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
@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    recipe = list(mongo.db.recipes.find())
    return render_template(
        "recipes.html", recipes=recipes, recipe=recipe)


@app.route("/all_recipes")
def all_recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("all_recipes.html", recipes=recipes)


@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("view_recipe.html", recipe=recipe)


# Credit to Flask Task Manager Mini-Project videos
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("recipes.html", recipes=recipes)


# Credit to Flask Task Manager Mini-Project videos
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
@app.route("/login", methods=["GET", "POST"])
def login():
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


@app.route("/profile/<username>")
def profile(username):
    # uses the session user's username from database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    recipes = list(mongo.db.recipes.find({"liked_by": session["user"]}))
    if session["user"]:
        return render_template("profile.html", username=username, recipes=recipes)
    else:
        return redirect(url_for("login"))


@app.route("/profile/<username>/<recipe_id>", methods=["GET", "POST"])
def add_favorite(username, recipe_id):
    # uses the session user's username from database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
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
    if request.method == "POST":
        mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        recipes = list(mongo.db.recipes.find({"liked_by": session["user"]}))
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)}, {"$push": {"liked_by": session["user"]}})
    if session["user"]:
        return render_template("profile.html", username=username, recipe=recipe, recipes=recipes)
    else:
        return redirect(url_for("login"))


@app.route("/remove_favorite/<recipe_id>", methods=["GET", "POST"])
def remove_favorite(recipe_id):
    mongo.db.recipes.update_one(
        {"_id": ObjectId(recipe_id)}, {"$pull": {"liked_by": session["user"]}})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("get_recipes"))


# Credit to Flask Task Manager Mini-Project videos
@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have successfully logget out")
    session.pop("user")
    return redirect(url_for("login"))


# Credit to Flask Task Manager Mini-Project videos
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
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
        return redirect(url_for("get_recipes"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    difficulties = mongo.db.difficulties.find()
    return render_template(
        "add_recipes.html", categories=categories, difficulties=difficulties)


# Credit to Flask Task Manager Mini-Project videos
@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
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
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("get_recipes"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
