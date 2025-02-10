import tkinter as tk
from tkinter import ttk, messagebox
import json
from attack_generator import AttackGenerator

class AttackConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Attack Generator")
        self.root.geometry("800x600")

        # Attack types and their default percentages from attack.py
        self.attack_types = {
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

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Number of records
        ttk.Label(main_frame, text="Number of Records:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.records_var = tk.StringVar(value="1000")
        ttk.Entry(main_frame, textvariable=self.records_var).grid(row=0, column=1, sticky=tk.W, pady=5)

        # Attack distribution frame
        attack_frame = ttk.LabelFrame(main_frame, text="Attack Distribution (%)", padding="5")
        attack_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        # Create entry fields for each attack type
        self.attack_vars = {}
        for i, (attack_type, default_value) in enumerate(self.attack_types.items()):
            row = i // 2
            col = i % 2 * 2

            # Create a nicer label from the attack type
            label_text = attack_type.replace('_', ' ').title()
            ttk.Label(attack_frame, text=label_text).grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
            
            var = tk.StringVar(value=str(default_value))
            self.attack_vars[attack_type] = var
            ttk.Entry(attack_frame, textvariable=var, width=10).grid(row=row, column=col+1, sticky=tk.W, padx=5, pady=2)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Validate", command=self.validate_distribution).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Generate Attacks", command=self.generate_attacks).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Save Config", command=self.save_config).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Load Config", command=self.load_config).grid(row=0, column=3, padx=5)

    def validate_distribution(self):
        try:
            total = sum(float(var.get()) for var in self.attack_vars.values())
            if abs(total - 100) > 0.01:  # Allow for small floating-point differences
                messagebox.showerror("Error", f"Distribution total must be 100%. Current total: {total}%")
                return False
            return True
        except ValueError:
            messagebox.showerror("Error", "All percentages must be valid numbers")
            return False

    def generate_attacks(self):
        if not self.validate_distribution():
            return

        try:
            num_records = int(self.records_var.get())
            if num_records <= 0:
                raise ValueError("Number of records must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid number of records")
            return

        # Create attack distribution dictionary
        distribution = {attack: float(var.get()) for attack, var in self.attack_vars.items()}

        try:
            generator = AttackGenerator(distribution)
            generator.generate_attacks(num_records)
            messagebox.showinfo("Success", "Attacks generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate attacks: {str(e)}")

    def save_config(self):
        config = {
            'num_records': self.records_var.get(),
            'distribution': {attack: var.get() for attack, var in self.attack_vars.items()}
        }
        
        try:
            with open('attack_config.json', 'w') as f:
                json.dump(config, f, indent=4)
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")

    def load_config(self):
        try:
            with open('attack_config.json', 'r') as f:
                config = json.load(f)
                
            self.records_var.set(config['num_records'])
            for attack, value in config['distribution'].items():
                if attack in self.attack_vars:
                    self.attack_vars[attack].set(value)
                    
            messagebox.showinfo("Success", "Configuration loaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved configuration found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttackConfigGUI(root)
    root.mainloop() 