import yaml
import logging
from meta_task import MetaTask


class MissingProperty(Exception):
    def __init__(self, entry: dict, property: str):
        self.message = ("Missing property '" + property + "' in entry " +
                        str(entry) + ".")

    def __str__(self):
        return self.message


class TaskFactory:
    @staticmethod
    def create_meta_tasks(file: str) -> list:
        meta_tasks: list = []
        with open(file) as f:
            data: list = yaml.load(f, Loader=yaml.FullLoader)
            logging.debug(data)

        for d in data:
            # check that all required properties are available!
            for prop in MetaTask.REQUIRED_PROPERTIES:
                if prop not in d.keys():
                    raise MissingProperty(d, prop)

            if len(d.keys()) > len(MetaTask.REQUIRED_PROPERTIES):
                print("WARNING: Entry '" + str(d) + "' has more than " +
                      str(len(MetaTask.REQUIRED_PROPERTIES)) + " properties.")

            meta_tasks.append(MetaTask(d["name"], d["periodicity"]))
        # end for

        return meta_tasks

    # end
