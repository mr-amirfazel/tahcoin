from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS


from wallet import Wallet
from blockchain import Blockchain


web_app = Flask(__name__)
wallet =  Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(web_app)



@web_app.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('User_Interface', 'node.html')



@web_app.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('User_Interface', 'network.html')

@web_app.route('/wallet',methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'public_key' : wallet.public_key,
            'private_key' : wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response ={
            'message' : 'saving keys failed...'
        }
        return jsonify(response), 500

@web_app.route('/wallet',methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'public_key' : wallet.public_key,
            'private_key' : wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response ={
            'message' : 'Loading keys failed...'
        }
        return jsonify(response), 500


@web_app.route('/chain',methods=['GET'])
def get_chain():
    chain = blockchain.chain
    chain_to_dict = [block.__dict__.copy() for block in chain]
    for dict_block in chain_to_dict:
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
    return jsonify(chain_to_dict), 200



@web_app.route('/mine',methods=['POST'])
def mine_block():
    block = blockchain.mine_block()
    if block != None:
            dict_block = block.__dict__.copy()
            dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
            response = {
                'message' : 'Block added Successfully',
                'block' : dict_block,
                'funds' : blockchain.get_balance()
            }
            return jsonify(response), 201
       
    else:
        response = {
                'message' : 'Mining block failed...',
                'wallet_set_up' : wallet.public_key != None
            }
        return jsonify(response), 500
            

@web_app.route('/balance',methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            'message' : 'fetched balance successfully',
            'funds':balance
        }
        return jsonify(response), 200
    else:
        response = {
            'message' : 'loading balance failed.',
            'wallet_set_up' : wallet.public_key != None
        }
        return jsonify(response), 500

@web_app.route('/transactions',methods=['GET'])
def get_open_transaction():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions), 200


@web_app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = {
            'message': 'No wallet set up.'
        }
        return jsonify(response), 400
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Required data is missing.'
        }
        return jsonify(response), 400
    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)
    if success:
        response = {
            'message': 'Successfully added transaction.',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Creating a transaction failed.'
        }
        return jsonify(response), 500

   
   
@web_app.route('/node',methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message' : 'Some Data missing'
        }
        return jsonify(response), 400
    if 'node' not in values:
        response = {
            'message' : 'Node Data missing'
        }
        return jsonify(response), 400
    node = values['node']
    blockchain.add_peer_node(node)
    response = {
        'message': 'Node added successfully!',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201

@web_app.route('/node/<node_URL>',methods=['DELETE'])
def remove_node(node_URL):
    if node_URL == '' or node_URL == None:
        response = {
            'message': 'Node not found :('
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_URL)
    response = {
        'message' : 'Node removed successfully :)',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200

@web_app.route('/node',methods=['GET'])
def get_nodes():
    all_nodes = blockchain.get_peer_nodes()
    response = {
        'all_nodes': all_nodes
    }
    return jsonify(response), 200

if __name__ == '__main__':
    web_app.run(host='0.0.0.0', port=5000)