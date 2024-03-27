from dataclasses import dataclass
from constructs import Construct
from terrajinja.imports.vcd.nsxt_alb_pool import NsxtAlbPool
from .decorators import run_once
from .nsxt_ip_set import SbpVcdNsxtIpSet


@dataclass
class SbpLoadbalancerPool:
    scope: Construct
    destination_address_name: str
    destination_port: int
    edge_gateway_id: str
    destination_address: list
    algorithm: str
    default_port: int
    persistence: str

    def __post_init__(self):
        object.__setattr__(self, "algorithm", self.algorithm.upper().replace(' ', '_'))

    @property
    def name(self):
        return f"{self.destination_address_name}-{self.destination_port}-pool".upper()

    @property
    def member_group_id(self):
        return [SbpVcdNsxtIpSet(
            scope=self.scope,
            edge_gateway_id=self.edge_gateway_id,
            name=self.destination_address_name,
            ip_addresses=self.destination_address
        ).id][0]

    @property
    def persistence_profile(self):
        return {
            'type': self.persistence.upper().replace(' ', '_')
        }


@run_once(parameter_match=["destination_address_name", "destination_port"])
class SbpVcdNsxtAlbPool(NsxtAlbPool):
    """Extends the original class to ensure that it only gets called once"""

    def __init__(self, scope: Construct, destination_address_name: str, destination_port: int,
                 algorithm: str, persistence: str, vip_port: int, destination_address: list,
                 edge_gateway_id: str, id_=None, **kwargs):

        pool = SbpLoadbalancerPool(
            scope=scope,
            destination_address_name=destination_address_name,
            destination_port=destination_port,
            algorithm=algorithm,
            persistence=persistence,
            default_port=vip_port,
            destination_address=destination_address,
            edge_gateway_id=edge_gateway_id
        )

        super().__init__(
            scope=scope,
            id_=pool.name,
            name=pool.name,
            algorithm=pool.algorithm,
            persistence_profile=pool.persistence_profile,
            default_port=pool.default_port,
            member_group_id=pool.member_group_id,
            edge_gateway_id=edge_gateway_id,
            **kwargs
        )
