# coding: utf-8

"""
This module contains extra functions/shortcuts used to render HTML.
"""
import os, sys
import re
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import template
from django.utils import simplejson
from django.conf import settings

def _render(request, tpl, user_context):
    """Custom rendering function

    Just a wrapper which automatically adds a RequestContext instance
    (useful to use settings variables like STATIC_URL inside templates)
    """
    return render_to_response(tpl, user_context, 
                              context_instance=template.RequestContext(request))

def _render_to_string(request, tpl, user_context):
    """Custom rendering function

    Same as _render.
    """
    return render_to_string(tpl, user_context,
                            context_instance=template.RequestContext(request))

def _render_error(request, errortpl="error", user_context={}):
    return render_to_response("common/%s.html" % errortpl, user_context,
                              context_instance=template.RequestContext(request))

def render_actions(actions):
    t = template.Template("""{% load libextras %}
{% for a in actions %}{% render_link a %}{% endfor %}
""")
    return t.render(template.Context(dict(actions=actions)))

def _ctx_ok(url):
    return {"status" : "ok", "url" : url}

def _ctx_ko(tpl, ctx):
    return {"status" : "ko", "content" : render_to_string(tpl, ctx)}

def getctx(status, level=1, callback=None, **kwargs):
    if not callback:
        callername = sys._getframe(level).f_code.co_name
    else:
        callername = callback
    ctx = {"status" : status, "callback" : callername}
    for kw, v in kwargs.iteritems():
        ctx[kw] = v
    return ctx

def ajax_response(request, status="ok", respmsg=None,
                  url=None, ajaxnav=False, norefresh=False, 
                  template=None, **kwargs):
    """Ajax response shortcut

    Simple shortcut that sends an JSON response. If a template is
    provided, a 'content' field will be added to the response,
    containing the result of this template rendering.

    :param request: a Request object
    :param status: the response status ('ok' or 'ko)
    :param respmsg: the message that will displayed in the interface
    :param url: url to display after receiving this response
    :param ajaxnav:
    :param norefresh: do not refresh the page after receiving this response
    :param template: eventual template's path
    :param kwargs: dict used for template rendering
    """
    ctx = {}
    for k, v in kwargs.iteritems():
        ctx[k] = v
    if template is not None:
        content = _render_to_string(request, template, ctx)
    elif kwargs.has_key("content"):
        content = kwargs["content"]
    else:
        content = ""
    jsonctx = {"status" : status, "content" : content}
    if respmsg is not None:
        jsonctx["respmsg"] = respmsg
    if ajaxnav:
        jsonctx["ajaxnav"] = True
    if url is not None:
        jsonctx["url"] = url
    jsonctx["norefresh"] = norefresh
    return HttpResponse(simplejson.dumps(jsonctx), mimetype="application/json")

def ajax_simple_response(content, **response_kwargs):
    """Simple AJAX response

    No extra formatting is done. The content is passed directly to simplejon.

    :param content: the response's content (list, dict, string)
    """
    response_kwargs["content_type"] = "application/json"
    return HttpResponse(simplejson.dumps(content), **response_kwargs)

def static_url(path):
    """Returns the correct static url for a given file

    :param path: the targeted static media
    """
    if path.startswith("/"):
        path = path[1:]
    return "%s%s" % (settings.STATIC_URL, path)

def size2integer(value):
    """Try to convert a string representing a size to an integer value
    in bytes.

    Supported formats: 
    * K|k for KB
    * M|m for MB
    * G|g for GB

    :param value: the string to convert
    :return: the corresponding integer value
    """
    m = re.match("(\d+)\s*(\w+)", value)
    if m is None:
        if re.match("\d+", value):
            return int(value)
        return 0
    if m.group(2)[0] in ["K", "k"]:
        return int(m.group(1)) * 2 ** 10
    if m.group(2)[0] in ["M", "m"]:
        return int(m.group(1)) * 2 ** 20
    if m.group(2)[0] in ["G", "g"]:
        return int(m.group(1)) * 2 ** 30
    return 0

@login_required
def topredirection(request):
    """Simple view to redirect the request when no application is specified

    The default "top redirection" can be specified in the *Admin >
    Settings* panel. It is the application that will be launched by
    default. Users that are not allowed to access this application
    will be redirected to the "User preferences" application.

    :param request: a Request object
    """
    from modoboa.lib import parameters
    from modoboa.extensions import exts_pool

    topredir = parameters.get_admin("DEFAULT_TOP_REDIRECTION", app="admin")
    if not topredir in ["admin", "userprefs"]:
        infos = exts_pool.get_extension_infos(topredir)
        path = infos["url"] if infos["url"] else infos["name"]
    else:
        path = topredir

    if topredir in ["admin", "stats"] and \
            request.user.belongs_to_group('SimpleUsers'):
        path = "userprefs"

    return HttpResponseRedirect(path)
