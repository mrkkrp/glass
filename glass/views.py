#!/usr/bin/env python
#
# Views of Glass application
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

from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse
from django.shortcuts               import render
from django.views.decorators.http   import require_GET, require_POST

def index(request):
    """
    Index page of the project.

    The page presents list of popular topics ordered by default by number of
    “likes”. Main feature on the page is “live” search that has a number of
    parameters, and uses AJAX.
    """
    return HttpResponse("index")

def about(request):
    """
    About page, nothing special.
    """
    return render(request, 'glass/about.html')

def topic(request, slug):
    """
    Topic-dedicated page.

    This displays all messages in order (obviously sorted by date or
    creation) and allows registered users to post new messages. This page
    features pagination, anchor links per message, and ability to edit or
    delete last posted message for its author. Messages can be “liked” too
    and this is reversible.
    """
    return HttpResponse("topic — " + slug)

@login_required
def new_topic(request):
    """
    Creation of new topics.

    This is mainly about processing of ‘TopicForm’ and ‘MessageForm’, since
    every topic must have initial message.
    """
    return HttpResponse("new topic")

@require_GET
def get_topic(request):
    """
    Used to interactively retrieve topics of interest.

    Parameters for the search are sent as GET parameters, the whole thing is
    currently done from the index (main) page.
    """
    return HttpResponse("get topic")

@login_required
def user(request, username):
    return HttpResponse("user")

@require_POST
def msg_post(request):
    """
    Post a message.

    Invoked by Java Script from topic page, causes addition of new message.
    """
    return HttpResponse("msg post")

@require_GET
def msg_like(request):
    """
    This is how users can like messages.

    Invoked by Java Script from topic page.
    """
    return HttpResponse("msg like")

@require_POST
def msg_edit(request):
    """
    Edit message.

    Invoked by Java Script from topic page. This essentially replaces old
    contents by new contents. We could have history of edits, but it seems
    like an overcomplication for now.
    """
    return HttpResponse("msg edit")

@require_GET
def msg_del(request):
    """
    Deletion of message.

    Quite trivially, it deletes messages. Only last message in thread can be
    deleted and only by its author.
    """
    return HttpResponse("msg del")
