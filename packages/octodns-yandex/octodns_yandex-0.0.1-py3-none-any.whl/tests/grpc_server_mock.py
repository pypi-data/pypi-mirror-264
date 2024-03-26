import grpc
import time

from concurrent import futures

import yandex.cloud.dns.v1.dns_zone_service_pb2_grpc as dns_zone_service_pb2_grpc

from yandex.cloud.dns.v1.dns_zone_service_pb2 import (
    ListDnsZonesRequest,
    ListDnsZoneRecordSetsRequest,
    UpdateRecordSetsRequest,

    ListDnsZonesResponse,
    ListDnsZoneRecordSetsResponse,

)

from tests.fixtures.dns_zones import STUB_ZONE_NAME, LIST_DNS_ZONES_RESPONSE_PAGE_1
from tests.fixtures.dns_zones_idna import STUB_IDNA_ZONE_NAME, IDNA_LIST_DNS_ZONES_RESPONSE_PAGE_1, STUB_IDNA_ZONE_ID
from tests.fixtures.record_sets import LIST_RECORD_SETS_RESPONSE_PAGE_1, LIST_RECORD_SETS_RESPONSE_PAGE_2

_DEFAULT_SERVICE_PORT = "50051"
_SERVICE_ADDR = "localhost:" + _DEFAULT_SERVICE_PORT


class DnsZoneServiceMock(dns_zone_service_pb2_grpc.DnsZoneServiceServicer):
    def __init__(self, handler):
        self.__handler = handler

    def List(self, request: ListDnsZonesRequest, context):
        zone = request.filter.split('=')[1].strip('"') if request.HasField('filter') else ''
        if zone == STUB_ZONE_NAME:
            return LIST_DNS_ZONES_RESPONSE_PAGE_1
        elif zone == STUB_IDNA_ZONE_NAME:
            return IDNA_LIST_DNS_ZONES_RESPONSE_PAGE_1
        else:
            context.set_code(grpc.StatusCode.UNIMPLEMENTED)
            context.set_details('Method not implemented!')
            return ListDnsZonesResponse()

    def ListRecordSets(self, request: ListDnsZoneRecordSetsRequest, context):
        if request.zone_id != STUB_IDNA_ZONE_ID:
            if request.page_token == '':
                return LIST_RECORD_SETS_RESPONSE_PAGE_1
            elif request.page_token == LIST_RECORD_SETS_RESPONSE_PAGE_1.next_page_token:
                return LIST_RECORD_SETS_RESPONSE_PAGE_2
        else:
            return IDNA_LIST_DNS_ZONES_RESPONSE_PAGE_1

        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        return ListDnsZoneRecordSetsResponse()

    def UpdateRecordSets(self, request: UpdateRecordSetsRequest, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        return None


def grpc_server(handler):
    service = DnsZoneServiceMock(handler)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port("[::]:" + _DEFAULT_SERVICE_PORT)

    dns_zone_service_pb2_grpc.add_DnsZoneServiceServicer_to_server(service, server)

    server.start()
    assert _is_grpc_endpoint_ready(60)
    return server


def default_channel():
    return grpc.insecure_channel(_SERVICE_ADDR)


def _is_grpc_endpoint_ready(timeout):
    def check_endpoint_ready():
        channel = grpc.insecure_channel(_SERVICE_ADDR)
        client = dns_zone_service_pb2_grpc.DnsZoneServiceStub(channel)

        try:
            client.List(ListDnsZonesRequest(), timeout=1)
        except grpc.RpcError as e:
            return e.code() not in [grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.DEADLINE_EXCEEDED]

        return True

    deadline = time.time() + timeout

    while time.time() <= deadline:
        if check_endpoint_ready():
            return True

    return False