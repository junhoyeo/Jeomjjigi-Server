from app import db
from app.models.device import Device

def device_exist(device_id):
    if Device.query.filter_by(name=device_id).first():
        return True
    return False

db.create_all()
