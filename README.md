# Tahcoin
I made my own crypto-coin **tahcoin** , using python 

## Aims & Goals ##
1. Learn Python
2. Increase my knowledge about Blockchain

## clientside webpage screenshots ##
the front end UI may change in future 
![wallet_and_node](https://user-images.githubusercontent.com/78591315/152568946-1d947125-c457-4715-90cd-130050652dc4.png)
![node_network](https://user-images.githubusercontent.com/78591315/152568988-0156ad2e-b8fc-41f5-b6a0-db19113193fc.png)

# How to Use #
### Install these libraries ###
- Cryptography
- flask
- flask_cors
- requests
## Run app ##
- download or clone the repository
- run the node.py file using python and using this command:
    `python node.py -p <port_number>`
    <br>
 **use an unoccupied  port number**
    <br>
 **the defualt port number is 5000**
 
# Brief Description #
- Built a REST API using Flask
- Also created clientside UI using jinja,bootstrap & a little bit of vue
- Like other cryptocurrencies you can mine, add transaction, handle wallet, ...
- as the blockchain technology requires this coin contains, hashing via sha256, proof of work, public & private keys, signatues, ...
- to not lose the track of transactions and mined blocks every data is saved in your disc in the `wallet.txt` and `blockchain.txt` file so be sure to delete them if they're cloned with other files,so you could have your own keys 
- ### wish you Luck ### 

## Sourcs and tips ## 

This is the [Source](https://www.udemy.com/course/learn-python-by-building-a-blockchain-cryptocurrency/ "source") I used to learn python and blockchain basics from.
   <br>
To develop knowlege about the blockchain technology , this [Book](https://www.goodreads.com/book/show/36189173-blockchain) is recommended.
