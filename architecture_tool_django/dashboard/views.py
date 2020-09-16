from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render  # get_object_or_404, redirect
from django.template import loader


@login_required(login_url="/accounts/login/")
def dashboard(request):
    return render(request, "pages/home.html")


@login_required(login_url="/accounts/login/")
def contacts(request):
    return render(request, "pages/contacts.html")


@login_required(login_url="/accounts/login/")
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
