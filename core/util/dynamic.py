import os.path
import json
from .util import Util

atomic = 100000000


class Dynamic:
    def __init__(self, u, msg, network, port):
        self.username = u
        self.msg = msg
        self.network = network
        self.port = port
        self.u = Util(self.network)
        self.client = self.u.get_client(self.port)
        
    
    def calculate_dynamic_fee(self, t, s, c):
        fee = int((t + s) * c)
        return fee

    
    def get_multipay_limit(self):
        try:
            limit = int(self.client.node.configuration()['data']['constants']['multiPaymentLimit'])
        except:
            limit = 20
        return limit
    
    
    def calculate_dynamic_multifee(self, t, s, c):
        fee = int((t + (round(s/2) + 1)) * c)
        return fee
    
    
    def get_dynamic_fee_multi(self, numtx):
        try:
            node_configs = self.client.node.configuration()['data']['transactionPool']['dynamicFees']
            if (node_configs['enabled'] == "False"):
                transaction_fee = int(0.1 * atomic)
            else:
                dynamic_offset = node_configs['addonBytes']['multiPayment']
                fee_multiplier = node_configs['minFeePool']
                
                # get size of transaction
                multi_tx = 125
                second_sig = 64
                per_tx_fee = 29
                v_msg = len(self.msg) 
                print("vendor length", v_msg)
                tx_size = multi_tx + v_msg + second_sig + (numtx * per_tx_fee)
                print("dynamic offset", dynamic_offset)
                print("transaction size", tx_size)
                print("fee multiplier", fee_multiplier)
                
                # calculate transaction fee
                transaction_fee = self.calculate_dynamic_multifee(dynamic_offset, tx_size, fee_multiplier)
                #transaction_fee = self.calculate_dynamic_fee(dynamic_offset, tx_size, fee_multiplier)
                print("calculated transaction fee", transaction_fee)
         
        except:
            transaction_fee = int(0.1 * atomic)
            
        return transaction_fee
    
    
    def get_dynamic_fee(self):        
        try:
            node_configs = self.client.node.configuration()['data']['transactionPool']['dynamicFees']
            if (node_configs['enabled'] == "False"):
                transaction_fee = int(0.1 * atomic)
            else:
                dynamic_offset = node_configs['addonBytes']['transfer']
                fee_multiplier = node_configs['minFeePool']
                
                # get size of transaction - S
                standard_tx = 230
                v_msg = len(self.msg) 
                tx_size = standard_tx + v_msg
                
                # calculate transaction fee
                transaction_fee = self.calculate_dynamic_fee(dynamic_offset, tx_size, fee_multiplier)
        except:
            transaction_fee = int(0.1 * atomic)

        return transaction_fee
