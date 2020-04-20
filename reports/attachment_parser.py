import math as m
from datetime import datetime

import xlrd

from nav_client.models import (FlatTableRow, GeoZone, Point)
from reports.models import ContainerType


def parse(file, sync_date, device, container_types):
    types = [x for x in ContainerType.objects.filter(pk__in=container_types)]

    all_flats = [x for x in FlatTableRow.objects
                 .filter(device=device, sync_date=sync_date)
                 .only("id", "utc", "point_value_id")
                 .prefetch_related('point_value')]

    worksheet = xlrd.open_workbook(file_contents=file.read()).sheet_by_index(0)
    rows = [x for x in worksheet.get_rows()]
    mt_ids = [int(row[2].value) for row in rows[1:]]
    geozones = [x for x in GeoZone.objects
                .filter(sync_date=sync_date, mt_id__in=mt_ids, is_custom=False)
                .only("id", "name", "mt_id")
                .prefetch_related("points")]

    res = []
    for row in rows[1:]:
        # if not check_schedule(row[7].value, date):
        #     continue

        # row14 = str(row[14].value).split(' ')

        container_type = [x for x in types
                          if x.name == row[5].value]
        if not container_type:
            continue
        container_type = container_type[0]

        geozone = None
        fl = True
        for x in geozones:
            if x.mt_id and (x.mt_id == int(row[2].value)):
                geozone = x
                fl = False
                break

        if fl or geozone is None:
            continue

        report_row = {}
        report_row["geozone"] = geozone
        report_row["nav_mt_id"] = geozone.mt_id or None
        report_row["directory"] = geozone.name or "geozone"
        report_row["count"] = row[4].value
        report_row["value"] = container_type.volume
        report_row["ct_type"] = container_type.name
        report_row["time_in"] = None
        report_row["time_out"] = None
        report_row["is_unloaded"] = False

        big_range = 350
        small_range = 25
        center = get_center([t for t in geozone.points.all()])
        current_flats = [flat for flat in all_flats
                         if in_range(flat.point_value, big_range, center)]

        if current_flats:
            current_flats = sorted(current_flats, key=lambda x: x.utc)
            fl = False
            for flat in current_flats:
                if in_range(flat.point_value, small_range, center):
                    fl = True
                    if report_row["time_in"] is None:
                        report_row["time_in"] = flat.utc
                    report_row["time_out"] = flat.utc

            if fl and check_unloaded(report_row, container_type):
                report_row["is_unloaded"] = True

        report_row["track_points"] = current_flats
        res.append(report_row)

    if len(rows[1:]):
        custom_geozones = [x for x in GeoZone.objects
                           .filter(sync_date=sync_date, is_custom=True)
                           .prefetch_related("points")]

        for gz in custom_geozones:
            report_row = {}
            report_row["geozone"] = gz
            report_row["directory"] = gz.name or "geozone"
            report_row["time_in"] = None
            report_row["time_out"] = None
            report_row["nav_mt_id"] = None
            report_row["count"] = 0
            report_row["value"] = 0
            report_row["ct_type"] = ""
            report_row["is_unloaded"] = False
            report_row["track_points"] = []

            big_range = 25
            center = get_center([t for t in gz.points.all()])
            current_flats = [flat for flat in all_flats
                             if in_range(flat.point_value, big_range, center)]

            if current_flats:
                current_flats = sorted(current_flats, key=lambda x: x.utc)

            fl = False
            for flat in current_flats:
                fl = True
                if report_row["time_in"] is None:
                    report_row["time_in"] = flat.utc
                report_row["time_out"] = flat.utc

            if fl:
                report_row["is_unloaded"] = True
                res.append(report_row)

    return res


def check_unloaded(report_row, container_type):
    time_in = datetime.strptime(report_row["time_in"], "%Y-%m-%d %H:%M:%S%z")
    time_out = datetime.strptime(report_row["time_out"], "%Y-%m-%d %H:%M:%S%z")

    fact_time = (time_out - time_in).total_seconds()

    if fact_time <= 0:
        return False

    if container_type is None:
        return False

    estim_time = container_type.upload_time * int(report_row["count"])
    return fact_time >= estim_time


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
    prep_list = [x
                 for y in prep_list.split(',')
                 for x in y.split('.')]

    for num in prep_list:
        for ch in num:
            if not ch.isnumeric():
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
