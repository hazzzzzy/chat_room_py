from flask_wtf import FlaskForm


class baseForm(FlaskForm):
    class Meta:
        csrf = False
