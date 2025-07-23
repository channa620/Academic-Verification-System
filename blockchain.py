import json
import time
import re
import js

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
        import hashlib
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
            return "✅ Block added successfully!"
        else:
            self.invalid_blocks.append(data)
            return "❌ Invalid block! USN format or other field is incorrect."

    def validate_data(self, data):
        required_fields = ['name', 'degree', 'year', 'usn']
        if not all(k in data for k in required_fields):
            return False
        if not data['name'].strip() or not data['degree'].strip():
            return False
        if not str(data['year']).isdigit() or not (1900 <= int(data['year']) <= 2100):
            return False
        usn_pattern = r'^1HK[0-9]{2}[A-Z]{2}[0-9]{3}$'
        if not re.match(usn_pattern, data['usn'].strip().upper()):
            return False
        return True

    def is_valid(self):
        for i in range(1, len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i-1]
            if cur.hash != cur.calculate_hash() or cur.prev_hash != prev.hash:
                return False
        return True

    def display_chain(self):
        output = "\n📜 Valid Blockchain Ledger:\n\n"
        for block in self.chain:
            output += f"Index: {block.index}\n"
            output += f"Timestamp: {time.ctime(block.timestamp)}\n"
            output += f"Data: {json.dumps(block.data, indent=2)}\n"
            output += f"Hash: {block.hash}\n"
            output += f"Previous Hash: {block.prev_hash}\n"
            output += "-" * 60 + "\n"
        return output

    def display_invalid_blocks(self):
        if self.invalid_blocks:
            output = "\n🚫 Invalid Blocks:\n\n"
            for i, data in enumerate(self.invalid_blocks, 1):
                output += f"[{i}] {json.dumps(data, indent=2)}\n"
            return output
        else:
            return "\n✅ No invalid blocks detected."

blockchain = Blockchain()
