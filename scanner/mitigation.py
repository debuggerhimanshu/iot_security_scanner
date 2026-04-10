def suggest_fixes(open_ports):
    """
    Suggests security fixes based on detected open ports.
    """

    suggestions = []
    for port in open_ports:
        if port == 21:
            suggestions.append("Disable FTP (port 21) or use SFTP instead.")
        elif port == 22:
            suggestions.append("Secure SSH (port 22) with strong passwords/keys.")
        elif port == 23:
            suggestions.append("Disable Telnet (port 23) – use SSH instead.")
        elif port == 80:
            suggestions.append("Use HTTPS instead of HTTP (port 80).")
        elif port == 443:
            suggestions.append("Ensure SSL certificates on port 443 are up-to-date.")
        elif port == 8080:
            suggestions.append("Harden management UI (port 8080) with TLS and authentication.")
        else:
            suggestions.append(f"Review service running on port {port} and secure it.")

    if not suggestions:
        suggestions.append("No risky ports detected. Device appears secure.")

    return suggestions
