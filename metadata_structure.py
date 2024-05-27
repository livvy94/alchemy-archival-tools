class record:
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

class recordtype2:
    def __init__(self, ein, taxyear, taxpayername, state, zipcode, returntype, subcode, totalassets, subdate): # this line being a different order is what fixed it
        self.ein = ein
        self.taxyear = taxyear
        self.taxpayername = taxpayername
        self.state = state
        self.zipcode = zipcode
        self.returntype = returntype
        self.subcode = subcode
        self.totalassets = totalassets
        self.subdate = subdate
