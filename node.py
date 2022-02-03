from flask import Flask
from flask_cors import CORS


from wallet import Wallet

web_app = Flask(__name__)
wallet =  Wallet()
CORS(web_app)


@web_app.route('/', methods=['GET'])
def get_ui():
    return 'this works!'

if __name__ == '__main__':
    web_app.run(host='0.0.0.0', port=5000)