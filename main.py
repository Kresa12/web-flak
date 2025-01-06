from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'circle'

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    database = "uas_web",
    password="")

@app.route('/cek_database')
def cek_database():
    cur = cnx.cursor()
    cur.execute('SELECT 1')
    return jsonify({'messege' : 'database berhasil'})

@app.route('/')
def home():
    cur = cnx.cursor()
    query = '''
            SELECT product.*, category.name_category FROM product
            INNER JOIN category
            ON product.categoryId = category.id_category
            '''
    cur.execute(query)
    product = cur.fetchall()
    return render_template('index.html', product=product)

@app.route('/homepage')
def homepage():
    cur = cnx.cursor()
    query = '''
            SELECT product.*, category.name_category FROM product
            INNER JOIN category
            ON product.categoryId = category.id_category
            '''
    cur.execute(query)
    product = cur.fetchall()
    return render_template('home-page.html', product=product)

@app.route('/simpan-data', methods=['post'])
def submit():
    name_product = request.form['name_product'].upper()
    image = request.form['image']
    price = request.form['price']
    categoryId = request.form['categoryId']
    data = {
            'name_product' : name_product, 
            'image' : image,
            'price' : price, 
            'categoryId' : categoryId, 
            }
    
    mysql.connection.commit()
    return redirect(url_for('home'))    

@app.route('/form-product')
def form_add_product():
    cur = cnx.cursor()
    query = 'SELECT * FROM category'
    cur.execute(query)
    category = cur.fetchall()
    return render_template('form-product.html', category = category)

@app.route('/add-product', methods = ['POST'])
def add_product():
    name_product = request.form['name_product']
    image = request.form['image_url']
    price = request.form['price']
    category = request.form['category']
    
    cur = cnx.cursor()
    cur.execute('INSERT INTO product (name_product, image, price, categoryId) VALUES (%s, %s, %s, %s)', (name_product, image, price, category))
    cur = cnx.commit()
    return redirect('/homepage')

@app.route('/form-edit-product/<int:id>')
def form_edit_product(id):
    cur = cnx.cursor()
    query = 'SELECT * FROM product WHERE id = %s'
    cur.execute(query, [id])
    product = cur.fetchone()
    # return jsonify (product)
    query = 'SELECT * FROM category'
    cur.execute(query)
    category = cur.fetchall()

    return render_template('form-edit-product.html' , product = product, category = category )

@app.route('/edit-product/<int:id>', methods = ['GET', "POST"])
def edit_product(id):
    name_product = request.form['name_product']
    image = request.form['image_url']
    price = request.form['price']
    category = request.form['category']

    cur = cnx.cursor()
    query = ''' UPDATE product SET 
                name_product = %s,
                image = %s,
                price = %s,
                categoryId = %s
                WHERE id = %s
            '''
    cur.execute(query,(name_product,image,price,category,id))
    cur = cnx.commit()  
    flash('data berhasil diedit','succes')
    return redirect('/homepage')

@app.route('/delete-product/<int:id>', methods = ['GET', "POST", "DELETE"])
def delete_product(id):
    cur = cnx.cursor()
    query = 'DELETE FROM product WHERE id = %s'
    cur.execute(query,[id])
    cur = cnx.commit()
    flash ('Data Berhasil dihapus','succes')
    return redirect('/homepage')

@app.route('/base')
def base():
    return render_template('base.html')

if __name__=="__main__":
    app.run(debug=True)