from ..DataModels.StratColumn import StratColumn
from .Client import Client


# TODO: Create FormationController on SERVER
class StratService:
    client: Client

    def __init__(self, c: Client):
        self.client = c

    def get_stratcolumns(self) -> list[StratColumn]:
        url = "stratcolumns"
        items = self.client.get_list(url)
        cols = [StratColumn.from_dict(w) for w in items]
        return cols

    def get_stratcolumn(self, column_id: int) -> StratColumn:
        url = "stratcolumn/%s" % column_id
        item = self.client.get(url)
        col = StratColumn.from_dict(item)
        return col

    def add_stratcolumn(self, col: StratColumn) -> None:
        url = "stratcolumn/add"
        item = self.client.post(url, col.to_dict())
        server_survey = StratColumn.from_dict(item)
        col.copy_ids_from(server_survey)


