import qrcode
import os
import pymongo
from datetime import datetime, timezone


from uuid import uuid4

dbclient = pymongo.MongoClient(os.getenv("DB_CONNECTION_STRING"))

db = dbclient["vault_db"]
qrs_table = db["qrs"]


def generate_qr():
    # qr congiguration
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # current_path = os.getcwd()
    # print(current_path)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)

    # generation of qr data and name of image
    qr_name = f"{str(uuid4())}.png"
    qr_data = str(uuid4())
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")


    os.makedirs(f"{script_dir}/static/images/qr_dir/", exist_ok=True)  # Создать папку, если её нет
    img.save(f"{script_dir}/static/images/qr_dir/{qr_name}")
    qrs_table.insert_one(
        {
            "qr_name": qr_name,
            "qr_data": qr_data,
            "created_at": datetime.now(timezone.utc),
            "is_scanned": False,
            "scanned_by": None,
        })
    return qr_name



# generate_qr()








def test():
    return os.getenv("DB_CONNECTION_STRING")
