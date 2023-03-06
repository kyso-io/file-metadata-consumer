import base64
from __init__ import db
import os
import pathlib
import uuid
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import paramiko
from pandas.api.types import is_numeric_dtype


def download_file_from_scs(kyso_file):
    print(f"Downloading file {kyso_file}")
    sftp_host = db["KysoSettings"].find_one({
        "key": "SFTP_HOST"
    })
    sftp_port = db["KysoSettings"].find_one({
        "key": "SFTP_PORT"
    })
    sftp_username = db["KysoSettings"].find_one({
        "key": "SFTP_USERNAME"
    })
    sftp_password = db["KysoSettings"].find_one({
        "key": "SFTP_PASSWORD"
    })
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=sftp_host["value"], port=sftp_port["value"], username=sftp_username["value"], password=sftp_password["value"])
    sftp_client = ssh_client.open_sftp()
    file_extension = pathlib.Path(kyso_file["name"]).suffix
    destination_file_path = f"../data/{uuid.uuid1()}{file_extension}"
    sftp_client.get(kyso_file["path_scs"], destination_file_path)
    ssh_client.close()
    return destination_file_path


def process_file_with_separated_values(kyso_file):
    # Download file from sfpt
    destination_file_path = download_file_from_scs(kyso_file)
    # Analize file
    df = pd.read_csv(destination_file_path)
    numeric_columns = list()
    for column_name in df.columns.values:
        if is_numeric_dtype(df[column_name]):
            numeric_columns.append(column_name)
    columns_stats = list()
    for column_name in numeric_columns:
        column_value = {
            "column": column_name,
            "count": int(df[column_name].count()),
            "maxValue": float(np.max(df[column_name])),
            "minValue": float(np.min(df[column_name])),
            "avgValue": float(np.mean(df[column_name])),
            "stdDev": float(np.std(df[column_name])),
            "medianValue": float(np.median(df[column_name])),
            "images": list(),
        }
        image = BytesIO()
        plt.hist(df[column_name], bins=int(column_value["count"] ** 0.5))
        plt.savefig(image, format='png')
        file_content = base64.b64encode(image.getbuffer())
        plt.clf()
        column_value["images"].append(str(file_content, 'utf-8'))
        columns_stats.append(column_value)
    # Update file metadata
    db["File"].update_one({
        "id": kyso_file["id"],
    }, {
        "$set": {
            "columns_stats": columns_stats
        }
    })
    # Remove downloaded file
    os.remove(destination_file_path)
    return
