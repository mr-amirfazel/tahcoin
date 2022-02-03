import re
from urllib import response
from flask import Flask, jsonify
from flask_cors import CORS


from wallet import Wallet
from blockchain import Blockchain


web_app = Flask(__name__)
wallet =  Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(web_app)


@web_app.route('/', methods=['GET'])
def get_ui():
    return 'this works!'

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
                'block' : dict_block
            }
            return jsonify(response), 201
       
    else:
        response = {
                'message' : 'Mining block failed...',
                'wallet_set_up' : wallet.public_key != None
            }
        return jsonify(response), 500
            



if __name__ == '__main__':
    web_app.run(host='0.0.0.0', port=5000)