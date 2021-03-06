"""This module provides the views for the TamPerovskites explorer interface."""

import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from mpcontribs.rest.views import get_endpoint
from mpcontribs.io.core.components import render_dataframe
from mpcontribs.io.core.recdict import render_dict
from ..rest.rester import TamPerovskitesRester

def index(request):
    ctx = RequestContext(request)
    if request.user.is_authenticated():
        API_KEY = request.user.api_key
        ENDPOINT = request.build_absolute_uri(get_endpoint())
        with TamPerovskitesRester(API_KEY, endpoint=ENDPOINT) as mpr:
            try:
                provenance = render_dict(mpr.get_provenance(), webapp=True)
                df = mpr.get_contributions()
                table = render_dataframe(df, webapp=True)
            except Exception as ex:
                ctx.update({'alert': str(ex)})
    else:
        ctx.update({'alert': 'Please log in!'})
    return render_to_response("tam_perovskites_explorer_index.html", locals(), ctx)
