# استدعاء المكتبات المطلوبة
import sqlite3
import os

# مسار قاعدة البيانات
DB = os.path.join(os.path.dirname(__file__), 'solvane.db')

# دالة الاتصال بقاعدة البيانات
def get_connection():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# دالة إنشاء الجداول وإضافة البيانات
def init_db():
    conn = get_connection()
    c = conn.cursor()

    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT)''')

    # جدول الحجوزات
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        travelers INTEGER,
        date TEXT)''')

    # جدول رسائل التواصل
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT)''')

    conn.commit()
    conn.close()
