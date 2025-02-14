# PCAP generator

A tool for generating and analyzing network attack traffic patterns for testing and research purposes.

## NOTE

This tool is intended for research and testing purposes only. Do not use it to generate attacks against systems you don't own or have explicit permission to test!

## OVERVIEW

This project provides the following system:
- Generating various types of network attack traffic
- Creating PCAP files with customizable attack distributions
- Analyzing generated PCAP files for validation
- Visualizing attack patterns and network traffic statistics

## SUPPORTED ATTACK TYPES

1. DDoS Attacks
   - HOIC (High Orbit Ion Cannon)
   - LOIC HTTP
   - Hulk
   - GoldenEye
   - Slowloris
   - SlowHTTPTest

2. Brute Force Attacks
   - FTP
   - Web Login
   - XSS Attempts

3. Other Attacks
   - SQL Injection
   - Bot Activity
   - Data Infiltration

## INSTALLATION

1. Clone the repository:
   ```bash
   git clone https://github.com/rcisneros99/attackPCAP.git
   cd attackPCAP
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install Wireshark for PCAP analysis:
   ```bash
   # macOS
   brew install --cask wireshark

   # Ubuntu/Debian
   sudo apt-get install wireshark

   # CentOS/RHEL
   sudo yum install wireshark
   ```

## USAGE

1. Generating Attack Traffic

   Using the GUI:
   ```bash
   python attack_gui.py
   ```

   Using the CLI:
   ```bash
   # Interactive mode
   python cli.py --interactive

   # Using a configuration file
   python cli.py --config attack_config.json

   # Using default distribution
   python cli.py --records 1000
   ```

2. Analyzing Generated Traffic
   ```bash
   # Analyze a specific PCAP file
   python pcap_analyzer.py pcaps/attack_traffic_YYYYMMDD_HHMMSS.pcap

   # Analyze all PCAP files in the directory
   python pcap_analyzer.py "pcaps/attack_traffic_*.pcap"
   ```

## CONFIGURATION

You can customize the attack distribution using a JSON configuration file:

```json
{
    "num_records": 1000,
    "distribution": {
        "ddos_attack_hoic": 10,
        "ddos_attack_loic_http": 10,
        "dos_attack_hulk": 10,
        "bot_activity": 10,
        "ftp_bruteforce": 10,
        "infiltration": 10,
        "dos_attack_slowhttptest": 10,
        "dos_attack_goldeneye": 5,
        "dos_attack_slowloris": 5,
        "brute_force_web": 10,
        "brute_force_xss": 5,
        "sql_injection": 5
    }
}
```


## PROJECT STRUCTURE

- `attack.py`: Core attack generation functions
- `attack_gui.py`: GUI interface for attack configuration
- `cli.py`: Command-line interface
- `pcap_analyzer.py`: PCAP file analysis tool
- `config.py`: Global configuration settings
- `requirements.txt`: Python dependencies

## OUTPUT

- Generated PCAP files are saved in the `pcaps/` directory
- Analysis visualizations are saved as PNG files
- Logs are stored in the `logs/` directory
