import os
import json
from web3 import Web3, HTTPProvider
from web3.auto import w3
from flask import Flask, redirect, render_template
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

x = open(os.getenv("ABI_PATH"), 'r').read()
abi = json.loads(x)
web3 = Web3(HTTPProvider(os.getenv("PROVIDER_URL")))
contract = web3.eth.contract(
    address=Web3.toChecksumAddress(os.getenv("CONTRACT_ADDRESS")),
    abi=abi,
)

@app.route("/<short>")
def respond(short):
    short = Web3.toBytes(hexstr=short) if short.startswith("0x") else Web3.toBytes(text=short)
    destination, paid = contract.functions.getURL(short).call()
    if not paid:
        return render_template("pre_redirect.html", destination=destination)
    return redirect(destination if destination != 'FAIL' else '/') 