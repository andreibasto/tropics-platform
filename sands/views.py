from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Sand, SandView
from waters.models import Water


@login_required
def index(request: HttpRequest) -> HttpResponse:
    sands = Sand.objects.all()
    return render(request, "sands/index.html", {"sands": sands})


@login_required
def sand(request, id, the_slug):
    sand = Sand.objects.get(id=id)
    if not SandView.objects.filter(sand=sand,session=request.session.session_key):
        view = SandView(sand=sand,
                        ip=request.META['REMOTE_ADDR'],
                        created=datetime.now(),
                        session=request.session.session_key)
        view.save()
    num_views = SandView.objects.filter(sand=sand).count()
    waters = Water.objects.filter(sand=sand)
    go_to_water = ""
    if request.method == "POST":
        data = request.POST.dict()
        if "content" in data:
            content = data["content"]
            content = content.replace('"', '\\"')
            content = content.replace("'", "\\'")

            sand = Sand.objects.get(id=id)
            if not Water.objects.filter(content=content, author=request.user, sand=sand).exists():
                water = Water(content=content, author=request.user, sand=sand)
                water.save()
                go_to_water = water.id
                messages.add_message(request, messages.SUCCESS, "Added water")
        elif "remove_mango" in data:
            water = Water.objects.get(id=data["remove_mango"])
            if request.user.gave_mangoes.filter(id=water.id).exists():
                request.user.gave_mangoes.remove(water)
                water.mangoes -= 1
                water.save()
                go_to_water = water.id
                messages.add_message(request, messages.SUCCESS, "Removed mango")
        elif "give_mango" in data:
            water = Water.objects.get(id=data["give_mango"])
            if not request.user.gave_mangoes.filter(id=water.id).exists():
                request.user.gave_mangoes.add(water)
                water.mangoes += 1
                water.save()
                go_to_water = water.id
                messages.add_message(request, messages.SUCCESS, "Gave mango")
        elif "delete" in data and Water.objects.filter(id=data["delete"]).exists():
            water = Water.objects.get(id=data["delete"])
            water.delete()
            messages.add_message(request, messages.SUCCESS, "Deleted water")

    return render(request, 'sands/sand.html', {"sand": sand, "waters": waters, "num_views": num_views, "go_to_water": go_to_water})