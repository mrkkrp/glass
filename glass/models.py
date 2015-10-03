#!/usr/bin/env python
#
# Modelling of application domain
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

from django.db                      import models
from django.contrib.auth.models     import User
from django.template.defaultfilters import slugify

class Tag(models.Model):
    name = models.CharField(max_length=16, primary_key=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(max_length=128)
    slug  = models.SlugField(unique=True)
    tags  = models.ManyToManyField(Tag)

    def likes(self):
        """
        Return number of people who like this topic. This is currently equal to
        number of people who like its introductory message.
        """
        return Message.objects.filter(topic=self)[0].likes()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        models.Model.save(self, *args, **kwargs)

    def __str__(self):
        return self.slug

class Message(models.Model):
    author   = models.ForeignKey(User)
    topic    = models.ForeignKey(Topic)
    content  = models.TextField()
    created  = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    likers   = models.ManyToManyField(User, related_name='liked')

    def likes(self):
        """
        How many people like this message?
        """
        return self.likers.count()

    def __str__(self):
        return str(self.id) + ' by ' + self.author.username

    class Meta:
        ordering = ['created']
