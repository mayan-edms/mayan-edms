from __future__ import absolute_import

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission

from .api import diagnostics, tools
from .settings import DISABLE_HOME_VIEW


def home(request):
    if DISABLE_HOME_VIEW:
        return HttpResponseRedirect(reverse('documents:document_list_recent'))
    else:
        return render_to_response('main/home.html', {},
            context_instance=RequestContext(request))


def maintenance_menu(request):
    user_tools = {}
    for namespace, values in tools.items():
        user_tools[namespace] = {
            'title': values['title']
        }
        user_tools[namespace].setdefault('links', [])
        for link in values['links']:
            try:
                permissions = link.get('permissions', [])
                Permission.objects.check_permissions(request.user, permissions)
                user_tools[namespace]['links'].append(link)
            except PermissionDenied:
                pass

    return render_to_response('main/tools.html', {
        'blocks': user_tools,
        'title': _(u'Maintenance menu')
    }, context_instance=RequestContext(request))


def diagnostics_view(request):
    return render_to_response('main/diagnostics.html', {
        'blocks': diagnostics,
        'title': _(u'Diagnostics')
    }, context_instance=RequestContext(request))
