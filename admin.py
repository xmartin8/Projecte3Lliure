from django.contrib import admin
from BrawlStars.models import Torneig, Equip, Brawler, Enfrontament, Accio

admin.site.register(Torneig)
admin.site.register(Equip)
admin.site.register(Brawler)

class AccioInline(admin.TabularInline):
    model = Accio
    fields = ["temps", "tipus", "brawler", "equip"]
    ordering = ("temps",)

class EnfrontamentAdmin(admin.ModelAdmin):
    search_fields = ["atacant__nom", "defensor__nom", "torneig__nom"]
    readonly_fields = ["resultat",]
    list_display = ["atacant", "defensor", "resultat", "torneig", "data"]
    ordering = ("-data",)
    inlines = [AccioInline,]

    def resultat(self, obj):
        punts_atacant = obj.accions.filter(tipus="PUNT", equip=obj.atacant).count()
        punts_defensor = obj.accions.filter(tipus="PUNT", equip=obj.defensor).count()
        return "{} - {}".format(punts_atacant, punts_defensor)

admin.site.register(Enfrontament, EnfrontamentAdmin)
