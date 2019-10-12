# -*- coding:Utf-8 -*
"""
@author: Thibault de Balthasar
@contact: contact (at) thibaultdebalt [.] fr
@license: GNU GENERAL PUBLIC LICENSE Version 3
"""

import json


class Address(object):
    """
    Will be used to store the detail of an address obtained from the web service

    @type address: String
    @type balance: Float
    @type balanceSat: Double
    @type totalReceived: Float
    @type totalReceivedSat: Double
    @type totalSent: Float
    @type totalSentSat: Double
    @type totalReceivedSat: Double
    @type unconfirmedBalance: Float
    @type unconfirmedBalanceSat: Double
    @type unconfirmedTxAppearances: Int
    @type txAppearances: int
    @type transactions: [String]
    """
    def __init__(self, string_json):
        parsed = json.loads(string_json)
        self.address = parsed["addrStr"]
        self.balance = parsed["balance"]
        self.balanceSat = parsed["balanceSat"]
        self.totalReceived = parsed["totalReceived"]
        self.totalReceivedSat = parsed["totalReceivedSat"]
        self.totalSent = parsed["totalSent"]
        self.totalSentSat = parsed["totalSentSat"]
        self.unconfirmedBalance = parsed["unconfirmedBalance"]
        self.unconfirmedBalanceSat = parsed["unconfirmedBalanceSat"]
        self.unconfirmedTxAppearances = parsed["unconfirmedTxApperances"]
        self.txAppearances = parsed["txApperances"]
        if "transactions" in parsed:
            self.transactions = parsed["transactions"]
        else:
            self.transactions = None

    def __str__(self):
        s = '\n[' + type(self).__name__ + ']\n'
        s += '\n'.join('    {0}:{1}'.format(key, value)
                       for key, value in self.__dict__.items())
        return s


class UnspentOutput(object):
    """
    Will be used to store the unsent outputs of some address
    @type address: String
    @type txid: String
    @type vout: Int
    @type scriptPubKey: String
    @type amount: Float
    @type satoshis: Int
    @type confirmations: Int
    @type ts: Int (Nullable)
    @type height: Int (Nullable)
    """
    def __init__(self, parsed_json):
        self.address = parsed_json['address']
        self.txid = parsed_json['txid']
        self.vout = parsed_json['vout']
        self.scriptPubKey = parsed_json['scriptPubKey']
        self.amount = parsed_json['amount']
        self.satoshis = parsed_json['satoshis']
        self.confirmations = parsed_json['confirmations']
        if "ts" in parsed_json:
            self.ts = parsed_json['ts']
        else:
            self.ts = None
        if "height" in parsed_json:
            self.height = parsed_json["height"]
        else:
            self.height = None

    def __str__(self):
        s = '\n[' + type(self).__name__ + ']\n'
        s += '\n'.join('    {0}:{1}'.format(key, value)
                       for key, value in self.__dict__.items())
        return s
