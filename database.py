import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from config import AppConfig
from abc import ABC, abstractmethod


class DatabaseConnection:
    
    def __init__(self):
        self.config = AppConfig()
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.config.db_host,
                user=self.config.db_user,
                password=self.config.db_password,
                database=self.config.db_name
            )
            self.cursor = self.connection.cursor()
            return self
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database:\n{e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
            self.connection.close()
        return False
    
    def execute(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor
    
    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()


class DatabaseRepository(ABC):
    def __init__(self):
        self.config = AppConfig()
    
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def get_by_id(self, record_id):
        pass
    
    @abstractmethod
    def create(self, data):
        pass
    
    @abstractmethod
    def update(self, record_id, data):
        pass
    
    @abstractmethod
    def delete(self, record_id):
        pass


class TrafficViolationRepository(DatabaseRepository):
    def get_all(self):
        try:
            with DatabaseConnection() as db:
                db.execute("SELECT * FROM traffic_violations")
                return db.fetchall()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch records:\n{e}")
            return []
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            return []
    
    def get_by_id(self, record_id):
        try:
            with DatabaseConnection() as db:
                db.execute("SELECT * FROM traffic_violations WHERE id=%s", (record_id,))
                return db.fetchone()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch record:\n{e}")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            return None
    
    def search(self, search_term):
        try:
            with DatabaseConnection() as db:
                query = """SELECT * FROM traffic_violations 
                           WHERE PlateNumber LIKE %s OR DriverName LIKE %s OR Charge LIKE %s"""
                value = f"%{search_term}%"
                db.execute(query, (value, value, value))
                return db.fetchall()
        except Error as e:
            messagebox.showerror("Search Error", f"Failed to search records:\n{e}")
            return []
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            return []
    
    def create(self, data):
        try:
            with DatabaseConnection() as db:
                query = """INSERT INTO traffic_violations 
                (PlateNumber, DriverName, Description, Belts, Personal_Injury, Property_Damage, 
                Commercial_License, Commercial_Vehicle, State, VehicleType, Year, Make, Model, Color, 
                Charge, PenaltyAmount, Contributed_To_Accident, Race, Gender, Driver_City, Driver_State, 
                DL_State, Arrest_Type, Violation_Type)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                db.execute(query, data)
                return True
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to add record:\n{e}")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            return False
    
    def update(self, record_id, data):
        try:
            with DatabaseConnection() as db:
                query = """UPDATE traffic_violations SET PlateNumber=%s, DriverName=%s, Description=%s, Belts=%s,
                Personal_Injury=%s, Property_Damage=%s, Commercial_License=%s, Commercial_Vehicle=%s,
                State=%s, VehicleType=%s, Year=%s, Make=%s, Model=%s, Color=%s, Charge=%s, PenaltyAmount=%s,
                Contributed_To_Accident=%s, Race=%s, Gender=%s, Driver_City=%s, Driver_State=%s, DL_State=%s,
                Arrest_Type=%s, Violation_Type=%s WHERE id=%s"""
                vals = data + (record_id,)
                db.execute(query, vals)
                return True
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to update record:\n{e}")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            return False
    
    def delete(self, record_id):
        try:
            with DatabaseConnection() as db:
                db.execute("DELETE FROM traffic_violations WHERE id=%s", (record_id,))
                return True
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to delete record:\n{e}")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            return False
