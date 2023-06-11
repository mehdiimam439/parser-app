from uuid import uuid4

import spacy
from flask import Flask, flash, render_template
from flask_toastr import Toastr
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from resume_parser import resumeparse
from werkzeug.utils import secure_filename
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import InputRequired

from firebase import db, storage


nlp = spacy.load("en_core_web_sm")

data = None

app = Flask(__name__)
toastr = Toastr(app)
app.config["SECRET_KEY"] = "secret_key"


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
        id = uuid4()
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
