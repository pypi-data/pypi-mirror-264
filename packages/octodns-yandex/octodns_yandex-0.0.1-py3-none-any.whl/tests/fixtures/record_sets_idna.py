import pytest

from yandex.cloud.dns.v1.dns_zone_pb2 import (
    RecordSet
)
from yandex.cloud.dns.v1.dns_zone_service_pb2 import (
    ListDnsZoneRecordSetsResponse
)

IDNA_LIST_RECORD_SETS_RESPONSE_PAGE_1 = ListDnsZoneRecordSetsResponse(
    next_page_token='',
    record_sets=[
        RecordSet(
            name="xn--b1agh1afp.xn--e1aybc.xn--p1ai.",
            type="A",
            ttl=600,
            data="127.0.0.2",
        ),
        RecordSet(
            name="xn--e1aybc.xn--p1ai.",
            type="A",
            ttl=600,
            data="127.0.0.1",
        ),
        RecordSet(
            name="xn--e1aybc.xn--p1ai.",
            type="NS",
            ttl=3600,
            data="ns.internal.",
        ),
        RecordSet(
            name="xn--e1aybc.xn--p1ai.",
            type="SOA",
            ttl=3600,
            data="ns.internal. mx.cloud.yandex.net. 1 10800 900 604800 900",
        ),
    ]
)
