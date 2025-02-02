# -*- coding:Utf-8 -*
"""
@author: Thibault de Balthasar
@contact: contact (at) thibaultdebalt [.] fr
@license: GNU GENERAL PUBLIC LICENSE Version 3
"""

import json
import datetime
from decimal import Decimal
from .utils import satoshi_to_bitcoin, bitcoin_to_satoshi


class TransactionInput(object):
    """
    Will contain the input of a transaction.
    @type txid: String
    @type vout: int
    @type scriptSigAsm: String
    @type scriptSigHex: String
    @type sequence: int
    @type n: int
    @type addr: string
    @type valueSat: int
    @type value: Float
    @type doubleSpentTxID: nullable (string ?)
    """
    def __init__(self, parsed_json):
        if 'coinbase' in parsed_json.keys():
            self.coinbase = parsed_json['coinbase']
            self.sequence = parsed_json['sequence']
            self.n = parsed_json['n']
        else:
            self.txid = parsed_json["txid"]
            self.vout = parsed_json["vout"]
            self.sequence = parsed_json["sequence"]
            self.n = parsed_json["n"]
            self.addr = parsed_json["addr"]
            self.valueSat = parsed_json["valueSat"]
            # self.value = parsed_json["value"]
            self.value = satoshi_to_bitcoin(parsed_json["valueSat"])
            self.doubleSpentTxID = parsed_json["doubleSpentTxID"]
            self.scriptSigAsm = parsed_json["scriptSig"]["asm"]
            self.scriptSigHex = parsed_json["scriptSig"]["hex"]

    def is_coinbase(self):
        return hasattr(self, 'coinbase')

    def __str__(self):
        s = '\n[' + type(self).__name__ + ']\n'
        s += '\n'.join('    {0}:{1}'.format(key, value)
                       for key, value in self.__dict__.items())
        return s


class TransactionOutput(object):
    """
    Will be used to store the outputs of a transaction.

    @type value: Float
    @type n: int
    @type spentTxId: String
    @type spentIndex: int
    @type spentHeight: int
    @type scriptPubKey: TransactionOutput.ScriptPublicKey
    """
    def __init__(self, parsed_json):
        self.value = Decimal(parsed_json["value"])
        self.valueSat = bitcoin_to_satoshi(Decimal(parsed_json["value"]))
        self.n = parsed_json["n"]
        self.spentTxId = parsed_json["spentTxId"]
        self.spentIndex = parsed_json["spentIndex"]
        self.spentHeight = parsed_json["spentHeight"]
        self.scriptPubKey = TransactionOutput.ScriptPublicKey(
            parsed_json["scriptPubKey"])

    class ScriptPublicKey(object):
        """
        To store the scriptPubKey
        @type hex: String
        @type asm: String
        @type addresses = [String]
        @type type: String
        """
        def __init__(self, parsed_json):
            self.hex = parsed_json["hex"]
            self.asm = parsed_json["asm"]
            if 'addresses' in parsed_json.keys():
                self.addresses = parsed_json["addresses"]
            if 'type' in parsed_json.keys():
                self.type = parsed_json["type"]

    def include_address(self):
        return hasattr(self.scriptPubKey, 'addresses')

    def __str__(self):
        s = '\n[' + type(self).__name__ + ']\n'
        s += '\n'.join('    {0}:{1}'.format(key, value)
                       for key, value in self.__dict__.items())
        return s


class Transaction(object):
    """
    Will be used to store the details of a transaction

    @type txid: String
    @type version: int
    @type lockTime: int
    @type blockHeight: int
    @type confirmations: int
    @type time: datetime
    @type valueOut: Float
    @type size: int
    @type valueIn: Float
    @type fees: Float
    @type inputs: [Input]
    @type outputs: [Output]
    """
    def __init__(self, string_json, already_parsed=False):
        """
        :param string_json: The string to parse
        :param already_parsed: If the json has already been parsed and a dictionary is given as a first argument \
        instead of a string
        """
        if already_parsed:
            parsed = string_json
        else:
            parsed = json.loads(string_json)
        self.txid = parsed["txid"]
        self.version = parsed["version"]
        self.lockTime = parsed["locktime"]
        if 'blockhash' in parsed.keys():
            # if confirmed
            self.blockHash= parsed["blockhash"]
        else:
            self.blockHash = ""
        # -1 if not confirmed
        self.blockHeight = parsed["blockheight"]
        # 0 if not confirmed
        self.confirmations = parsed["confirmations"]
        self.time = datetime.datetime.fromtimestamp(parsed['time'])
        self.size = parsed["size"]

        self.inputs = []
        self.outputs = []

        for item in parsed["vout"]:
            self.outputs.append(TransactionOutput(item))
        for item in parsed["vin"]:
            self.inputs.append(TransactionInput(item))

        # abandon for precision
        #if 'fees' in parsed.keys():
        #    self.fees = parsed["fees"]
        #else:
        #    self.fees = 0
        #
        #self.valueOut = parsed["valueOut"]
        #if 'valueIn' in parsed.keys():
        #    self.valueIn = parsed["valueIn"]
        self.feesSat, self.valueInSat, self.valueOutSat = self.recalculate()
        self.fees, self.valueIn, self.valueOut = satoshi_to_bitcoin(self.feesSat), satoshi_to_bitcoin(self.valueInSat), satoshi_to_bitcoin(self.valueOutSat)


    def recalculate(self):
        value_in_sat = 0
        value_out_sat = 0
        for inp in self.inputs:
            if not inp.is_coinbase():
                value_in_sat += inp.valueSat
        for out in self.outputs:
            if out.include_address():
                value_out_sat += out.valueSat

        if self.inputs[0].is_coinbase():
            # coinbase
            return 0, 0, value_out_sat
        else:
            # not coinbase
            fee_unit = value_in_sat - value_out_sat
            return fee_unit, value_in_sat, value_out_sat

    def gain_for_address(self, address):
        """
        This method allows to get the gain of a specific address for this transaction
        @param address: The bitcoin address we wish to get details about
        @type address: String
        @return: The sum gained or lost
        @rtype: Float
        """
        total = 0
        for inp in self.inputs:
            if not inp.is_coinbase() and inp.addr == address:
                total -= inp.value
        for out in self.outputs:
            if out.include_address() and address in out.scriptPubKey.addresses:
                total += out.value
        return total

    def __str__(self):
        s = '\n[' + type(self).__name__ + ']\n'
        s += '\n'.join('    {0}:{1}'.format(key, value)
                       for key, value in self.__dict__.items())
        return s
