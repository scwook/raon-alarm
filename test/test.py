class TEST:
    def __init__(self, value):
        self.value = value

    @classmethod
    def getValue(cls):
        return cls
    

c = TEST(10)
print(c.getValue().value)