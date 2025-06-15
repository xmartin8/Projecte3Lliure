from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from BrawlStars.models import Torneig, Equip

class MenuForm(forms.Form):
    torneig = forms.ModelChoiceField(queryset=Torneig.objects.all())

def torneig_menu(request):
    queryset = Torneig.objects.all()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            torneig = form.cleaned_data.get("torneig")
            return redirect('classificacio', torneig.id)
    form = MenuForm()
    return render(request, "torneig_menu.html", {
        "tornejos": queryset,
        "form": form,
    })

def classificacio(request, torneig_id):
    torneig = Torneig.objects.get(pk=torneig_id)
    equips = torneig.equips.all()
    classi = []
    for equip in equips:
        punts = 0
        for enf in torneig.enfrontaments.filter(atacant=equip):
            if enf.punts_atacant > enf.punts_defensor:
                punts += 3
            elif enf.punts_atacant == enf.punts_defensor:
                punts += 1
        for enf in torneig.enfrontaments.filter(defensor=equip):
            if enf.punts_defensor > enf.punts_atacant:
                punts += 3
            elif enf.punts_defensor == enf.punts_atacant:
                punts += 1
        classi.append((punts, equip.nom))
    classi.sort(reverse=True)
    return render(request, "classificacio.html", {
        "classificacio": classi,
    })

class EquipForm(forms.ModelForm):
    class Meta:
        model = Equip
        exclude = ()

def crea_equip(request):
    form = EquipForm()
    if request.method == "POST":
        form = EquipForm(request.POST)
        if form.is_valid():
            equips = Equip.objects.filter(nom=form.cleaned_data.get("nom"))
            if equips.exists():
                return HttpResponse("ERROR: aquest nom d'equip ja existeix.")
            form.save()
    return render(request, "crea_equip.html", {
        "form": form,
    })
