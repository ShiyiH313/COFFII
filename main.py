from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location (URL)', validators=[URL()])
    open_time = StringField('Opening time e.g. 10:30AM', validators=[DataRequired()])
    close_time = StringField('Closing time e.g. 5PM', validators=[DataRequired()])
    coffee = SelectField('Coffee quality', choices=["💢", "💢💢", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"], validators=[DataRequired()])
    wifi = SelectField('WiFi reliability', choices=['💢', '💢💢', '🟢🟢🟢', '✅✅✅✅', '✅✅✅✅✅'], validators=[DataRequired()])
    socket = SelectField('socket availability', choices=['💢', '💢💢', '⌛️⌛️⌛️', '💡💡💡💡', '💡💡💡💡💡'], validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        with open('cafe-data.csv', 'a', newline='') as file:

            cafe = form.cafe.data
            location = form.location.data
            open_time = form.open_time.data
            close_time = form.close_time.data
            coffee = form.coffee.data
            wifi = form.wifi.data
            socket = form.socket.data
            file.write(f"\n{cafe}, {location}, {open_time}, {close_time}, {coffee}, {wifi}, {socket}")


            return redirect(url_for("cafes"))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
