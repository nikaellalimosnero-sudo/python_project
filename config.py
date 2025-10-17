class AppConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        # Database Configuration
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = ""
        self.db_name = "traffic_violation"
        
        # Authentication
        self.login_username = "admin"
        self.login_password = "admin123"
        
        # Field Configuration
        self.int_fields = ["Year"]
        self.numeric_fields = ["Penalty Amount"]  
        self.columns = ("ID","Plate Number","Driver Name","Description","Belts","Personal Injury","Property Damage",
                       "Commercial License","Commercial Vehicle","State","Vehicle Type","Year","Make","Model","Color",
                       "Charge","Penalty Amount","Contributed To Accident","Race","Gender","Driver City","Driver State",
                       "DL State","Arrest Type","Violation Type")
        
        # UI Colors
        self.colors = {
            'dark': "#17252A",
            'teal': "#2B7A78",
            'light_teal': "#3AAFA9",
            'light_cyan': "#DEF2F1",
            'white': "#FEFFFF"
        }

