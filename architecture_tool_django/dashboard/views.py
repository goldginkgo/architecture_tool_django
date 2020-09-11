from django import template
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404, redirect, render


# @login_required(login_url="/login/")
def dashboard(request):
    return render(request, "index.html")


# @login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("page-404.html")
        return HttpResponse(html_template.render(context, request))

    except Exception:

        html_template = loader.get_template("page-500.html")
        return HttpResponse(html_template.render(context, request))
