import xlrd
from nav_client.models import FlatTableRow, GeoZone, NavMtId, SyncDate
from django.utils import timezone
import math as m
from reports.models import ContainerType


def parse(file, date, device, container_types):
    types = []
    for ctype in container_types:
        tmp = ContainerType.objects.get(pk=int(ctype))

        types.append((tmp.volume, tmp.material))

    last_sd = SyncDate.objects.last()
    all_flats = FlatTableRow.objects.filter(
        device=device, sync_date=last_sd)

    worksheet = xlrd.open_workbook(file_contents=file.read()).sheet_by_index(0)

    mtids = NavMtId.objects.all()
    [x for x in mtids]
    for row in worksheet.get_rows():
        geozone = mtids.filter(mt_id=int(row[1].value)).first()

        if not check_schedule(row[7].value, date):
            continue

        fl = True
        row5 = str(row[5].value).split(' ')
        for ctype in types:
            if ctype[0] == row5[0] and ctype[1] == row5[1]:
                fl = False

        if fl:
            continue

        if geozone is not None:
            report_row = {}
            report_row["directory"] = geozone.name or "geozone"
            report_row["geozone"] = GeoZone.objects.filter(
                sync_date=last_sd,
                nav_id=geozone.nav_id).first()
            report_row["count"] = row[6].value
            report_row["value"] = row5[0]
            report_row["ct_type"] = row5[1]

            current_flats = []
            report_row["time_in"] = None
            report_row["time_out"] = None
            report_row["is_unloaded"] = False
            m_range = 5000

            for flat in all_flats[:5]:
                if in_range(flat.point_value, m_range,
                            report_row["geozone"].points.first()):
                    current_flats.append(flat)

                    if report_row["time_in"] is None:
                        report_row["time_in"] = flat.utc
                    elif report_row["time_out"] is None:
                        report_row["time_out"] = timezone.now()
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


def in_range(point1, dist_m, point2):
    return 111100*m.acos(
        m.sin(float(point1.lat))*m.sin(float(point2.lat)) +
        m.cos(float(point1.lat))*m.cos(float(point2.lat)) *
        m.cos(float(point2.lon) - float(point1.lon))
    ) < dist_m
