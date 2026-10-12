import os
import secrets

from flask import Flask, abort, jsonify, render_template, request, send_file, session


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_ARCHIVE_DIR = os.path.join(BASE_DIR, "challenge_files", "public")
ARCHIVE_EXPORTS = [
    "hall_confessions.txt",
    "campus_rider_complaints.txt",
    "group_project_venting.txt",
    "moderator_handover.txt",
]

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", secrets.token_urlsafe(48)),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

PUBLIC_POSTS = [
    ("Anonymous #4821", "i hate my cc0067 groupmates, i am tanking everything sia"),
    ("Anonymous #1957", "Who dressed up in a maid costume at west spine yesterday???"),
    ("Anonymous #6103", "My roomate keeps leaving his underwear on the floor brah"),
    ("Anonymous #3370", "I just went to 3 different printers across campus and somehow EVERYONE decideds to print their notes today"),
    ("Anonymous #7284", "I secretely love class part, but no one gets me.. i love yapping sm"),
    ("Anonymous #4040", "Can I dabao a mod 2 weeks in?"),
    ("Anonymous #2126", "I am in love with my prof, sometimes i rewatch lectures just to hear him talk <3"),
    ("Anonymous #8991", "Someone has left a laptop, water bottle and jacket in the library for 7 hours. Is the table legally theirs now?"),
]

REPORTS = [
    {
        "id": "confession-1204",
        "body": "Someone microwaved fish in the pantry again.",
        "reports": 19,
    },
    {
        "id": "confession-3488",
        "body": "The Campus Rider app said the bus was arriving. The bus disagreed.",
        "reports": 7,
    },
    {
        "id": "confession-5012",
        "body": "My group project meeting could have been a message. The message could also have been ignored.",
        "reports": 12,
    },
]

RESTRICTED_CONFESSION = {
    "id": "confession-6701",
    "visibility": "Senior Moderators Only",
    "status": "Removed",
    "body": "I have a confession.\n\nThe North Spine tables are not occupied. The laptops have gained consciousness and are reserving the seats themselves.",
    "flag": "sentctf{c0nf35510n_r3qu35t_1nt3rc3pt3d}",
}


def logged_in():
    return session.get("moderator") == "sleepy.mod"


@app.get("/")
def home():
    return render_template("home.html", posts=PUBLIC_POSTS)


@app.get("/robots.txt")
def robots():
    return app.response_class(
        "User-agent: *\nDisallow: /moderator-preview/\nDisallow: /confession-archive/\n",
        mimetype="text/plain",
    )


@app.get("/moderator-preview/")
def moderator_preview():
    return render_template("moderator_preview.html")


@app.get("/confession-archive/")
def archive():
    return render_template(
        "archive.html",
        exports=ARCHIVE_EXPORTS,
    )


@app.get("/confession-archive/download")
def download_archive():
    filename = request.args.get("file", "")
    if not filename:
        abort(400, "Missing file parameter.")

    if filename not in ARCHIVE_EXPORTS:
        abort(404, "Archive export not found.")
    requested_file = os.path.join(PUBLIC_ARCHIVE_DIR, filename)
    if not os.path.isfile(requested_file):
        abort(404, "Archive export not found.")
    return send_file(requested_file, as_attachment=False, download_name=os.path.basename(filename))


@app.route("/moderator-login", methods=["GET", "POST"])
def moderator_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == "sleepy.mod" and password == "OneMoreDeadline!":
            session["moderator"] = username
            return render_template("login_success.html", username=username)
        error = "Login failed. Maybe check whether Caps Lock is expressing itself."
    return render_template("login.html", error=error)


@app.get("/moderator-dashboard")
def moderator_dashboard():
    if not logged_in():
        return render_template("login.html", error="Please sign in to access the moderation dashboard."), 401
    return render_template("dashboard.html", reports=REPORTS)


@app.post("/api/confession/view")
def view_confession():
    if not logged_in():
        return jsonify({"error": "Moderator session required."}), 401

    payload = request.get_json(silent=True) or {}
    confession_id = payload.get("confession_id", "")
    visibility = payload.get("visibility", "")

    # Deliberately vulnerable for this CTF challenge: the API trusts the request's
    # confession ID and visibility fields instead of enforcing the moderator role.
    if confession_id == RESTRICTED_CONFESSION["id"] and visibility == "moderator-only":
        return jsonify(RESTRICTED_CONFESSION)

    for report in REPORTS:
        if report["id"] == confession_id and visibility == "public":
            return jsonify(
                {
                    "id": report["id"],
                    "visibility": "Public",
                    "status": "Open",
                    "body": report["body"],
                    "reports": report["reports"],
                }
            )

    return jsonify({"error": "Confession unavailable at this visibility level."}), 404


@app.get("/logout")
def logout():
    session.clear()
    return render_template("login.html", notice="You have been signed out.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
