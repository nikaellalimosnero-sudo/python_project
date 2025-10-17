from config import AppConfig
from tkinter import messagebox
from database import TrafficViolationRepository


class ValidationService:
    
    def __init__(self):
        self.config = AppConfig()
    
    def validate_empty_fields(self, entries, labels):
        for i, ent in enumerate(entries):
            if not ent.get().strip():
                messagebox.showerror("Validation Error", f"Please fill in the field: {labels[i]}")
                return False
        return True
    
    def validate_data_types(self, entries, labels):
        for i, label in enumerate(labels):
            value = entries[i].get().strip()
            
            # Check strictly integer fields
            if label in self.config.int_fields:
                if not self._is_valid_integer(value):
                    messagebox.showerror("Validation Error", f"{label} must be a valid integer number")
                    return False
            
            # Check numeric fields (can be integer or decimal)
            elif label in self.config.numeric_fields:
                if not self._is_valid_numeric(value):
                    messagebox.showerror("Validation Error", f"{label} must be a valid number")
                    return False
        
        return True
    
    def validate_record_fields(self, entries, labels):
        return (self.validate_empty_fields(entries, labels) and 
                self.validate_data_types(entries, labels))
    
    def _is_valid_integer(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    def _is_valid_numeric(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False


class AuthenticationService:
    
    def __init__(self):
        self.config = AppConfig()
    
    def authenticate(self, username, password):
        return (username == self.config.login_username and 
                password == self.config.login_password)


class TrafficViolationService:
    def __init__(self):
        self.repository = TrafficViolationRepository()
        self.validator = ValidationService()
    
    def get_all_violations(self):
        return self.repository.get_all()
    
    def search_violations(self, search_term):
        return self.repository.search(search_term)
    
    def create_violation(self, entries, labels):
        if not self.validator.validate_record_fields(entries, labels):
            return False
        
        values = tuple(ent.get().strip() for ent in entries)
        return self.repository.create(values)
    
    def update_violation(self, record_id, entries, labels):
        if not self.validator.validate_record_fields(entries, labels):
            return False
        
        values = tuple(ent.get().strip() for ent in entries)
        return self.repository.update(record_id, values)
    
    def delete_violation(self, record_id):
        return self.repository.delete(record_id)
