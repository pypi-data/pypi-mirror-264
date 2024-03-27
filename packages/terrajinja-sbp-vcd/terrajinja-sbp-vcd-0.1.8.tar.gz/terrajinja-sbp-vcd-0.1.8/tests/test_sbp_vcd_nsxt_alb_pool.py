import json
import pytest
from cdktf import Testing
from src.terrajinja.sbp.vcd.nsxt_alb_pool import SbpVcdNsxtAlbPool
from .helper import stack, has_resource, has_resource_count


class TestSbpVcdNsxtAlbPool:

    def test_resource(self, stack):
        pool = SbpVcdNsxtAlbPool(
            scope=stack,
            destination_address_name="name",
            destination_port=8080,
            algorithm="Least connections",
            persistence="Client IP",
            destination_address=["10.0.0.1", "10.0.0.2", "10.0.0.3"],
            edge_gateway_id="edge_gateway_id",
            vip_port=8080
        )
        # We should have gotten a formatted pool name
        assert pool.name_input == 'NAME-8080-POOL'

        synthesized = Testing.synth(stack)
        j = json.loads(synthesized)

        has_resource(synthesized, "vcd_nsxt_alb_pool")
        has_resource(synthesized, "vcd_nsxt_ip_set")
        # we should have 1 ip sets
        has_resource_count(synthesized, "vcd_nsxt_ip_set", 1)
        # containing 3 addresses
        assert len(j['resource']['vcd_nsxt_ip_set']['NAME']['ip_addresses']) == 3


if __name__ == "__main__":
    pytest.main()
