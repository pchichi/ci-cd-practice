from flask import Flask, request, redirect

app = Flask(__name__)

@app.route("/")
def login():
    return """
    <form action="/login" method="post">
        <input name="id" />
        <input name="pw" />
        <button type="submit">Login</button>
    </form>
    """

@app.route("/login", methods=["POST"])
def do_login():
    if request.form["id"] == "admin" and request.form["pw"] == "1234":
        return redirect("/dashboard")
    return "fail"

@app.route("/dashboard")
def dashboard():
    return "DASHBOARD PAGE"

if __name__ == "__main__":
    app.run(debug=True)