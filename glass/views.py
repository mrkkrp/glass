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
from django.shortcuts               import render, redirect, get_object_or_404
from django.views.decorators.http   import require_GET, require_POST

from glass.forms  import UserForm, TopicForm, MessageForm
from glass.models import User, Tag, Topic, Message

def index(request):
    """
    Index page of the project.

    The page presents list of popular topics ordered by default by number of
    “likes”. Main feature on the page is “live” search that has a number of
    parameters, and uses AJAX.
    """
    return render(request, 'glass/index.html')

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
    topic = get_object_or_404(Topic, slug=slug)
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        msg_form = MessageForm(request.POST)
        if msg_form.is_valid():
            message = msg_form.save(commit=False)
            message.author = request.user
            message.topic  = topic
            message.save()
            msg_form.save_m2m()

    messages = Message.objects.filter(topic=topic)
    context = {'topic': topic,
               'form': MessageForm(),
               'messages': messages}
    return render(request, 'glass/topic.html', context)

@login_required
def new_topic(request):
    """
    Creation of new topics.

    This is mainly about processing of ‘TopicForm’ and ‘MessageForm’, since
    every topic must have initial message.
    """
    if request.method == 'GET':
        context = {'topic_form': TopicForm(prefix='topic_'),
                   'msg_form':   MessageForm(prefix='msg_')}
    elif request.method == 'POST':
        topic_form = TopicForm(request.POST, prefix='topic_')
        msg_form = MessageForm(request.POST, prefix='msg_')
        context = {'topic_form': topic_form,
                   'msg_form':   msg_form}
        if topic_form.is_valid():
            new_topic = topic_form.save()
            if msg_form.is_valid():
                new_msg = msg_form.save(commit=False)
                new_msg.author = request.user
                new_msg.topic  = new_topic
                new_msg.save()
                msg_form.save_m2m()
                return redirect('topic', slug=new_topic.slug)
    return render(request, 'glass/new-topic.html', context=context)

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
    """
    User profile.

    Every registered user can see all profiles, but only his own profile is
    editable for him. This page also displays latest messages authored by
    the user.
    """
    user = get_object_or_404(User, username=username)
    latest_msgs = Message.objects.filter(author=user).order_by('-id')[:5]
    context = {'this_user': user, 'latest_msgs': latest_msgs}
    if request.user == user:
        if request.method == 'GET':
            context['form'] = UserForm(instance=user)
        elif request.method == 'POST':
            form = UserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
            else: # if form is invalid, render it to show messages
                context['form'] = form
    return render(request, 'glass/user.html', context=context)

@require_POST
def msg_post(request):
    """
    Post a message.

    Invoked by Java Script from topic page, causes addition of new message.
    """
    return HttpResponse("msg post")

def carefully_get_msg(request):
    """
    Return message according to parameters in ‘request’ or ‘None’. Request
    should contain parameter named ‘msg_id’ identifying the message.
    """
    user = request.user
    if not user.is_authenticated():
        return None
    msg_id = request.REQUEST.get('msg_id')
    if not msg_id:
        return None
    try:
        msg = Message.objects.get(id=msg_id)
    except Message.DoesNotExist:
        return None
    return msg

@require_GET
def msg_like(request):
    """
    This is how users can like messages.

    Invoked by Java Script from topic page.
    """
    msg = carefully_get_msg(request)
    if not msg:
        return HttpResponse('0')
    if msg.likers.filter(username=request.user.username).exists():
        msg.likers.remove(request.user)
    else:
        msg.likers.add(request.user)
    msg.save()
    return HttpResponse(str(msg.likes()))

@require_POST
def msg_edit(request):
    """
    Edit message.

    Invoked by Java Script from topic page. This essentially replaces old
    contents by new contents. We could have history of edits, but it seems
    like an overcomplication for now.
    """
    msg = carefully_get_msg(request)
    if not msg or not msg.editable_by(request.user):
        return HttpResponse('')
    # msg.delete()
    return HttpResponse("deleted")

@require_GET
def msg_del(request):
    """
    Deletion of message.

    Quite trivially, it deletes messages. Only last message in thread can be
    deleted and only by its author.
    """
    msg = carefully_get_msg(request)
    if not msg or not msg.editable_by(request.user):
        return HttpResponse('')
    msg.delete()
    return HttpResponse("deleted")
