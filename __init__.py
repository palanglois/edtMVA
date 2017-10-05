# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, render_template, send_from_directory, request
from flask_wtf import FlaskForm, widgets
from flask_wtf.csrf import CSRFProtect
from flask_appbuilder.widgets import ListWidget
from wtforms.fields import SelectMultipleField
from wtforms.widgets import CheckboxInput
import os
import csv
import sys
import json
import datetime
from readEdt import matchId
from coursList import coursList

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = 's3cr3t'
here = os.path.dirname(__file__)


class MultiCheckboxField(SelectMultipleField):
  widget = ListWidget(prefix_label=False)
  option_widget = CheckboxInput()

class SimpleForm(FlaskForm):
  all_courses = [(k.decode('utf-8'), v.decode('utf-8')) for k, v in coursList.items()]
  my_field = MultiCheckboxField('Cours choisis', choices=all_courses)

@app.route("/", methods=["GET"])
@csrf.exempt
def createCourses():
    my_form = SimpleForm()
    return(render_template('course_creator.html', form=my_form))

@app.route("/", methods=["POST"])
@csrf.exempt
def createCoursesPost():
  my_form = SimpleForm()
  # Check that the user has filled something
  if my_form.my_field.data is None: 
    return(render_template('tes_con.html'))
  # Load the users course combination choices
  data = None
  course_comb_path = os.path.join(here, 'static/course_combinations.json')
  if not os.path.isfile(course_comb_path):
    data = []
  else:
    with open(course_comb_path, 'r') as comb:
      data = json.load(comb)
  # Add the new choice
  with open(course_comb_path, 'w') as comb:
    data.append(my_form.my_field.data)
    json.dump(data, comb)
  # Generate the user URL
  comb_number = str(len(data)-1).zfill(6)
  url = 'http://lucienetleon.hopto.org/pa?id=' + comb_number
  return(render_template('page_url.html', url=url, comb_number=comb_number))

@app.route("/edt")
def paEdt():
  identifier = request.args.get('id')
  my_form = SimpleForm()
  data, correct = matchId(int(identifier))
  if not correct:
    return(render_template('wrong_id.html'))
  edt_path = os.path.join(here, 'static/edt.csv')
  last_update_time = datetime.datetime.fromtimestamp(os.path.getmtime(edt_path)).strftime("%Y-%m-%d %H:%M:%S")
  return(render_template('edt.html', **{'listCours' : data, 'last_time' : last_update_time}))

@app.route("/robots.txt")
def robots():
  robotsListString = open('/var/www/myServ/robots.txt','r').readlines()
  robotsString = "<br>".join(robotsListString)
  return(send_from_directory('/var/www/myServ','robots.txt'))

if __name__ == "__main__":
  app.run(debug=True)
