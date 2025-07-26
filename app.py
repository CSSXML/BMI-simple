from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # 請更改為一組強密鑰

class BMIForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(min=3)])
    height = FloatField('身高 (公分)', validators=[DataRequired(), NumberRange(min=50, max=250)])
    weight = FloatField('體重 (公斤)', validators=[DataRequired(), NumberRange(min=20, max=300)])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = BMIForm()
    bmi = None
    category = None
    if form.validate_on_submit():
        name = form.name.data
        height = form.height.data / 100  # 公分轉公尺
        weight = form.weight.data
        bmi = round(weight / (height ** 2), 2)

        # BMI分類邏輯
        if bmi < 18.5:
            category = '體重過輕'
        elif 18.5 <= bmi < 24:
            category = '正常'
        elif 24 <= bmi < 27:
            category = '過重'
        else:
            category = '肥胖'
        return render_template('index.html', form=form, bmi=bmi, category=category, name=name)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, port=80)
