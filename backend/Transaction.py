'''
Transaction class for parsing bank transaction file lines.
'''

class Transaction:
    code = {
        "01" : "withdrawal",
        "02" : "transfer",
        "03" : "paybill",
        "04" : "deposit",
        "05" : "create",
        "06" : "delete",
        "07" : "disable",
        "08" : "changeplan",
        "00":  "end_session"
    }
    def __init__(self, code, name, account_num, amount, misc):
        self.code = code
        self.name = name
        self.account_num = account_num
        self.amount = amount
        self.misc = misc

def from_line(line):
    '''
    Parses a 40-character transaction line and returns Transaction object.
    '''

    code = line[0:2]
    name = line[3:23]
    account_num = int(line[24:29])
    amount = float(line[30:38])
    misc = line[39:41]

    return Transaction(code, name, account_num, amount, misc)


