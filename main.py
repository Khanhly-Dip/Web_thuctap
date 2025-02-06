import mysql.connector
from flask import Flask, jsonify, request, redirect, url_for
import os
from flask import Flask, render_template

cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password="khanhLee#10825",
        database="web_ungdung"
    )
print("Connection successful!")


def get_all():
    print("Không có dữ liệu trả về từ cơ sở dữ liệu3")
    cursor = cnx.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM ungdung"
        cursor.execute(query)
        
        result = cursor.fetchall()
        print("Dữ liệu trả về từ cơ sở dữ liệu:", result)
        for rows in result:
            print(rows)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        result = []
    
    finally:
        cursor.close()
    
    return jsonify(result)



app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/fanpage')
def fanpage():
    return render_template("index.html")  # Nếu đây cũng là trang chủ.

@app.route('/resgiter')
def resgiter():
    return render_template("ResgiterForm.html")


@app.route('/forstudent')
def forstudent():
    return render_template('Forstudent.html')

@app.route('/danhgia')
def danhgia():
    product_id = request.args.get('id')
    if not product_id:
        return "Product ID not provided", 400

    try:
        cursor = cnx.cursor(dictionary=True)

        # Truy vấn sản phẩm theo ID
        cursor.execute("SELECT * FROM ungdung WHERE id_ungdung = %s", (product_id,))
        product = cursor.fetchone()

        if not product:
            return "Product not found", 404

        # Truy vấn đánh giá từ bảng danhgia
        cursor.execute("SELECT * FROM danhgia WHERE id_ungdung = %s", (product_id,))
        reviews = cursor.fetchall()  # Lấy tất cả đánh giá

        return render_template('danhgia.html', product=product, reviews=reviews if reviews else None)

    except mysql.connector.Error as err:
        return f"Database error: {err}", 500

    finally:
        cursor.close()


@app.route('/contact')
def contact():
    return render_template('Contact.html')


# tải trang sản phẩm

@app.route('/product')
def product():
    product_id = request.args.get('id')
    cursor = cnx.cursor(dictionary=True)

    if product_id:
        # Truy vấn sản phẩm theo ID
        cursor.execute("SELECT * FROM ungdung WHERE id_ungdung = %s", (product_id,))
        product = cursor.fetchone()
        
        if product:
            return render_template('product.html', product=product)
        else:
            return "Product not found", 404
    else:
        return "Product ID not provided", 400

# dành cho gửi đánh giá đi
@app.route('/api/submit-rating', methods=['POST'])
def submit_rating():
    try:
        data = request.get_json()  # Lấy dữ liệu JSON từ body
        id_ungdung = data['id_ungdung']
        mota = data['mota']
        saovote = data['saovote']
        print(f"Received id_ungdung: {id_ungdung}, mota: {mota}, saovote: {saovote}")

        # Chèn vào bảng danhgia mà không cần gửi id_danhgia
        cursor = cnx.cursor()
        query = """
            INSERT INTO danhgia (id_ungdung, mota, saovote)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (id_ungdung, mota, saovote))
        cnx.commit()

        return jsonify({"success": True})

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        cursor.close()


# dành cho trang đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = cnx.cursor(dictionary=True)

        try:
            # Truy vấn để tìm user
            cursor.execute('SELECT * FROM account WHERE email = %s AND password = %s', (email, password))
            user = cursor.fetchone()

            if user:
                # Đăng nhập thành công, chuyển hướng
                return redirect(url_for('fanpage'))
            else:
                # Thông báo lỗi nếu không tìm thấy người dùng
                return render_template('loginForm.html', error="Invalid email or password")
        except mysql.connector.Error as err:
            return render_template('loginForm.html', error="Database error: " + str(err))

        finally:
            cursor.close()

    return render_template('loginForm.html')


# dành cho trang chủ

@app.route('/api/ungdung')
def api_ungdung():
    cursor = cnx.cursor(dictionary=True)
    try:
        query = "SELECT * FROM ungdung LIMIT 6"
        cursor.execute(query)
        result = cursor.fetchall()
        return jsonify(result)  # Trả về dữ liệu JSON
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
# Trang dành cho sinh viên

@app.route('/api/filter')
def api_filter():
    cursor = cnx.cursor(dictionary=True)
    try:
        query = "SELECT * FROM ungdung where theloai='hoctap' LIMIT 6"
        cursor.execute(query)
        result = cursor.fetchall()
        return jsonify(result)  # Trả về dữ liệu JSON
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8000)