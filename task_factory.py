import yaml
import logging
from meta_task import MetaTask


class MissingProperty(Exception):
    def __init__(self, entry: dict, property: str):
        self.message = ("Missing property '" + property + "' in entry " +
                        str(entry) + ".")

    def __str__(self):
        return self.message


prop_name: str = "name"
prop_period: str = "periodicity"


class TaskFactory:
    @staticmethod
    def create_meta_tasks(file: str) -> list:
        meta_tasks: list = []
        with open(file) as f:
            data: list = yaml.load(f, Loader=yaml.FullLoader)
            logging.debug(data)

        for d in data:
            if prop_name not in d.keys():
                raise MissingProperty(d, prop_name)

            if prop_period not in d.keys():
                raise MissingProperty(d, prop_period)

            if len(d.keys()) > MetaTask.NUM_PROPERTIES:
                print("WARNING: Entry '" + str(d) + "' has more than " +
                      str(MetaTask.NUM_PROPERTIES) + " properties.")

            meta_tasks.append(MetaTask(d[prop_name], d[prop_period]))
        # end for

        return meta_tasks

    # end

