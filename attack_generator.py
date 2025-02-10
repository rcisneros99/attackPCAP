import os
from scapy.all import wrpcap
from datetime import datetime
import logging
from attack import attack_function_mapping
import random
import time
from tqdm import tqdm

class AttackGenerator:
    def __init__(self, distribution):
        self.distribution = distribution
        self.setup_logging()
        
    def setup_logging(self):
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Set up logging
        log_file = f'logs/attack_generation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def generate_attacks(self, num_records):
        """Generate attacks based on the specified distribution and number of records"""
        self.logger.info(f"Starting attack generation for {num_records} records")
        
        # Create output directory if it doesn't exist
        if not os.path.exists('pcaps'):
            os.makedirs('pcaps')

        # Calculate number of packets for each attack type
        attack_counts = {}
        for attack_type, percentage in self.distribution.items():
            attack_counts[attack_type] = int((percentage / 100) * num_records)

        # Generate packets for each attack type
        all_packets = []
        
        with tqdm(total=num_records, desc="Generating packets") as pbar:
            for attack_type, count in attack_counts.items():
                if count > 0:
                    self.logger.info(f"Generating {count} packets for {attack_type}")
                    
                    # Get the attack function
                    attack_func = attack_function_mapping[attack_type]
                    
                    # Generate packets
                    try:
                        packets = attack_func(count)
                        all_packets.extend(packets)
                        pbar.update(count)
                    except Exception as e:
                        self.logger.error(f"Error generating packets for {attack_type}: {str(e)}")

        # Shuffle packets to make the traffic more realistic
        self.logger.info("Shuffling packets...")
        random.shuffle(all_packets)

        # Save to PCAP file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pcap_file = f'pcaps/attack_traffic_{timestamp}.pcap'
        
        try:
            self.logger.info(f"Saving {len(all_packets)} packets to {pcap_file}")
            wrpcap(pcap_file, all_packets)
            self.logger.info("PCAP file saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving PCAP file: {str(e)}")
            raise

        return pcap_file 