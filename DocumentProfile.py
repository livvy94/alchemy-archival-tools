#import json

class DocumentProfile:
    def __init__(self, ein, returntype, state, subcode, subdate, taxyear, taxpayername, totalassets, zipcode):
        self.ein = ein
        self.returntype = returntype
        self.state = state
        self.subcode = subcode
        self.subdate = subdate
        self.taxyear = taxyear
        self.taxpayername = taxpayername
        self.totalassets = totalassets
        self.zipcode = zipcode

    #def toJSON(self):
    #    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)