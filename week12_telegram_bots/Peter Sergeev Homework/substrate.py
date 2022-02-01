import substrateinterface as sub
from telebot import TeleBot
from threading import Thread
from mysubstratedb import writeData

# TG bot key
bot = TeleBot('KEY')
# set of users who will receive blockchain updates
ids = dict()


# handle subscription
def subscription_handler(obj, update_nr, subscription_id):
    
    # Retrieve transactions in block
    result = substrate.get_block(block_number=obj['header']['number'])
    parse_data(result)

    # for later use, currently use 100 for testing
    if update_nr > 100:
        return {'message': 'Subscription will cancel when a value is returned', 'updates_processed': update_nr}
           

# parse block data
def parse_data(result):
    data = dict()

    for extrinsic in result['extrinsics']:

        if extrinsic.value["call"]["call_module"] in ['Crowdloan', 'Balances']:

            if 'address' in extrinsic.value:
                signed_by_address = extrinsic.value['address']
            else:
                signed_by_address = None

            data['Pallet'] = extrinsic.value["call"]["call_module"]
            data['Call'] = extrinsic.value["call"]["call_function"]
            data['Signature'] = signed_by_address

            # Loop through call params
            for param in extrinsic.value["call"]['call_args']:

                if param['type'] == 'Balance' or param['type'] == 'BalanceOf':
                    #param['value'] = '{:.2f} {}'.format(param['value'] / 10 ** substrate.token_decimals, substrate.token_symbol)
                    data['Amount'] = param['value'] / 10 ** substrate.token_decimals

                elif param['type'] == 'LookupSource' or param['type'] == 'ParaId':
                    data['Dest'] = param['value']
                
            writeData(data)
            
            # send messages if user threshold is met. 
            if data['Pallet'] == 'Balances':
                s = '{:.2f} DOT were transferred to account {}'.format(data['Amount'], data['Dest'])
                print(s)
                for id, threshold in ids.items():
                    if data['Amount'] >= threshold:
                        bot.send_message(id, s)

            elif data['Pallet'] == 'Crowdloan':
                s = '{:.2f} DOT were contributed to parachain_id {}'.format(data['Amount'], data['Dest'])
                print(s)
                for id, threshold in ids.items():
                    if data['Amount'] >= threshold:
                        bot.send_message(id, s)
    
    
# bot functions
@bot.message_handler(commands=['start'])
def save_id(message):
    
    # ids.add(message.from_user.id) 
    # # add key to a dict
    ids[message.from_user.id] = 0
    print(ids)
    sent = bot.send_message(message.from_user.id, 'Hi, this is a polkadot blockchain bot\
        which reads realtime transfers and crowdloan contributions from the blockchain')
    sent = bot.send_message(message.from_user.id, 'Please input desired threshold for native currency amount (DOT) in decimals')
    bot.register_next_step_handler(sent, threshold)


def threshold(message):
    try: 
        float(message.text)
    except ValueError:
        sent = bot.send_message(message.from_user.id, 'I asked for a number... Tyr one more time')
        bot.register_next_step_handler(sent, threshold)

    # t.append(float(message.text))
    ids[message.from_user.id] = float(message.text)
    bot.send_message(message.from_user.id, 'Subscribing to block headers...')


@bot.message_handler(commands=['stop'])
def stop(message):
    ids.pop(message.from_user.id, None)
    bot.send_message(message.from_user.id, 'Done, you will now stop receiveing blockchain updates')


if __name__ == '__main__':

    # threshold
    # t = [0]

    # node connection
    substrate = sub.SubstrateInterface(
        url="wss://rpc.polkadot.io",
        ss58_format=0,
        type_registry_preset='substrate-node-template'
    )
    print("substrate initialized")

    # create threade for node connection. 
    thread = Thread(target = substrate.subscribe_block_headers, args=(subscription_handler, ))
    thread.start()
    print("Thread created")
    bot.infinity_polling()

    

# tbd: batch transactions
'''
# multiple calls in one transaction (not available atm)

    if param['type'] == 'Vec<Call>': 
        for j in param['value']:
            print 
            for k in j['call_args']:
                if k['type'] == 'Balance' or k['type'] == 'ParaId':
                    k['value'] = '{} {}'.format(k['value'] / 10 ** substrate.token_decimals, substrate.token_symbol)
                print("{}: {}".format(k['name'], k['value']))
    else:
        print("{}: {}".format(param['name'], param['value']))


a = [{'call_index': '0x0001', 'call_function': 'remark', 'call_module': 'System', 'call_args': [{'name': 'remark', 'type': 'Bytes', 'value': '2031#0x4439fba228ad9a1c73af384af7119782123aa6f6d55592f07bf82da5b919c0c7'}], 'call_hash': '0x602962dc0688f843a855b3ab0891506a9f8de0d555bbb6cdef2113577498b829'}, {'call_index': '0x0500', 'call_function': 'transfer', 'call_module': 'Balances', 'call_args': [{'name': 'dest', 'type': 'LookupSource', 'value': '13wNbioJt44NKrcQ5ZUrshJqP7TKzQbzZt5nhkeL4joa3PAX'}, {'name': 'value', 'type': 'Balance', 'value': 60000000000}], 'call_hash': '0x8684d51fda246d58daad60a8b4ce094bbbb468b28279810f38bf65ed2474a76b'}] 
for x in a:
    # print(x['call_args'])
    for y in x['call_args']:
        if y['type'] == 'Balance':
            y['value'] = '{} {}'.format(y['value'] / 10 ** substrate.token_decimals, substrate.token_symbol)
        print (y['value'])
'''       
