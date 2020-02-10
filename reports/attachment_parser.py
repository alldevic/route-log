from openpyxl import load_workbook
from nav_client.models import NavMtId


def parse(file):
    worksheet = load_workbook(file).worksheets[0]
    for row in worksheet.rows:
        report_row = {}
        report_row["geozone"] = NavMtId.objects.filter(
            mt_id=int(row[1].value)).first()
        report_row["count"] = row[6].value
        report_row["value"] = str(row[5].value).split(' ')[0]
        report_row["ct_type"] = str(row[5].value).split(' ')[1]
        yield report_row
