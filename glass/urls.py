#!/usr/bin/env python
#
# URL configuration for Glass application
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

from django.conf.urls import patterns, url
from glass import views

urlpatterns = [
    url('^$',                            views.index,     name='index'),
    url('^topic/(?P<slug>[\w\-]+)/$',    views.topic,     name='topic'),
    url('^new-topic/$',                  views.new_topic, name='new-topic'),
    url('^get-topic/$',                  views.get_topic, name='get-topic'),
    url('^user/(?P<username>[\w\-]+)/$', views.user,      name='user'),
    url('^msg-post/$',                   views.msg_post,  name='msg-post'),
    url('^msg-like/$',                   views.msg_like,  name='msg-like'),
    url('^msg-edit/$',                   views.msg_edit,  name='msg-edit'),
    url('^msg-del/$',                    views.msg_del,   name='msg-del'),
]
