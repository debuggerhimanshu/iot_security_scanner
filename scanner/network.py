import socket, ipaddress, subprocess, shutil

DEFAULT_CIDR = "172.25.216.174/24"

def _get_ip_from_ifconfig(interface: str):
    try:
        out = subprocess.check_output(["ipconfig", "getifaddr", interface], text=True).strip()
        return out if out else None
    except Exception:
        return None

def guess_local_cidr() -> str:
    for iface in ("en0", "en1", "en2"):
        ip = _get_ip_from_ifconfig(iface)
        if ip:
            base = ip.rsplit(".", 1)[0] + ".0/24"
            return base
    return DEFAULT_CIDR

def ensure_nmap_available():
    if shutil.which("nmap") is None:
        raise RuntimeError("Install nmap first: brew install nmap")
