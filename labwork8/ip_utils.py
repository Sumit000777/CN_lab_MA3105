# ip_utils.py

def ip_to_binary(ip_address: str) -> str:
    """Convert dotted-decimal IP to 32-bit binary string."""
    octets = ip_address.split('.')
    binary_octets = [format(int(octet), '08b') for octet in octets]
    return ''.join(binary_octets)

def get_network_prefix(ip_cidr: str) -> str:
    """Return binary network prefix from CIDR notation."""
    ip, prefix_length = ip_cidr.split('/')
    prefix_length = int(prefix_length)
    binary_ip = ip_to_binary(ip)
    return binary_ip[:prefix_length]

# Example execution
if __name__ == "__main__":
    print(ip_to_binary("192.168.1.1"))
    print(get_network_prefix("200.23.16.0/23"))

