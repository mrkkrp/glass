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
from django.core.paginator          import Paginator, EmptyPage, PageNotAnInteger
from django.http                    import HttpResponse
from django.shortcuts               import render, redirect, get_object_or_404
from django.views.decorators.http   import require_GET, require_POST

from glass.forms  import UserForm, TopicForm, MessageForm
from glass.models import User, Tag, Topic, Message

@require_GET
def index(request):
    """
    Index page of the project.

    The page presents list of popular topics ordered by default by number of
    “likes”. Main feature on the page is “live” search that has a number of
    parameters, and uses AJAX.
    """
    page_size = request.GET.get('page_size', 5)
    page      = request.GET.get('page', 1)
    tag       = request.GET.get('tag')
    search    = request.GET.get('search')
    tm        = Topic.objects
    topics    = tm.filter(tags__in=[tag]) if tag else tm.all()
    if search:
        topics = topics.filter(title__contains=search)
    # FIXME The following processing logic assumes that relatively small
    # (maybe a few hundreds) number of topics is returned by ‘topic’ query
    # set. This may be *quite* slow if the data base contains lots of
    # topics. If this is the case, we could add ‘initial_message’ foreign
    # key field to ‘Topic’ model and use it to sort topics on data base
    # level. Other solutions would involve lower level of interaction with
    # the data base and thus may lock the application into using of
    # particular back-end, which is often bad design.
    topics = sorted(list(topics),
                    key=lambda x: x.initial_message().likes(),
                    reverse=True)
    # ↑ Who could believe that Python copies so much of Lisp…
    context = {}
    if topics:
        paginator = Paginator(topics, page_size)
        num_pages = paginator.num_pages
        try:
            p = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            p = paginator.page(num_pages)
        context['page'] = p
        # Range of page links to show, we should take care of situations
        # when there are too many pages:
        page_range = range(max(1, p.number - 4),
                           min(num_pages, p.number + 4) + 1)
        context['page_range'] = page_range
        context['num_pages'] = num_pages
    else:
        context['page'] = None
    return render(request, 'glass/index.html', context=context)

def about(request):
    """
    About page, nothing special.
    """
    return render(request, 'glass/about.html')

def topic(request, slug):
    """
    Topic-dedicated page.

    This displays all messages in order and allows registered users to post
    new messages. This page features anchor links per message and ability to
    edit or delete last posted message for its author. Messages can be
    “liked” too and this is reversible.
    """
    topic = get_object_or_404(Topic, slug=slug)
    messages = Message.objects.filter(topic=topic)
    context = {'topic': topic,
               'form': MessageForm(),
               'messages': messages}
    if request.user.is_authenticated():
        if request.method == 'POST':
            msg_form = MessageForm(request.POST)
            if msg_form.is_valid():
                message = msg_form.save(commit=False)
                message.author = request.user
                message.topic = topic
                message.save()
                msg_form.save_m2m()
                return redirect('topic', slug=slug)
            else:
                context['form'] = msg_form # render errors
    return render(request, 'glass/topic.html', context)

@login_required
def new_topic(request):
    """
    Creation of new topics.

    This is mainly about processing of ‘TopicForm’ and ‘MessageForm’, since
    every topic must have initial message.
    """
    if request.method == 'GET':
        context = {'topic_form': TopicForm(prefix='topic'),
                   'msg_form':   MessageForm(prefix='msg')}
    elif request.method == 'POST':
        topic_form = TopicForm(request.POST, prefix='topic')
        msg_form = MessageForm(request.POST, prefix='msg')
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

def carefully_get_msg(request):
    """
    Return message according to parameters in ‘request’ or ‘None’. Request
    should contain parameter named ‘msg_id’ identifying the message.
    """
    user = request.user
    if not user.is_authenticated():
        return None
    msg_id = request.GET.get('msg_id')
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

@require_GET
def msg_del(request):
    """
    Deletion of message.

    Quite obviously, it deletes messages. Only last message in thread can be
    deleted and only by its author. Staff can delete everything, of course.
    """
    msg = carefully_get_msg(request)
    topic = msg.topic
    if not msg or not msg.editable_by(request.user):
        return HttpResponse('')
    msg.delete()
    # if this is the single message in topic, delete topic:
    if not Message.objects.filter(topic=topic).exists():
        topic.delete()
    return HttpResponse("deleted")
