# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
# import pdb

import csv


# Get available timeslots for each dentist
# Reserve/cancel timeslot
class Timeslot(Resource):
    def get(self):
        dentist = g.args.get('dentist')
        a = []
        with open('timeslots.csv', mode='r') as csvFile:
            csv_reader = csv.DictReader(csvFile)
            lines = [l for l in csv_reader]
            for i in lines:
                if i['dentist'] == dentist and i['status'] == 'available':
                    a.append(i)
            print(a)
        return a, 200, None

    def patch(self):
        # pdb.set_trace()
        # print(request.data)
        dentist = g.args.get('dentist')
        # print(dentist)
        time = g.args.get('time')
        # with open('timeslots.csv', mode='r') as csvFile:
        #     csv_reader = csv.DictReader(csvFile)
        #     # print(0)
        #     r = [l for l in csv_reader]
        r = csv.reader(open('timeslots.csv'))
        lines = [l for l in r]
        a = {}
        for i in lines:
            if i[1] == dentist and int(i[2]) == time:
                if i[4] == 'available':
                    i[4] = 'unavailable'
                elif i[4] == 'unavailable':
                    i[4] = 'available'
                print(i)
                a = i
                break
        writer = csv.writer(open('timeslots.csv', 'w'))
        writer.writerows(lines)
        return a, 200, None
