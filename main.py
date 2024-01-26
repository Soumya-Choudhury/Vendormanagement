from flask import Flask, redirect, url_for, session, request, render_template
from requests_oauthlib import OAuth2Session
from mysql.connector import connect, Error
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) 

# Google OAuth2 configuration
GOOGLE_CLIENT_ID = "261086046288-nf43280t94sqei96dmnr684nb7b7bbql.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
REDIRECT_URI = 'https://localhost:8501/callback'
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPE = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]

# Database configuration
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Soumya@27052002"
MYSQL_DB = "vendormanagement"

# Function to create a connection with the MySQL database
def create_connection():
    try:
        conn = connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def home():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vendors")
    vendors = cursor.fetchall()
    conn.close()
    return render_template('home.html', vendors=vendors)

@app.route('/login')
def login():
    google = OAuth2Session(GOOGLE_CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
    authorization_url, state = google.authorization_url(AUTHORIZATION_BASE_URL, access_type="offline", prompt="select_account")
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    
    state = session.get('oauth_state')
    
    if not state:
        
        print("OAuth state not found in the session.")
        return redirect(url_for('login'))

    google = OAuth2Session(GOOGLE_CLIENT_ID, state=state, redirect_uri=REDIRECT_URI)
    try:
        token = google.fetch_token(TOKEN_URL, client_secret=GOOGLE_CLIENT_SECRET, authorization_response=request.url)
    except Error as e:
        
        print(f"Error fetching the OAuth token: {e}")
        return redirect(url_for('login'))

    userinfo = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    session['email'] = userinfo['email']
    
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE email = %s", (userinfo['email'],))
        result = cursor.fetchone()
        
        if not result:
            cursor.execute("INSERT INTO users (email) VALUES (%s)", (userinfo['email'],))
            conn.commit()
        
        conn.close()
    
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():
    if request.method == 'POST':
        vendor_name = request.form['vendor_name']
        bank_account_no = request.form['bank_account_no']
        bank_name = request.form['bank_name']
        address_line_1 = request.form['address_line_1']
        address_line_2 = request.form['address_line_2']
        city = request.form['city']
        country = request.form['country']
        zip_code = request.form['zip_code']
        
        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vendors (
                    vendor_name, bank_account_no, bank_name, address_line_1, address_line_2, city, country, zip_code
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                vendor_name, bank_account_no, bank_name, address_line_1, address_line_2, city, country, zip_code
            ))
            conn.commit()
            conn.close()
        
        return redirect(url_for('home'))
    return render_template('add_vendor.html')



@app.route('/edit_vendor/<int:vendor_id>', methods=['GET', 'POST'])
def edit_vendor(vendor_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        
        vendor_name = request.form['vendor_name']
        bank_account_no = request.form['bank_account_no']
        bank_name = request.form['bank_name']
        address_line_1 = request.form['address_line_1']
        address_line_2 = request.form['address_line_2']
        city = request.form['city']
        country = request.form['country']
        zip_code = request.form['zip_code']
        
        
        cursor.execute("""
            UPDATE vendors SET
            vendor_name=%s, bank_account_no=%s, bank_name=%s, address_line_1=%s, 
            address_line_2=%s, city=%s, country=%s, zip_code=%s
            WHERE vendor_id=%s
        """, (
            vendor_name, bank_account_no, bank_name, address_line_1, address_line_2, 
            city, country, zip_code, vendor_id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    
    cursor.execute("SELECT * FROM vendors WHERE vendor_id = %s", (vendor_id,))
    vendor = cursor.fetchone()
    conn.close()
    return render_template('edit_vendor.html', vendor=vendor)

@app.route('/delete_vendor/<int:vendor_id>', methods=['POST'])
def delete_vendor(vendor_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    
    cursor.execute("DELETE FROM vendors WHERE vendor_id = %s", (vendor_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, port=8501, ssl_context='adhoc')
