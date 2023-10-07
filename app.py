from flask import Flask, request, jsonify
import hashlib
import json
import time

app = Flask(__name__)

# Define the structure of a block
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

# Initialize the blockchain with a genesis block
blockchain = []
genesis_block = Block(0, "0", int(time.time()), "Genesis Block", "0")
blockchain.append(genesis_block)

# Function to calculate the hash of a block
def calculate_hash(block):
    block_string = json.dumps(block.__dict__, sort_keys=True)
    return hashlib.sha256(block_string.encode()).hexdigest()

# Function to add a new block to the blockchain
def add_block(data):
    previous_block = blockchain[-1]
    new_index = previous_block.index + 1
    new_timestamp = int(time.time())
    new_hash = calculate_hash(Block(new_index, previous_block.hash, new_timestamp, data, ""))
    new_block = Block(new_index, previous_block.hash, new_timestamp, data, new_hash)
    blockchain.append(new_block)

# Function to validate the integrity of the blockchain
def is_valid_chain():
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]

        if current_block.previous_hash != calculate_hash(previous_block):
            return False

    return True

# Endpoint to add data to the blockchain
@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()
    add_block(data)
    response = {'message': 'Data added to the blockchain successfully.'}
    return jsonify(response), 201

# Endpoint to retrieve the entire blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': [block.__dict__ for block in blockchain],
        'length': len(blockchain)
    }
    return jsonify(response), 200

# Main
if __name__ == '__main__':
    app.run(host='localhost', port=5000)
