from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from client import Client
from threading import Thread
import time

NAME_KEY = "name"
client = None
message = []

app = Flask(__name__)
app.secret_key = "hello"


def disconnect():
    """
    call this for disconnecting client
    """
    global client
    if client:
        client.disconnect()


@app.route("/login")
def login():
    """
    display main login page
    """
    disconnect()
    if request.method == "POST":
        session[NAME_KEY] = request.form["inputName"]
        return redirect(url_for("home"))

    return render_template("login.html", {"session":"session"})


@app.route("/logout")
def logout():
    """
    log out by popping name from session
    """
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/")
@app.route("/home")
def home():
    global client

    if NAME_KEY not in session:
        return redirect(url_for("home"))

    client = Client(session[NAME_KEY])
    return render_template("index.html", {"login":True, "session": session})


@app.route("/run/", methods = ["GET"])
def send_message(url=None):
    """
    called from JQuery to send message"""
    global client

    msg = request.args.get("val")
    if "client" != None:
        client.send_message(msg)
    
    return "none"


@app.route("/get_messages")
def get_messages():
    return jsonify({"messages": messages})
    

def update_message():
    """
    updates the local list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)  # update every 1/10 of a second
        if not client: continue
        new_messages = client.get_messages()  # get any new messages from client
        msgs.extend(new_messages)  # add to local list of messages

        for msg in new_messages:  # display new messages
            if msg == "{quit}":
                run = False
                break




if __name__ == "__main__":
    app.run(debug = True)
    Thread(target = update_message).start()