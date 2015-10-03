#!/usr/bin/env python
#
# Various forms used in Glass application
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

from django.forms                   import ModelForm, ValidationError
from django.forms.models            import modelform_factory
from django.contrib.auth.models     import User
from django.template.defaultfilters import slugify
from glass.models                   import Topic, Message

UserForm = modelform_factory(User, fields=['first_name','last_name','email'])
MessageForm = modelform_factory(Message, fields=['content'])

class TopicForm(ModelForm):

    def clean_title(self):
        data = slugify(self.cleaned_data['title'])
        if Topic.objects.filter(slug=data):
            raise ValidationError('Such (or similar) topic already exists!')
        return data

    class Meta:
        model = Topic
        fields = ['title', 'tags']
