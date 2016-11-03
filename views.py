import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from django.shortcuts import render, render_to_response
from main.settings import TEMPLATE_NAME
from pprint import pprint

from instance_manager.models import Instance
from servicecatalog.models import Module
from machine_manager.models import Machine

def index(request):
    return render_to_response('%s/my_search.tpl.html' % TEMPLATE_NAME, {'request': request,})


def autocomplete(request):
    suggestion = []
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', '')).models(Module, Instance, Machine)
    for a in sqs:
        name = a.object.name
        if a.model.__name__ == "Instance":
            my_type = 'Instance'
            url = '/instance/%s/' % a.object.slug
        elif a.model.__name__ == "Module":
            my_type = 'Module'
            url = '/module/%s/' % a.object.slug
        elif a.model.__name__ == "Machine":
            my_type = 'Machine'
            url = '/instance/%s/' % a.object.instance.slug
        else:
            pprint(a.model.__name__)
            url=''
        suggestion.append({'type':my_type, 'name':name, 'url':url})

    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps(suggestion)
    return HttpResponse(the_data, content_type='application/json')