# استدعاء مكتبة Flask
from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib
import sqlite3
from database import get_connection, init_db

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = 'solvane123'

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

# صفحة الرحلات
@app.route('/trips')
def trips():
    return render_template('trips.html')

# صفحة تفاصيل الرحلة
@app.route('/trip-details')
def trip_details():
    return render_template('trip_details.html')

# صفحة الحجز
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        travelers = request.form.get('travelers')
        date = request.form.get('date')
        conn = get_connection()
        conn.execute('INSERT INTO bookings (name,email,phone,travelers,date) VALUES (?,?,?,?,?)',
                     (name, email, phone, travelers, date))
        conn.commit()
        conn.close()
        return render_template('booking.html', success='Booking confirmed successfully!')
    return render_template('booking.html')

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = hashlib.sha256(request.form.get('password').encode()).hexdigest()
        conn = get_connection()
        user = conn.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password)).fetchone()
        conn.close()
        if user:
            session['user_name'] = user['name']
            return redirect(url_for('home'))
        # رسالة خطأ لو البيانات غلط
        return render_template('login.html', error='Wrong email or password.')
    return render_template('login.html')

# صفحة إنشاء حساب
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = hashlib.sha256(request.form.get('password').encode()).hexdigest()
        conn = get_connection()
        conn.execute('INSERT INTO users (name,email,password) VALUES (?,?,?)', (name, email, password))
        conn.commit()
        conn.close()
        # رسالة نجاح بعد التسجيل
        return render_template('register.html', success='Account created successfully!')
    return render_template('register.html')

# صفحة التواصل
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        conn = get_connection()
        conn.execute('INSERT INTO messages (name,email,message) VALUES (?,?,?)', (name, email, message))
        conn.commit()
        conn.close()
        # رسالة نجاح بعد الإرسال
        return render_template('contact.html', success='Message sent successfully!')
    return render_template('contact.html')

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    conn = get_connection()
    bookings = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()
    return render_template('admin.html', bookings=bookings)

# تشغيل التطبيق
if __name__== '__main__':
    init_db()
    