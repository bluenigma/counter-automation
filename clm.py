class rd():
    
    def __init__(self, sn, name, date, color_total, black_total):
        self.name = name
        self.sn = sn
        self.date = date
        self.color_total = color_total
        self.black_total = black_total
        print(f'{self.name} instance created')
