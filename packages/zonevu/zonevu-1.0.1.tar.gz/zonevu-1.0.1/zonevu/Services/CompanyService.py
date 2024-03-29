from typing import Tuple
from .Client import Client
from ..DataModels.Company import Company
from ..DataModels.StratColumn import StratColumn
import warnings


class CompanyService:
    client: Client

    def __init__(self, c: Client):
        self.client = c

    def get_info(self) -> Company:
        item = self.client.get('company', None, False)
        return Company.from_dict(item)

    # DEPRECATED - moved to FormationService
    def get_stratcolumns(self) -> list[StratColumn]:
        # Deprecated
        url = "stratcolumns"
        items = self.client.get_list(url)
        cols = [StratColumn.from_dict(w) for w in items]
        return cols

    # DEPRECATED - moved to FormationService
    def get_stratcolumn(self, column_id: int) -> StratColumn:
        url = "stratcolumn/%s" % column_id
        item = self.client.get(url)
        col = StratColumn.from_dict(item)
        return col

    def get_delete_authorization(self) -> None:
        """
        Sends a 6-digit delete authorization code the caller's cell phone or email address.
        Good for 24 hours and only from the device that called this method.
        Available only if this ZoneVu account is enabled for Web API deleting.
        @return:
        """
        self.client.get('company/deleteauth')

    def confirm_delete_authorization(self, code: str) -> Tuple[bool, str]:
        """
        Confirms whether a 6-digit delete authorization code is valid for this device.
        @param code: 6-digit authorization code
        @return: true or false, and a message that is 'OK' if true, or an error message if false.
        """
        item = self.client.get_dict('company/confirmdeleteauth', {"deletecode": code})
        return item["confirmed"], item["msg"]
