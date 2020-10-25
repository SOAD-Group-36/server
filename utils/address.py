import json

from django.db.models import Field


class Address:
    def __init__(
        self,
        house_no: str,
        street_name: str,
        landmark: str,
        pincode: str,
        state: str,
        city: str,
    ):
        self.house_no = house_no
        self.street_name = street_name
        self.landmark = landmark
        self.pincode = pincode
        self.state = state
        self.city = city

    def __dict__(self) -> dict:
        return {
            "house_no": self.house_no,
            "street_name": self.street_name,
            "landmark": self.landmark,
            "pincode": self.pincode,
            "state": self.state,
            "city": self.city,
        }

    def json(self):
        return json.dumps(self.__dict__())


class AddressField(Field):
    pass
