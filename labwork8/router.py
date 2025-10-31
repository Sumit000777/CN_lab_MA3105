# router.py

from ip_utils import ip_to_binary, get_network_prefix

class Router:
    def __init__(self, routes):
        self.forwarding_table = []
        self.build_forwarding_table(routes)

    def build_forwarding_table(self, routes):
        for cidr, link in routes:
            prefix = get_network_prefix(cidr)
            self.forwarding_table.append((prefix, link))
        # Sort by prefix length (longest first)
        self.forwarding_table.sort(key=lambda x: len(x[0]), reverse=True)

    def route_packet(self, dest_ip: str) -> str:
        binary_ip = ip_to_binary(dest_ip)
        for prefix, link in self.forwarding_table:
            if binary_ip.startswith(prefix):
                return link
        return "Default Gateway"

# Example test
if __name__ == "__main__":
    routes = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]

    r = Router(routes)
    print(r.route_packet("223.1.1.100"))  # Link 0
    print(r.route_packet("223.1.2.5"))    # Link 1
    print(r.route_packet("223.1.250.1"))  # Link 4 (ISP)
    print(r.route_packet("198.51.100.1")) # Default Gateway

