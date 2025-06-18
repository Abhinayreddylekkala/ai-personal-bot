from flask import Flask, render_template, request, jsonify
from assistant import handle_command

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    command = data.get("command", "")
    response = handle_command(command.lower())
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
