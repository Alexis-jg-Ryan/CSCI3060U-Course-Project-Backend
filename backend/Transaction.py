'''
Transaction class for parsing bank transaction file lines.
'''

class Transaction:
    code = {
        "01" : "withdraw",
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

    @classmethod
    def from_line(cls, line):
        '''
        Parses a 40-character transaction line and returns Transaction object.
        '''

        code = line[0:2].strip()
        name = line[3:23].strip()
        account_num = int(line[24:29].strip())
        amount = float(line[30:38].strip())
        misc = line[39:41].strip()

        return cls(code, name, account_num, amount, misc)