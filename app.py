from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
import os
from automation_runner import main as run_script

app = Flask(__name__)

app.config["STATIC_FOLDER"] = "static"
app.config["CSV_FOLDER"] = "csv"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["RESULT_FOLDER"] = "results"
app.config["ALLOWED_EXTENSIONS"] = {"mp4"}

app.secret_key = os.urandom(24)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


first_access = True


@app.route("/")
def index():
    global first_access

    if first_access:
        csv_files = os.listdir(app.config["CSV_FOLDER"])
        upload_files = os.listdir(app.config["UPLOAD_FOLDER"])
        result_files = os.listdir(app.config["RESULT_FOLDER"])

        for csv_file in csv_files:
            file_path = os.path.join(app.config["CSV_FOLDER"], csv_file)
            os.remove(file_path)

        for upload_file in upload_files:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], upload_file)
            os.remove(file_path)

        for result_file in result_files:
            file_path = os.path.join(app.config["RESULT_FOLDER"], result_file)
            os.remove(file_path)
        first_access = False

    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file.filename = "upload.mp4"

            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            run_script()
            flash("🎉 Proses deteksi selesai! Hasil deteksi dapat diunduh sekarang.", "success")
            return redirect(url_for("index", _anchor="result"))

    return redirect(request.url)


@app.route("/download")
def download_file():
    result_file = "result.csv"
    result_file_path = os.path.join(app.config["RESULT_FOLDER"], result_file)

    if os.path.exists(result_file_path):
        return send_from_directory(app.config["RESULT_FOLDER"], result_file, as_attachment=True)
    else:
        flash("📂 Nampaknya belum ada file CSV yang bisa diunduh. Selesaikan proses deteksi terlebih dahulu.", "error")
        return redirect(url_for("index", _anchor="detection"))


@app.route("/css/<path:filename>")
def send_css(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/font/<path:filename>")
def send_font(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/img/<path:filename>")
def send_img(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/js/<path:filename>")
def send_js(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/results/<path:filename>")
def send_results(filename):
    return send_from_directory(app.config["RESULT_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
