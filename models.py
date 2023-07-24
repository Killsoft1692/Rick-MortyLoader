from dataclasses import dataclass

from dataclass_wizard import JSONWizard


@dataclass
class Info(JSONWizard):
    class Meta(JSONWizard.Meta):
        json_key_to_field = {
            '__all__': True,
            'Id': 'id',
            'Metadata': 'metadata',
            'RawData': 'raw_data'
        }

    id: str
    metadata: str
    raw_data: dict
