from requests import post
import config
from firebase import db
from firebase import storage
from flask import Flask, flash, render_template
from flask_toastr import Toastr
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField, StringField, SearchField
from wtforms.validators import InputRequired, DataRequired
import uuid
import spacy

nlp = spacy.load("en_core_web_sm")
from resume_parser import resumeparse

data = None

app = Flask(__name__)
toastr = Toastr(app)
app.config["SECRET_KEY"] = config.key
app.config["UPLOAD_FOLDER"] = "static/files"


class UploadFileForm(FlaskForm):
    file = FileField(
        "File",
        validators=[
            InputRequired(message="Please select a file before uploading"),
            FileAllowed(
                ["docx", "pdf", "txt"],
                message="Please upload a .pdf, .docx, or .txt file",
            ),
        ],
    )
    submit = SubmitField("Upload Resume")


class SearchForm(FlaskForm):
    searched = StringField(
        "Searched", validators=[InputRequired(message="Please search something")]
    )
    submit = SubmitField("Submit")


@app.route("/search", methods=["POST"])
def search():
    global data
    searched = ""
    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        if searchForm.searched.data:
            searched = searchForm.searched.data
    else:
        if searchForm.searched.errors:
            flash(searchForm.searched.errors[0], "warning")
    return render_template(
        "index.html",
        form=searchForm,
        searched=searched,
        display="block",
        data=data,
    )


@app.route("/", methods=["GET", "POST"])
def index():
    display = "none"
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file_name = secure_filename(file.filename)
        id = uuid.uuid4()
        storage.child("resumes/" + file_name).put(file)
        storage.child("resumes/" + file_name).download("resumes/", file_name)
        global data
        data = resumeparse.read_file(file_name)
        for key, val in data.items():
            if isinstance(val, list):
                string = ""
                for item in val:
                    if string:
                        string += " | " + str(item)
                    else:
                        string = str(item)
                data[key] = string
            else:
                data[key] = str(val)
        db.child("resumes/" + str(id)).set(data)
        display = "block"
    else:
        if form.file.errors:
            flash(form.file.errors[0], "error")
    return render_template(
        "index.html", form=form, display=display, data=data, searched=""
    )


if __name__ == "__main__":
    app.run(debug=True)
