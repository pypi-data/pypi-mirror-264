
from google.protobuf.timestamp_pb2 import (
    Timestamp
)
from yandex.cloud.dns.v1.dns_zone_pb2 import (
    DnsZone, PrivateVisibility
)
from yandex.cloud.dns.v1.dns_zone_service_pb2 import (
    ListDnsZonesResponse
)

from tests.fixtures import STUB_FOLDER_ID

STUB_IDNA_ZONE_NAME = "xn--e1aybc.xn--p1ai."
STUB_IDNA_ZONE_ID = 'dnshahmeep0hei5aighe'

IDNA_LIST_DNS_ZONES_RESPONSE_PAGE_1 = ListDnsZonesResponse(
    next_page_token='',
    dns_zones=[
        DnsZone(
            id=STUB_IDNA_ZONE_ID,
            folder_id=STUB_FOLDER_ID,
            created_at=Timestamp(seconds=1710779521, nanos=553000000),
            name="idna-test",
            description="An idna test",
            zone=STUB_IDNA_ZONE_NAME,
            private_visibility=PrivateVisibility()
        )
    ]
)
