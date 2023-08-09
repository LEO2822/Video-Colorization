from flask import Flask, render_template, request
from test import process

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/colorize", methods=["GET", "POST"])
def colorize():
    if request.method == "POST":
        file = request.files.get("videoFileInput")
        if file:
            file_path = "./input/" + file.filename
            file.save(file_path)
            print("Video file saved at:", file_path)

            print("Video processed successfully")
            out_file_path = process(file_path)

            return out_file_path  # Return the out_file_path as the response

    return render_template("colorize.html")




if __name__ == "__main__":
    app.run(debug=True, port=8000)
