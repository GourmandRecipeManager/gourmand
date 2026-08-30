from gourmand import convert, shopping


class DatabaseShopper(shopping.Shopper):
    """We are a Shopper class that conveniently saves our key dictionaries
    in our database"""

    def __init__(self, lst, db, conv=None):
        self.db = db
        self.cnv = conv
        shopping.Shopper.__init__(self, lst)

    def init_converter(self):
        if not self.cnv:
            self.cnv = convert.get_converter()

    def init_orgdic(self):
        from .backends.db import dbDic
        self.orgdic = dbDic("ingkey", "shopcategory", self.db.shopcats_table, db=self.db)
        if len(list(self.orgdic.items())) == 0:
            dic = shopping.setup_default_orgdic()
            self.orgdic.initialize(dic)

    def init_ingorder_dic(self):
        from .backends.db import dbDic
        self.ingorder_dic = dbDic("ingkey", "position", self.db.shopcats_table, db=self.db)

    def init_catorder_dic(self):
        from .backends.db import dbDic
        self.catorder_dic = dbDic("shopcategory", "position", self.db.shopcatsorder_table, db=self.db)

    def init_pantry(self):
        from .backends.db import dbDic
        self.pantry = dbDic("ingkey", "pantry", self.db.pantry_table, db=self.db)
        if len(self.pantry.items()) == 0:
            self.pantry.initialize(dict([(i, True) for i in self.default_pantry]))
