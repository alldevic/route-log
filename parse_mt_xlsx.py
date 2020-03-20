import xlrd
import json
import random


def parse(filepath, sync_date_id):
    worksheet = xlrd.open_workbook(filepath).sheet_by_index(0)

    cc = 0
    res = []
    for row in worksheet.get_rows():
        if cc == 0:
            cc += 1
            continue

        q_id = int(row[0].value)
        sync_id = int(sync_date_id)
        name = str(row[2].value)
        nav_id = int(row[3].value)
        try:
            mt_id = int(row[4].value)
        except Exception:
            mt_id = None

        node = {}
        node["model"] = "nav_client.navmtid"
        node["pk"] = q_id
        fields_node = {}
        fields_node["sync_date"] = sync_id
        fields_node["name"] = name
        fields_node["nav_id"] = nav_id
        fields_node["mt_id"] = mt_id
        node["fields"] = fields_node

        res.append(node)

        # [
        # {
        #     "model": "nav_client.navmtid",
        #     "pk": 1,
        #     "fields": {
        #         "sync_date": 20,
        #         "name": "\u041b\u0443\u0437\u0438\u043d\u0430 \u0443\u043b., 6, \u041c\u0443\u043d\u0434\u044b\u0431\u0430\u0448",
        #         "nav_id": 7331,
        #         "mt_id": 230
        #     }
        # },
        #
        # ]
        #

    res_json = json.dumps(res)
    out_file = open(f"NavMtId-{int(random.random()*1000)}.json", "w")
    out_file.write(res_json)
    out_file.close()


if __name__ == "__main__":
    parse("000.xlsx", 1)
