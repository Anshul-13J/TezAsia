import smartpy as sp

class Playground(sp.Contract):
    def __init__(self):
        #storage
        self.init(
            num_1 = sp.nat(5),
            num_2 = sp.int(-4),
            admin = sp.test_account("admin").address,
            map_1 = sp.map(l = {}, tkey = sp.TNat, tvalue = sp.TAddress),
            time = sp.timestamp(25),
            map_2 = sp.big_map(l = {}, tkey = sp.TNat, tvalue = sp.TAddress),
        )

    @sp.entry_point
    def changeNumValues(self,params):
        sp.set_type(params, sp.TRecord(num_a = sp.TNat , num_b = sp.TInt))

        #Using an assertion
        sp.verify(sp.sender == self.data.admin , "NOT AUTHORIZED")
        sp.verify(sp.now > self.data.time, "INCORRECT TIMING")

        #assignment
        self.data.num_1 = params.num_a
        
        #Condition check
        sp.if params.num_b > 0:
            self.data.num_2 = params.num_b
        sp.else:
            self.data.num_2 = params.num_b * -1
            self.data.num_2 = params.num_b


    @sp.entry_point
    def changeMapValue(self,num):
        sp.set_type(num, sp.TNat)
        
        self.data.map_1[num] = sp.sender
        self.data.map_2[num] = sp.sender

@sp.add_test(name = "main")
def test():
    scenario  =sp.test_scenario()

    #Testing account

    alice = sp.test_account("alice")
    bob = sp.test_account("bob")
    admin = sp.test_account("admin")

    playground = Playground()

    #Important part
    scenario += playground

    #calling changeNumValues()

    scenario += playground.changeNumValues(num_a = sp.nat(2), num_b = sp.int(-3)).run(
        sender = admin, now = sp.timestamp(26)
    )
    scenario += playground.changeNumValues(num_a = sp.nat(2), num_b = sp.int(-3)).run(
        sender = bob, now = sp.timestamp(26), valid = False
    )

    scenario += playground.changeNumValues(num_a = sp.nat(2), num_b = sp.int(-3)).run(
        sender = admin, now = sp.timestamp(23),valid = False
    )

    #calling ChangeMapValues()
    scenario += playground.changeMapValue(5).run(sender = alice)
    scenario += playground.changeMapValue(1).run(sender = alice)
