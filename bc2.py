import hashlib
import json
import time
import re

class Block:
    def __init__(self, index, data, prev_hash):
        self.timestamp = time.time()
        self.index = index
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "timestamp": self.timestamp,
            "index": self.index,
            "data": self.data,
            "prev_hash": self.prev_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.invalid_blocks = []

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def add_block(self, data):
        if self.validate_data(data):
            prev_block = self.chain[-1]
            new_block = Block(len(self.chain), data, prev_block.hash)
            self.chain.append(new_block)
            print("✅ Block added successfully!")
        else:
            print("❌ Invalid block! USN format or other field is incorrect.")
            self.invalid_blocks.append(data)

    def validate_data(self, data):
        # Basic checks
        required_fields = ['name', 'degree', 'year', 'usn']
        if not all(k in data for k in required_fields):
            return False
        if not data['name'].strip() or not data['degree'].strip():
            return False
        if not str(data['year']).isdigit() or not (1900 <= int(data['year']) <= 2100):
            return False
        # USN format validation (example: 1DA20EC001)
        usn_pattern = r'^1HK[0-9]{2}[A-Z]{2}[0-9]{3}$'
        if not re.match(usn_pattern, data['usn'].strip().upper()):
            return False
        return True

    def is_valid(self):
        for i in range(1, len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i - 1]
            if cur.hash != cur.calculate_hash() or cur.prev_hash != prev.hash:
                return False
        return True

    def display_chain(self):
        print("\n📜 Valid Blockchain Ledger:\n")
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {time.ctime(block.timestamp)}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.prev_hash}")
            print("-" * 60)

    def display_invalid_blocks(self):
        if self.invalid_blocks:
            print("\n🚫 Invalid Blocks:\n")
            for i, data in enumerate(self.invalid_blocks, 1):
                print(f"[{i}] {data}")
        else:
            print("\n✅ No invalid blocks detected.")

# ✅ Main program
if __name__ == "__main__":
    bc = Blockchain()

    print("🔐 Student Certificate Blockchain with USN Validation")

    while True:
        print("\nEnter certificate details:")
        name = input("Name: ").strip()
        degree = input("Degree: ").strip()
        year = input("Year: ").strip()
        usn = input("USN : ").strip().upper()

        cert_data = {
            "name": name,
            "degree": degree,
            "year": year,
            "usn": usn
        }

        bc.add_block(cert_data)

        cont = input("Do you want to add another certificate? (y/n): ").lower()
        if cont != 'y':
            break

    bc.display_chain()
    bc.display_invalid_blocks()
    print("\n🔒 Blockchain Validity:", "✅ Valid" if bc.is_valid() else "❌ Invalid")


