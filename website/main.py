from flask import Flask, render_template, url_for, redirect, session, request

NAME_KEY = "name"

app = Flask(__name__)
app.secret_key = "hello"

@app.route("/login")
def login():
    if request.method == "POST":
        session[NAME_KEY] = request.form["inputName"]
        return redirect(url_for("home"))

    return render_template("login.html", {"session":"session"})


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/")
@app.route("/home")
def home():
    #if NAME_KEY not in session:
    #    return redirect(url_for("home"))
    #name = session[NAME_KEY]
    return render_template("index.html", {"login":True, "session": session})

if __name__ == "__main__":
    app.run(debug = True)