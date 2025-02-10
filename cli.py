import argparse
import json
from attack_generator import AttackGenerator
import sys

def get_user_input_distribution():
    """Get attack distribution interactively from user"""
    print("\nEnter percentage for each attack type (total must sum to 100%):")
    distribution = {
        'ddos_attack_hoic': 0,
        'ddos_attack_loic_http': 0,
        'dos_attack_hulk': 0,
        'bot_activity': 20,
        'ftp_bruteforce': 10,
        'infiltration': 20,
        'dos_attack_slowhttptest': 0,
        'dos_attack_goldeneye': 0,
        'dos_attack_slowloris': 0,
        'brute_force_web': 10,
        'brute_force_xss': 20,
        'sql_injection': 20
    }

    for attack_type in distribution.keys():
        while True:
            try:
                print(f"\nCurrent attack type: {attack_type.replace('_', ' ').title()}")
                value = float(input(f"Enter percentage (current: {distribution[attack_type]}%): ") or distribution[attack_type])
                if 0 <= value <= 100:
                    distribution[attack_type] = value
                    break
                else:
                    print("Please enter a value between 0 and 100")
            except ValueError:
                print("Please enter a valid number")

    total = sum(distribution.values())
    if abs(total - 100) > 0.01:
        print(f"\nWarning: Total distribution is {total}%, not 100%")
        if input("Would you like to normalize the distribution to 100%? (y/n): ").lower() == 'y':
            factor = 100 / total
            distribution = {k: v * factor for k, v in distribution.items()}

    return distribution

def main():
    parser = argparse.ArgumentParser(description='Network Attack Traffic Generator')
    parser.add_argument('--config', type=str, help='Path to configuration JSON file')
    parser.add_argument('--records', type=int, help='Number of records to generate')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    args = parser.parse_args()

    if args.interactive:
        try:
            num_records = int(input("Enter number of records to generate: "))
            distribution = get_user_input_distribution()
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return
    elif args.config:
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
            distribution = config['distribution']
            num_records = config['num_records']
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            return
    else:
        if not args.records:
            print("Either --config, --records, or --interactive must be specified")
            return
        # Use default distribution
        distribution = {
            'ddos_attack_hoic': 0,
            'ddos_attack_loic_http': 0,
            'dos_attack_hulk': 0,
            'bot_activity': 20,
            'ftp_bruteforce': 10,
            'infiltration': 20,
            'dos_attack_slowhttptest': 0,
            'dos_attack_goldeneye': 0,
            'dos_attack_slowloris': 0,
            'brute_force_web': 10,
            'brute_force_xss': 20,
            'sql_injection': 20
        }
        num_records = args.records

    try:
        print("\nGenerating attacks...")
        generator = AttackGenerator(distribution)
        pcap_file = generator.generate_attacks(num_records)
        print(f"\nSuccessfully generated PCAP file: {pcap_file}")
        
        # Save configuration if in interactive mode
        if args.interactive:
            if input("\nWould you like to save this configuration? (y/n): ").lower() == 'y':
                config = {
                    'num_records': num_records,
                    'distribution': distribution
                }
                filename = input("Enter configuration filename (default: attack_config.json): ") or "attack_config.json"
                with open(filename, 'w') as f:
                    json.dump(config, f, indent=4)
                print(f"Configuration saved to {filename}")
                
    except Exception as e:
        print(f"Error generating attacks: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1) 