# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas

import csv


# dentists info
class DentistName(Resource):

    def get(self, name):
        a = []
        with open('dentists.csv', mode='r') as csvFile:
            csv_reader = csv.DictReader(csvFile)
            r = [l for l in csv_reader]
            for i in r:
                if i['name'] == name:
                    print(i)
                    a.append(i)
        return a, 200, None