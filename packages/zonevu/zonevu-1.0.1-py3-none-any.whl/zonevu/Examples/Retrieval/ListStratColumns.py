from ...Zonevu import Zonevu


def main_list_stratcolumns(zonevu: Zonevu):
    strat_svc = zonevu.strat_service

    print('Strat Columns:')
    stratcolumn_entries = strat_svc.get_stratcolumns()
    for entry in stratcolumn_entries:
        print('%s (%s)' % (entry.name, entry.id))

    if len(stratcolumn_entries) > 0:
        entry = stratcolumn_entries[0]
        stratcolumn = strat_svc.get_stratcolumn(entry.id)

    print("Execution was successful")
