from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home(): 
    return render_template("index.html")

@app.route("/about")
def about(): 
    return "<h1>About the project</h1><p>Just trying to learn new things >:D </p>"

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", username=name)

if __name__ == "__main__":
    app.run(debug=True)