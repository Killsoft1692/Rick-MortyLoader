import json
import dataclasses


class DataClassJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return obj.to_dict()
        return super().default(obj)
