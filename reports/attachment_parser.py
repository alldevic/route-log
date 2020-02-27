import xlrd
from nav_client.models import FlatTableRow, GeoZone, NavMtId, SyncDate
from django.utils import timezone


def parse(file, date, device):
    last_sd = SyncDate.objects.last()
    all_flats = FlatTableRow.objects.filter(
        device=device, sync_date=last_sd)

    worksheet = xlrd.open_workbook(file_contents=file.read()).sheet_by_index(0)

    for row in worksheet.get_rows():
        geozone = NavMtId.objects.filter(
            mt_id=int(row[1].value)).first()

        if not check_schedule(row[7].value, date):
            continue

        if geozone is not None:
            report_row = {}
            report_row["directory"] = geozone.name or "geozone"
            report_row["geozone"] = GeoZone.objects.filter(
                sync_date=last_sd,
                nav_id=geozone.nav_id).first()
            report_row["count"] = row[6].value
            report_row["value"] = str(row[5].value).split(' ')[0]
            report_row["ct_type"] = str(row[5].value).split(' ')[1]

            report_row["time_in"] = timezone.now()
            report_row["time_out"] = timezone.now()
            report_row["is_unloaded"] = False

            report_row["track_points"] = all_flats[:250]
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
