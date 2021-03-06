#!/usr/bin/env python
#
# Extra template tags for Glass application
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

from django                   import template
from django.core.urlresolvers import reverse
from glass.models             import Tag

import bleach
import markdown

register = template.Library()

@register.inclusion_tag('form.html')
def form(action='.'):
    return {'action': action}

@register.inclusion_tag('endform.html')
def endform():
    return {}

@register.inclusion_tag('generic-fields.html')
def generic_fields(form):
    return {'form': form}

@register.inclusion_tag('generic-button.html')
def generic_button(caption):
    return {'caption': caption}

@register.filter(name='css_class')
def css_class(field, cls):
    return field.as_widget(attrs={"class":cls})

@register.filter(name='markdown')
def render_markdown(value):
    goodish_tags = ['p','kbd','br'] + bleach.ALLOWED_TAGS
    return bleach.clean(markdown.markdown(value), tags=goodish_tags)

@register.inclusion_tag('message.html', name='message')
def render_message(message, user):
    editable = message.editable_by(user)
    return {'message': message, 'user': user, 'editable': editable}

@register.inclusion_tag('like-badge.html')
def like_badge(message, user):
    liked = message.likers.filter(username=user.username).exists()
    return {'message': message, 'user': user, 'liked': liked}

@register.inclusion_tag('tags.html', name='tags_of')
def render_tags(topic=None):
    tags = Tag.objects.filter(topic=topic) if topic else Tag.objects.all()
    return {'tags': tags}

@register.simple_tag(takes_context=True)
def with_get_param(context, param, value):
    """
    Add given GET parameter to existing parameters of the page, overwriting
    value of ‘param’ if it already exists.
    """
    request = context['request']
    params  = request.GET.copy()
    params[param] = value
    return '?{}'.format(params.urlencode())

@register.inclusion_tag('pagination.html',
                        name='pagination',
                        takes_context=True)
def render_paginaiton(context):
    """
    Render selection for pagination. Hairy stuff abstracted.

    Note the this tag requires 'page', 'page_range', and 'num_pages' items
    be defined in request context.
    """
    return context
