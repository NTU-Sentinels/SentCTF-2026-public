
from flask import Flask, render_template, request
import json
import subprocess

app = Flask(__name__)

# Home Page
@app.route("/")
def index():
    return render_template("index.html", menu=None)

# Read Menu File
@app.route("/menu", methods=["POST"])
def menu():
    category = request.form.get("category", "")
    
    try:

        if "cat" in category or "secret" in category:
            return render_template("404.html", error='"cat" or "secret" string detected in input! Command not executed.')

        command=f"cat menu/{category}.json"

        result = subprocess.run(command,shell=True,capture_output=True,text=True,timeout=5)
            
        # Display menu
        menu = json.loads(result.stdout)['items']
        return render_template("index.html",
            menu=menu,
            selected_category=category
            )

    except:
        return render_template("404.html", error=result.stderr+result.stdout)
        

    

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)

