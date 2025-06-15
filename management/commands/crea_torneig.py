from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint

from BrawlStars.models import Torneig, Equip, Brawler, Enfrontament

faker = Faker(["es_CA", "es_ES"])

class Command(BaseCommand):
    help = 'Crea un torneig amb equips i brawlers'

    def add_arguments(self, parser):
        parser.add_argument('nom_torneig', nargs=1, type=str)

    def handle(self, *args, **options):
        nom_torneig = options['nom_torneig'][0]
        torneig = Torneig.objects.filter(nom=nom_torneig)
        if torneig.exists():
            print("Aquest torneig ja existeix.")
            return

        torneig = Torneig(nom=nom_torneig, temporada="temporada")
        torneig.save()

        prefixos = ["Team", "Squad", "Crew", "Clan", "Guild"]
        for i in range(20):
            regió = faker.city()
            prefix = prefixos[randint(0, len(prefixos)-1)]
            nom = f"{prefix} {regió}"
            equip = Equip(regió=regió, nom=nom)
            equip.save()
            equip.torneig.add(torneig)

            for j in range(3):
                nom_b = faker.first_name()
                sobrenom = faker.last_name()
                raritat = "comú"
                data_creacio = timezone.now() - timedelta(days=randint(500, 3000))
                brawler = Brawler(nom=nom_b, sobrenom=sobrenom, raritat=raritat,
                                  dorsal=j + 1, data_creacio=data_creacio,
                                  rol="lluitador", equip=equip)
                brawler.save()

        for atacant in torneig.equips.all():
            for defensor in torneig.equips.all():
                if atacant != defensor:
                    enf = Enfrontament(
                        atacant=atacant,
                        defensor=defensor,
                        torneig=torneig,
                        data=timezone.now()
                    )
                    enf.save()
