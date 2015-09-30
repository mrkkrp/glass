#!/usr/bin/env python
#
# URL configuration of Glass project
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

"""glass_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls         import include, url
from django.contrib           import admin
from django.core.urlresolvers import reverse
from django.views             import static

from registration.backends.simple.views import RegistrationView
import registration.backends.simple.urls
import django_markdown.urls

import glass.urls

class GlassRegView(RegistrationView):
    def get_success_url(self, request, user):
        return reverse('index')

urlpatterns = [
    url(r'^admin/',    include(admin.site.urls)),
    url(r'^$',         include(glass.urls)),
    url(r'^accounts/register/$', GlassRegView.as_view(), name='register'),
    url(r'^accounts/', include(registration.backends.simple.urls)),
    url('^markdown/',  include(django_markdown.urls)),
]
