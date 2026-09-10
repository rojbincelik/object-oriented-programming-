class Config():
    cng=None
    def __new__(cls,db_url,debug):
        
        if cls.cng is None:
            cls.cng=super().__new__(cls)
            cls.cng.db_url=db_url
            cls.cng.debug=debug
        return cls.cng
config1=Config("sqlite:///school.db" ,True)
config2=Config("mysql:///instance/class.db",False)
print(config1.db_url,config1.debug)
print(config2.db_url,config2.debug)
print(config1 is config2)
print(id(config1), id(config2))