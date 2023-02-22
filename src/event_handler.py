import json

from __init__ import db
from helpers import process_file_with_separated_values


async def check_report_files(msg):
    payload = json.loads(msg.data.decode("utf-8"))
    report = payload['data']['report']
    print(f"Received a message on '{msg.subject}' for report '{report['id']} - {report['sluglified_name']}'")
    files = db["File"].find({
        "report_id": report["id"]
    }).sort("version", -1)
    # Group files by name
    files_dict = dict()
    for kyso_file in files:
        if kyso_file["name"] not in files_dict:
            files_dict[kyso_file["name"]] = []
        if len(files_dict[kyso_file["name"]]) == 2:
            continue
        files_dict[kyso_file["name"]].append(kyso_file)
    # Get mew files or thouse have different sha respect to the previous version
    files_to_check = list()
    for file_name in files_dict:
        if len(files_dict[file_name]) == 1:
            files_to_check.append(files_dict[file_name][0])
        elif files_dict[file_name][0]["sha"] != files_dict[file_name][1]["sha"]:
            files_to_check.append(files_dict[file_name][0])
    for kyso_file in files_to_check:
        if kyso_file["name"].endswith(".csv") or kyso_file["name"].endswith(".tsv"):
            print(f"Processing file {kyso_file['name']}...")
            process_file_with_separated_values(kyso_file)
            print(f"Processed file {kyso_file['name']}")
    return
