# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas

import csv


# available dentist
class Dentist(Resource):

    def get(self):
        with open('dentists.csv', mode='r') as csvFile:
            csv_reader = csv.DictReader(csvFile)
            r = [l for l in csv_reader]
            print(r)
        return r, 200, None