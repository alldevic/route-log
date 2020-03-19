import xlrd
from nav_client.models import FlatTableRow, GeoZone, NavMtId, Point, SyncDate
import math as m
from reports.models import ContainerType


def parse(file, date, device, container_types):
    types = []
    for ctype in container_types:
        tmp = ContainerType.objects.get(pk=int(ctype))
        types.append((tmp.volume, tmp.material))

    sync_date = SyncDate.objects.filter(datetime__year=date.year,
                                        datetime__month=date.month,
                                        datetime__day=date.day).first()
    all_flats = [x for x in FlatTableRow.objects
                 .filter(device=device, sync_date=sync_date)
                 .prefetch_related('point_value')]
    mtids = [x for x in NavMtId.objects.filter(sync_date=sync_date)]
    geozones = [x for x in GeoZone.objects.filter(sync_date=sync_date)]

    worksheet = xlrd.open_workbook(file_contents=file.read()).sheet_by_index(0)
    for row in worksheet.get_rows():
        if not check_schedule(row[7].value, date):
            continue

        fl = True
        for x in mtids:
            if x.mt_id == int(row[1].value):
                geozone = x
                fl = False
                break
        if fl:
            continue

        row5 = str(row[5].value).split(' ')
        fl = True
        for ctype in types:
            if ctype[0] == row5[0] and ctype[1] == row5[1]:
                fl = False

        if fl:
            continue

        if geozone is not None:
            report_row = {}
            report_row["nav_mt_id"] = geozone.mt_id or None
            report_row["directory"] = geozone.name or "geozone"

            for xx in geozones:
                if int(xx.nav_id) == int(geozone.nav_id):
                    report_row["geozone"] = xx
                    report_points = [x for x in xx.points.all()]
                    break

            report_row["count"] = row[6].value
            report_row["value"] = row5[0]
            report_row["ct_type"] = row5[1]

            report_row["time_in"] = None
            report_row["time_out"] = None
            report_row["is_unloaded"] = False
            m_range = 1000

            current_flats = []
            for flat in all_flats:
                if in_range(flat.point_value, m_range,
                            get_center(report_points)):
                    if report_row["time_in"] is None:
                        report_row["time_in"] = flat.utc
                    current_flats.append(flat)

            if report_row["time_in"] is not None:
                report_row["time_out"] = sorted(
                    current_flats, key=lambda x: x.utc)[-1].utc

            report_row["is_unloaded"] = False

            report_row["track_points"] = current_flats
            yield report_row


def check_schedule(schedule, date):
    schedule = str(schedule).lower()
    if schedule == "ежедневно":
        return True

    if (schedule == "чет" or schedule == "четн" or schedule == "четные")\
            and date.day % 2 == 0:
        return True

    if (schedule == "нечет" or schedule == "нечетн" or schedule == "нечетные")\
            and date.day % 2 == 1:
        return True

    if is_days_numbers(schedule) and f'{date.day:02}' in schedule:
        return True

    if DAYS_NAMES_SHORT[date.weekday()] in schedule:
        return True

    return False


def is_days_numbers(prep_list):
    for day in prep_list:
        if not day.isnumeric():
            return False
    return True


DAYS_NAMES_SHORT = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']


def get_center(points):
    lats = 0.0
    lons = 0.0
    for point in points:
        lats += float(point.lat)
        lons += float(point.lon)
    lats = lats / len(points)
    lons = lons / len(points)

    return Point(lat=lats, lon=lons)


def in_range(point1, dist_m, point2):
    tmp = 111100*m.acos(
        m.sin(float(point1.lat))*m.sin(float(point2.lat)) +
        m.cos(float(point1.lat))*m.cos(float(point2.lat)) *
        m.cos(float(point2.lon) - float(point1.lon))
    )
    return tmp < dist_m
