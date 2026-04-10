import nmap
from .network import ensure_nmap_available

def discover_devices(cidr="172.25.216.174/24"):
    ensure_nmap_available()
    nm = nmap.PortScanner()
    nm.scan(hosts=cidr, arguments="-Pn")
    devices = []
    for host in nm.all_hosts():
        entry = {"ip": host, "mac": nm[host]["addresses"].get("mac")}
        devices.append(entry)
    return devices
