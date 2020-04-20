
from nav_client.models import GeoZone, Point, SyncDate
from django.core.management.base import BaseCommand

gzs = [
    {
        "name": "МПС Каз",
        "points": [
            {"lat": 53.122106, "lon": 87.594318},
            {"lat": 53.122249, "lon": 87.594975},
            {"lat": 53.121777, "lon": 87.595849},
            {"lat": 53.121531, "lon": 87.594312},
        ]
    },
    {
        "name": "МПС Таштагол",
        "points": [
            {"lat": 52.846908, "lon": 87.801386},
            {"lat": 52.847364, "lon": 87.801063},
            {"lat": 52.847487, "lon": 87.801680},
            {"lat": 52.847069, "lon": 87.802039},
        ]
    },
    {
        "name": "МПС Междуреченск",
        "points": [
            {"lat": 53.659327, "lon": 88.035571},
            {"lat": 53.658709, "lon": 88.035912},
            {"lat": 53.658544, "lon":  88.034979},
            {"lat": 53.659148, "lon": 88.034539},
        ]
    },
    {
        "name": "МПС Мыски",
        "points": [
            {"lat": 53.777856, "lon": 87.589277},
            {"lat": 53.778290, "lon": 87.589304},
            {"lat": 53.778344, "lon": 87.588220},
            {"lat": 53.777891, "lon": 87.588129},
        ]
    },
    {
        "name": "МПС Мыски 2",
        "points": [
            {"lat": 53.736803, "lon": 87.711749},
            {"lat": 53.736660, "lon": 87.712642},
            {"lat": 53.736013, "lon": 87.712207},
            {"lat": 53.736248, "lon": 87.711113},
        ]
    },
    {
        "name": "МПС Прокопьевск",
        "points": [
            {"lat": 53.821749, "lon": 86.681165},
            {"lat": 53.821055, "lon": 86.681350},
            {"lat": 53.821061, "lon": 86.680438},
            {"lat": 53.821669, "lon": 86.680352},
        ]
    },
    {
        "name": "Полигон ЭкоЛэнд",
        "points": [
            {"lat": 53.821993, "lon": 87.234713},
            {"lat": 53.823075, "lon": 87.236448},
            {"lat": 53.821333, "lon": 87.237875},
            {"lat": 53.821016, "lon": 87.235837},
        ]
    },
    {
        "name": "Полигон Феникс",
        "points": [
            {"lat": 54.127288, "lon": 86.614502},
            {"lat": 54.127854, "lon": 86.611283},
            {"lat": 54.126075, "lon": 86.611605},
            {"lat": 54.126119, "lon": 86.615725},
        ]
    },
    {
        "name": "Полигон Чистый город",
        "points": [
            {"lat": 54.038141, "lon": 86.604681},
            {"lat": 54.040044, "lon": 86.605829},
            {"lat": 54.038872, "lon": 86.609316},
            {"lat": 54.037580, "lon": 86.606720},
        ]
    },
    {
        "name": "Полигон Красобродский",
        "points": [
            {"lat": 54.192153, "lon": 86.408302},
            {"lat": 54.194325, "lon": 86.411510},
            {"lat": 54.192630, "lon": 86.413849},
            {"lat": 54.190784, "lon": 86.410620},
        ]
    },
]


class Command(BaseCommand):
    help = 'Инициализация кастомных геозон'

    def handle(self, *args, **options):
        GeoZone.objects.filter(is_custom=True).delete()

        sync_dates = [x for x in SyncDate.objects.all()]
        for sync_date in sync_dates:
            for gz in gzs:
                x_points = [Point(sync_date=sync_date,
                                  lat=x["lat"], lon=x["lon"])
                            for x in gz["points"]]

                points = Point.objects.bulk_create(x_points)
                tmp = GeoZone.objects \
                    .create(sync_date=sync_date,
                            name=gz["name"],
                            is_custom=True)
                tmp.points.set(points)
                tmp.save()
