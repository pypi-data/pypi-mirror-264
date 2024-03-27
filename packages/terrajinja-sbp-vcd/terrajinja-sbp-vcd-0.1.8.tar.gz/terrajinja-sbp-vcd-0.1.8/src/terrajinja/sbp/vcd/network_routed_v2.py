from ipaddress import IPv4Network

from constructs import Construct

from terrajinja.imports.vcd.network_routed_v2 import NetworkRoutedV2


class SbpVcdNetworkRoutedV2(NetworkRoutedV2):
    """SBP version of vcd.network_routed_v2"""

    def __init__(self, scope: Construct, ns: str, cidr: str, dns: list, **kwargs):
        """Enhances the original vcd.network_routed_v2

        Args:
            scope (Construct): Cdktf App
            id (str): uniq name of the resource
            result_cache (dict): cache of all collected resource outputs so far
            cidr (str): a cidr block to add, which will be used to calculate static_ip_pool and gateway parameters
            dns (list): a list of ips to the dns servers, will be used to fill the dns1 and dns2 parameters

        Original:
            https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/network_routed_v2
        """
        # prepare arguments for constructs
        cidr_ = IPv4Network(cidr)
        static_ip_pool = [
            {
                "startAddress": str(cidr_.network_address + 2),
                "endAddress": str(cidr_.broadcast_address - 1),
            }
        ]
        dns1, dns2 = dns
        gateway = str(cidr_.network_address + 1)

        # call the original resource
        super().__init__(
            scope=scope,
            id_=ns,
            gateway=gateway,
            prefix_length=cidr_.prefixlen,
            dns1=dns1,
            dns2=dns2,
            static_ip_pool=static_ip_pool,
            **kwargs,
        )
