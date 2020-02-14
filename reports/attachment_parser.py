from openpyxl import load_workbook
from nav_client.models import NavMtId, GeoZone, SyncDate


def parse(file):
    worksheet = load_workbook(file).worksheets[0]
    for row in worksheet.rows:
        print(int(row[1].value))
        geozone = NavMtId.objects.filter(
            mt_id=int(row[1].value)).first()
        if geozone is not None:
            report_row = {}
            report_row["directory"] = geozone.name or "geozone"
            report_row["geozone"] = GeoZone.objects.filter(
                sync_date=SyncDate.objects.last(),
                nav_id=geozone.nav_id).first()
            report_row["count"] = row[6].value
            report_row["value"] = str(row[5].value).split(' ')[0]
            report_row["ct_type"] = str(row[5].value).split(' ')[1]
            yield report_row
