from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class Company(DataClassJsonMixin):
    #: API Version
    Version: str = ''
    #: ZoneVu server runtime version
    RuntimeVersion: str = '?'
    #: Company name associated with this ZoneVu account
    CompanyName: str = ''
    #: ZoneVu username accessing this ZoneVu accounts
    UserName: str = ''
    #: ZoneVu corporate notice
    Notice: str = ''

    def printNotice(self):
        print()
        print("Zonevu Web API Version %s. Zonevu Server Version %s." % (self.Version, self.RuntimeVersion))
        print(self.Notice)
        print("%s accessing ZoneVu account '%s'" % (self.UserName, self.CompanyName))
        print()

