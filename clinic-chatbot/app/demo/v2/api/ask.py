# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g
import os
from .wit import ask_wit
from . import Resource
from .. import schemas
from rivescript import RiveScript

username = 'Felix'
bot = RiveScript()
bot.load_directory(
    os.path.join(os.path.dirname(__file__), ".", "brain")
)
bot.sort_replies()


class Ask(Resource):

    def get(self):
        msg = g.args.get("expression")
        print('You> %s' % msg)
        answer = bot.reply(username, msg)
        if "ERR" in answer:
            answer = ask_wit(msg)
        print('Bot>', answer)
        return {'answer': answer}, 200, None