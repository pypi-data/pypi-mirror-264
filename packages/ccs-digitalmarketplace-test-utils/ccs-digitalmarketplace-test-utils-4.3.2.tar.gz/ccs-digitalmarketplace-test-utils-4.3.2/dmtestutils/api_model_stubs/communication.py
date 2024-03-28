from datetime import datetime, timedelta

from .base import BaseAPIModelStub


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class CommunicationStub(BaseAPIModelStub):
    resource_name = 'communications'

    admin_user = {
        'id': 123,
        'email': 'test+123@digital.cabinet-office.gov.uk'
    }
    supplier_user = {
        'id': 456,
        'email': 'test+456@digital.gov.uk'
    }
    default_time = datetime(2024, 3, 14, 14, 30)
    default_data = {
        'id': 1234,
        'subject': 'Communication Subject',
        'supplierId': 1234,
        'supplierName': "My Little Company",
        'frameworkSlug': 'g-cloud-14',
        'frameworkFramework': 'g-cloud',
        'frameworkFamily': 'g-cloud',
        'frameworkName': 'G-Cloud 14',
        'frameworkStatus': 'pending',
        'createdAt': default_time.strftime(DATETIME_FORMAT),
        'updatedAt': default_time.strftime(DATETIME_FORMAT),
        'links': {},
        'messages': [],
    }
    optional_keys = [
        ('supplierName', 'supplier_name'),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if kwargs.get('archived'):
            self.response_data.update(**{
                'archivedByUserEmail': self.admin_user["email"],
                'archivedByUserId': self.admin_user["id"]
            })

        message_data = {
            'id': int(f"{self.response_data['id']}1"),
            'communicationId': self.response_data["id"],
            'text': 'This is the communication message sent by CCS',
            'sentAt': self.default_time.strftime(DATETIME_FORMAT),
            'sentByUserId': self.admin_user["id"],
            'sentByUserEmail': self.admin_user["email"],
            'target': 'for_supplier',
        }

        message_data['attachments'] = [
            {"id": int(f"{message_data['id']}{index + 1}")} | attachment
            for index, attachment in enumerate(kwargs.get('attachments', []))
        ]

        if kwargs.get('read') or kwargs.get('last_message_target', 'for_admin') == 'for_admin':
            message_data.update(**{
                'readAt': (
                    self.default_time
                    + timedelta(minutes=self.response_data['id'])
                ).strftime(DATETIME_FORMAT),
                'readByUserId': self.supplier_user["id"],
                'readByUserEmail': self.supplier_user["email"]
            })

        self.response_data['messages'].append(message_data)

        if kwargs.get('last_message_target', 'for_admin') == 'for_admin':
            message_data = {
                'id': int(f"{self.response_data['id']}2"),
                'communicationId': self.response_data["id"],
                'text': 'This is the communication message sent by Supplier',
                'sentAt': (
                    self.default_time
                    + timedelta(days=self.response_data['id'])
                ).strftime(DATETIME_FORMAT),
                'sentByUserId': self.supplier_user["id"],
                'sentByUserEmail': self.supplier_user["email"],
                'target': 'for_admin',
                'attachments': []
            }

            if kwargs.get('read'):
                message_data.update(**{
                    'readAt': (
                        self.default_time
                        + timedelta(days=self.response_data['id'], minutes=self.response_data['id'])
                    ).strftime(DATETIME_FORMAT),
                    'readByUserId': self.admin_user["id"],
                    'readByUserEmail': self.admin_user["email"]
                })

            self.response_data['messages'].append(message_data)
