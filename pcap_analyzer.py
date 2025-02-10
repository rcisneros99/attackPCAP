from scapy.all import rdpcap
from collections import Counter
import argparse
from pprint import pprint
import matplotlib.pyplot as plt
import glob
import os

class PcapAnalyzer:
    def __init__(self, pcap_file):
        self.packets = rdpcap(pcap_file)
        self.filename = os.path.basename(pcap_file)
        
    def basic_stats(self):
        """Get basic stats about the PCAP - useful for quick checks"""
        # Initialize counters
        stats = {
            'total_packets': len(self.packets),
            'protocols': Counter(),  # TCP, UDP, etc
            'ports': Counter(),      # Port numbers
            'ip_addresses': Counter(),  # Might add geolocation later
        }
        
        # Count everything - there's probably a more elegant way to do this
        for pkt in self.packets:
            if 'TCP' in pkt:
                stats['protocols']['TCP'] += 1
                stats['ports'][f'TCP/{pkt.dport}'] += 1
            elif 'UDP' in pkt:
                stats['protocols']['UDP'] += 1
                stats['ports'][f'UDP/{pkt.dport}'] += 1
            elif 'ICMP' in pkt:
                stats['protocols']['ICMP'] += 1
            
            if 'IP' in pkt:
                stats['ip_addresses'][pkt['IP'].dst] += 1
        
        return stats
    
    def attack_pattern_analysis(self):
        """Analyze patterns that might indicate specific attacks"""
        patterns = {
            'possible_dos': 0,
            'possible_bruteforce': 0,
            'possible_injection': 0,
            'possible_xss': 0,
            'possible_infiltration': 0
        }
        
        for pkt in self.packets:
            if 'Raw' in pkt:
                payload = str(pkt['Raw'].load)
                
                # Check for DOS patterns
                if 'HTTP' in payload and pkt.dport == 80:
                    patterns['possible_dos'] += 1
                
                # Check for bruteforce patterns
                if 'USER' in payload or 'PASS' in payload or 'password' in payload.lower():
                    patterns['possible_bruteforce'] += 1
                
                # Check for SQL injection patterns
                if "'" in payload or 'UNION' in payload or 'SELECT' in payload:
                    patterns['possible_injection'] += 1
                
                # Check for XSS patterns
                if '<script>' in payload or 'alert(' in payload:
                    patterns['possible_xss'] += 1
                
                # Check for data exfiltration
                if 'data.' in payload and '.example.com' in payload:
                    patterns['possible_infiltration'] += 1
        
        return patterns
    
    def visualize_stats(self, stats):
        """Create visualizations of the statistics"""
        # Protocol distribution
        plt.figure(figsize=(10, 5))
        protocols = stats['protocols']
        plt.subplot(121)
        plt.pie(protocols.values(), labels=protocols.keys(), autopct='%1.1f%%')
        plt.title('Protocol Distribution')
        
        # Top ports
        plt.subplot(122)
        ports = dict(sorted(stats['ports'].items(), key=lambda x: x[1], reverse=True)[:5])
        plt.bar(ports.keys(), ports.values())
        plt.title('Top 5 Ports')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('pcap_analysis.png')
        print("Analysis visualization saved as 'pcap_analysis.png'")

def main():
    parser = argparse.ArgumentParser(description='Analyze PCAP files')
    parser.add_argument('pcap_files', help='Path to the PCAP file(s). Can use wildcards.')
    args = parser.parse_args()
    
    # Handle wildcards in file path
    pcap_files = glob.glob(args.pcap_files)
    if not pcap_files:
        print(f"No files found matching pattern: {args.pcap_files}")
        return

    for pcap_file in pcap_files:
        print(f"\n{'='*20} Analyzing {os.path.basename(pcap_file)} {'='*20}")
        analyzer = PcapAnalyzer(pcap_file)
        
        print("\n=== Basic Statistics ===")
        stats = analyzer.basic_stats()
        print(f"Total packets: {stats['total_packets']}")
        print("\nProtocol distribution:")
        pprint(dict(stats['protocols']))
        print("\nTop 5 destination ports:")
        pprint(dict(sorted(stats['ports'].items(), key=lambda x: x[1], reverse=True)[:5]))
        
        print("\n=== Attack Pattern Analysis ===")
        patterns = analyzer.attack_pattern_analysis()
        pprint(patterns)
        
        # Create visualizations with unique names for each file
        base_name = os.path.splitext(os.path.basename(pcap_file))[0]
        plt.figure(figsize=(10, 5))
        protocols = stats['protocols']
        plt.subplot(121)
        plt.pie(protocols.values(), labels=protocols.keys(), autopct='%1.1f%%')
        plt.title('Protocol Distribution')
        
        plt.subplot(122)
        ports = dict(sorted(stats['ports'].items(), key=lambda x: x[1], reverse=True)[:5])
        plt.bar(ports.keys(), ports.values())
        plt.title('Top 5 Ports')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'pcap_analysis_{base_name}.png')
        print(f"Analysis visualization saved as 'pcap_analysis_{base_name}.png'")
        plt.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user")
    except Exception as e:
        print(f"Error during analysis: {str(e)}") 