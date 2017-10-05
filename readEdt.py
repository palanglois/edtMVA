# -*- coding: utf-8 -*-
import csv
import time
import copy
from coursList import coursList
from sortList import *
import dateparser
from datetime import datetime
import json
import cPickle as pickle
import os

here = os.path.dirname(__file__)

def matchId(identifier):
  with open(os.path.join(here, 'static/course_combinations.json'), 'r') as comb:
    all_user_courses = json.load(comb)
    if identifier < len(all_user_courses):
      user_courses = all_user_courses[identifier]
    else:
      return [], False
  all_courses = pickle.load(open(os.path.join(here, "static/parsedEdt.pkl"), "rb"))
  kept_courses = []
  for course in all_courses:
    for my_course in user_courses:
      if my_course.decode('utf-8') in course['title'].lower():
        kept_courses.append(course)
        break
  return kept_courses, True

