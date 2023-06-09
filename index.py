import config
from firebase import db
from flask import Flask, flash, render_template
from flask_toastr import Toastr
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired


app = Flask(__name__)
toastr = Toastr(app)
app.config["SECRET_KEY"] = config.key
app.config["UPLOAD_FOLDER"] = "static/files"


class UploadFileForm(FlaskForm):
    file = FileField(
        "File",
        validators=[
            InputRequired(message="test"),
            FileAllowed(["docx", "pdf"], message="Please upload a .docx or .pdf file"),
        ],
    )
    submit = SubmitField("Upload Resume")


@app.route("/", methods=["GET", "POST"])
def hello():
    status = "Waiting for resume..."
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        # Save file to ./static/files
        """
        file.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                secure_filename(file.filename),
            )
        )
        """
        # Dictionary 'data' will be parsed resume information
        data = {"attribute": "dummy_data"}
        db.child("Resumes").set(data)
        status = "Resume uploaded"
    else:
        if form.file.errors:
            flash(form.file.errors[0], "error")
    return render_template("index.html", form=form, status=status)


if __name__ == "__main__":
    app.run(debug=True)
