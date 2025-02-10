try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QLabel, QSpinBox, QPushButton, QMessageBox)
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("\nError: GUI dependencies not available.")
    print("To use the GUI, you need to either:")
    print("\n1. Install PyQt5:")
    print("   pip install PyQt5")
    print("\nOr")
    print("\n2. Use the CLI version instead:")
    print("   python cli.py --interactive")
    print("   python cli.py --config attack_config.json")
    print("   python cli.py --records 1000")
    import sys
    sys.exit(1)

from attack_generator import AttackGenerator
import json
import os

class AttackConfigGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Attack Generator")
        self.setGeometry(100, 100, 800, 600)

        # Attack types and their default percentages
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

        self.spinboxes = {}
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Records input
        records_layout = QHBoxLayout()
        records_label = QLabel("Number of records:")
        self.records_spinbox = QSpinBox()
        self.records_spinbox.setRange(1, 100000)
        self.records_spinbox.setValue(1000)
        records_layout.addWidget(records_label)
        records_layout.addWidget(self.records_spinbox)
        layout.addLayout(records_layout)

        # Attack type inputs
        for attack_type, default_value in self.attack_types.items():
            row_layout = QHBoxLayout()
            label = QLabel(attack_type.replace('_', ' ').title())
            spinbox = QSpinBox()
            spinbox.setRange(0, 100)
            spinbox.setValue(default_value)
            self.spinboxes[attack_type] = spinbox
            row_layout.addWidget(label)
            row_layout.addWidget(spinbox)
            layout.addLayout(row_layout)

        # Generate button
        generate_button = QPushButton("Generate Attack Traffic")
        generate_button.clicked.connect(self.generate_traffic)
        layout.addWidget(generate_button)

    def generate_traffic(self):
        distribution = {attack: spinbox.value() 
                       for attack, spinbox in self.spinboxes.items()}
        total = sum(distribution.values())
        
        if abs(total - 100) > 0.01:
            reply = QMessageBox.question(self, 'Distribution Warning',
                f'Total distribution is {total}%, not 100%. Normalize?',
                QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                factor = 100 / total
                distribution = {k: v * factor for k, v in distribution.items()}
            else:
                return

        try:
            generator = AttackGenerator(distribution)
            pcap_file = generator.generate_attacks(self.records_spinbox.value())
            QMessageBox.information(self, "Success", 
                                  f"Successfully generated PCAP file:\n{pcap_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating attacks: {str(e)}")

def main():
    app = QApplication([])
    window = AttackConfigGUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main() 