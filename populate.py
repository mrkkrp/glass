#!/usr/bin/env python
#
# Script to populate data base of Glass project for testing
#
# Copyright © 2015 Mark Karpov <markkarpov@openmailbox.org>
#
# Glass is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Glass is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

import argparse
import os
import random
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glass_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from glass.models               import Tag, Topic, Message

version = '0.1.0'
description = 'Populate data base of the Glass project'
license = """populate.py — Populate data base of the Glass project

Copyright © 2015 Mark Karpov

populate.py is part of Glass project

Glass is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

Glass is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
"""

parser = argparse.ArgumentParser(description=description)
parser.add_argument('-u', '--users', metavar='N', dest='users', default=0,
                    type=int, help="how many users to create")
parser.add_argument('-g', '--tags', metavar='N', dest='tags', default=0,
                    type=int, help="how many tags to create")
parser.add_argument('-t', '--topics', metavar='N', dest='topics', default=0,
                    type=int, help="how many topics to create")
parser.add_argument('-m', '--messages', metavar='N', dest='messages', default=0,
                    type=int, help="how many messages to create")
parser.add_argument('--license', action='store_true', dest='show_license',
                    help="show program's license and exit")
parser.add_argument('--version', action='version',
                    version='%(prog)s ' + version)

class Generator():
    """
    Little auxiliary class implementing logic for generation of objects.
    """

    def __init__(self, model, p_field, p_field_gen, object_gen):
        self.model = model
        self.p_field     = p_field
        self.p_field_gen = p_field_gen
        self.object_gen  = object_gen

    def generate(self, count):
        added_total = 0
        i = self.model.objects.count()
        while added_total < count:
            j = i if self.p_field == 'id' else str(i)
            p_field = self.p_field_gen() + j
            if not self.model.objects.filter(**{self.p_field: p_field}):
                obj = self.object_gen(p_field)
                obj.save()
                added_total += 1
            i += 1

def random_object(model):
    """
    Return one of existing objects of ‘model’ class. This should be pretty
    efficient.
    """
    total = model.objects.count()
    return model.objects.all()[random.randint(0, total - 1)]

def random_objects(model, count_min, count_max):
    """
    Return list of objects of ‘model’ class. Result list will contain from
    ‘count_min’ to ‘count_max’ objects. However, if there are not enough
    objects in existance, the list may be shorter.

    I expect this to be inefficient when there are lots of objects of that
    type. Don't use this for anything serious.
    """
    objects = list(model.objects.all())
    total   = model.objects.count()
    count_min = min(count_min, total)
    count_max = min(count_max, total)
    random.shuffle(objects) # ← this may perform quite poorly
    return objects[0:random.randint(count_min, count_max)]

def populate_users(count):
    """
    Create ‘count’ new users in database. Names of users are unique, they
    are combination of human-readable string and a number. First name and
    last name are omitted and email is always “foo@example.org”.
    """
    USER_NAMES = ['nina','rick','dick','brown','mary','anna','antonio','boba',
                  'michael','rosa','alex','bruno','alfred','nikolay','ivan',
                  'mark','elvis','joseph','ricardo','eleniovey']

    def gen_user(username):
        user = User.objects.create_user(username, 'foo@example.org', 'user')
        user.first_name = re.match(r"(\D+)", username).group(1).capitalize()
        user.last_name = 'Smith'
        return user

    gen = Generator(model=User, p_field='username', object_gen=gen_user,
                    p_field_gen=(lambda: random.choice(USER_NAMES)))
    gen.generate(count)

def populate_tags(count):
    """
    Create ‘count’ new tags in database. Names of tags are unique, they are
    combination of human-readable string and a number.
    """
    TAGS = ['news','music','politics','nonsense','hacking','fucking',
            'racking','health','in-pictures']

    def gen_tag(name):
        tag = Tag(name=name)
        return tag

    gen = Generator(model=Tag, p_field='name', object_gen=gen_tag,
                    p_field_gen=(lambda: random.choice(TAGS)))
    gen.generate(count)

def populate_topics(count):
    """
    Create ‘count’ new topics in database. Titles of topics are unique, they
    are combination of human-readable string and a number. Every topic has
    associated collection of tags.
    """
    TOPIC_TITLES = ["Life on Mars?",
                    "Disaster in South Africa",
                    "Evil flute player kills a cat",
                    "Evangelism as way of life",
                    "Radiation can give you new feelings",
                    "Learn a Haskell and make a basket",
                    "Unbelievable power of rats",
                    "Infection in South Africa",
                    "Love cannot bear",
                    "Hunky Dory",
                    "Honesty can lead to impotency",
                    "More refuges have been destroyed in South Africa",
                    "Red Sails (the contest if open!)",
                    "Previously unknown insects kill people in South Africa",
                    "New kind of nuke bombs has been invented in Russia",
                    "You better think before ridiculing your boss",
                    "Ultrasonic vibrations can increase",
                    "It has grown much bigger than I hoped!",]

    def gen_topic(title):
        topic       = Topic(title=title)
        topic.save() # for many-to-many relations
        topic.tags = random_objects(Tag, 1, 3)
        return topic

    gen = Generator(model=Topic, p_field='title', object_gen=gen_topic,
                    p_field_gen=(lambda: random.choice(TOPIC_TITLES) + ' '))
    gen.generate(count)

def populate_messages(count):
    """
    Create ‘count’ new messages in database. Random author from existing
    users is assigned to every message as well as random topic. Content is
    pretty stupid right now. There may be a few “likers” from existing
    users.
    """
    MESSAGE = ["Cannot imagine this topic is interesting.",
               "I don't wanna die, so let's address this while we can!",
               "Well, I don't know a lot about this, it's dirty.",
               "We should not support this sort of behavior here.",
               "I don't think so.",
               "Disagree. This is *quite* interesting.",
               "Is that a joke?",
               "This makes me choke.",
               "Oh, that's one big mess.",
               "I've never been to South Africa, but it seems it's hard to live there.",
               "Press <kbd>Ctrl+4</kbd> and you're done!",]

    def gen_message(pk):
        message = Message(id=pk)
        message.author = random_object(User)
        message.topic = random_object(Topic)
        message.content = random.choice(MESSAGE)
        message.save() # for many-to-many relations
        message.likers = random_objects(User, 0, 10)
        return message

    gen = Generator(model=Message, p_field='id', object_gen=gen_message,
                    p_field_gen=(lambda: 0))
    gen.generate(count)

def with_comments(fnc, count, what):
    """
    Execute ‘fnc’ telling the user that ‘count’ objects named ‘what’ are
    created. ‘fnc’ is expected to take ‘count’ as argument.

    No action is performed if ‘count’ is not a positive number.
    """
    if count > 0:
        print("Creating {} {}…".format(count, what))
        fnc(count)
        print("Done: {} {} created.".format(count, what))

if __name__ == '__main__':
    args = parser.parse_args()
    if args.show_license:
        print(license)
        exit(0)
    print("Starting Glass populartion script…")
    with_comments(populate_users,    args.users,    'users')
    with_comments(populate_tags,     args.tags,     'tags')
    with_comments(populate_topics,   args.topics,   'topics')
    with_comments(populate_messages, args.messages, 'messages')
