from flask import Flask, render_template,flash,redirect, render_template_string,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import date


# user login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session :
            return f(*args, **kwargs)
        else:
            flash("login for this page","danger")
            return redirect(url_for("login"))
    return decorated_function


# user Register form
class RegisterForm(Form):
    name = StringField("Name Surname",validators=[validators.Length(min = 4,max = 25)])
    username = StringField("Username",validators=[validators.Length(min = 5,max = 35)])
    email = StringField("Email ",validators=[validators.Email(message = "Please enter a correct email...")])
    password = PasswordField("Password:",validators=[
        validators.DataRequired(message = "Creat password"),
        validators.EqualTo(fieldname = "confirm",message="invalid password ...")
    ])
    confirm = PasswordField("Success Password")


class ProfileForm(Form):
    name = StringField("Name Surname",validators=[validators.Length(min = 4,max = 25)])
    password = PasswordField("Password:",validators=[
        validators.DataRequired(message = "Creat password")
    ])    


class LoginForm(Form):
    email = StringField("Email")
    password = PasswordField("Password")


class AddNewProductForm(Form):
    title = StringField("Title",validators=[validators.Length(min = 1)])
    category = StringField("Category",validators=[validators.Length(min = 1)])
    url = StringField("Url",validators=[validators.Length(min = 1)])
    product_code = StringField("Product Code",validators=[validators.Length(min = 1)])
    price = StringField("Price",validators=[validators.Length(min = 1)])
    description = StringField("Description",validators=[validators.Length(min = 0)])
    quantity = StringField("Quantity",validators=[validators.Length(min = 0)])


class EditProductForm(Form):
    title = StringField("Title",validators=[validators.Length(min = 1)])
    category = StringField("Category",validators=[validators.Length(min = 1)])
    url = StringField("Url",validators=[validators.Length(min = 1)])
    product_code = StringField("Product Code",validators=[validators.Length(min = 1)])
    price = StringField("Price",validators=[validators.Length(min = 1)])
    description = StringField("Description",validators=[validators.Length(min = 0)])
    quantity = StringField("Quantity",validators=[validators.Length(min = 0)])


app = Flask(__name__)
#important! KEY
app.secret_key= "project"
 # mysql 
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "project"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
#apps to do
@app.route("/")
def index():
   return render_template("index.html")

#products
@app.route("/products", methods = ["GET"])
def products():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        qry = "Select * From product"
        result = cursor.execute(qry)

        if result > 0:
            products = cursor.fetchall()
            return render_template("products.html",products = products)
        else:
            return render_template("products.html")
#products2
@app.route("/products2", methods = ["GET"])
def products2():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        qry = "Select * From product_2"
        result = cursor.execute(qry)

        if result > 0:
            products = cursor.fetchall()
            return render_template("products2.html",products = products)
        else:
            return render_template("products2.html")
        
#product edit 1

@app.route("/product-edit/<int:id>", methods = ["GET","POST"])
@login_required
def productEdit(id):
    form = EditProductForm(request.form)
    if request.method == 'POST'and form.validate():
        baseId = id
        title = form.title.data
        category = form.category.data
        url = form.url.data
        product_code = form.product_code.data
        price = form.price.data
        description = form.description.data
        quantity = form.quantity.data

        # connect to database
        cursor = mysql.connection.cursor()
        qry = """
                Update product Set title = %s,
                            category = %s,
                            url = %s,
                            product_code = %s,
                            price = %s,
                            description = %s,
                            quantity = %s
                            WHERE id = %s
            """
        cursor.execute(
            qry,(
                title,
                category,
                url,
                product_code,
                price,
                description,
                quantity,
                baseId,
            )
        )
        
        mysql.connection.commit()
        cursor.close()
        
        flash("Product editted successfully","success")
        return redirect(url_for("products"))
    else:
        return render_template("editproduct.html",form = form)        


#product edit 2

@app.route("/product2-edit/<int:id>", methods = ["GET","POST"])
@login_required
def product2Edit(id):
    form = EditProductForm(request.form)
    if request.method == 'POST'and form.validate():
        baseId = id
        title = form.title.data
        category = form.category.data
        url = form.url.data
        product_code = form.product_code.data
        price = form.price.data
        description = form.description.data
        quantity = form.quantity.data

        # connect to database
        cursor = mysql.connection.cursor()
        qry = """
                Update product_2 Set title = %s,
                            category = %s,
                            url = %s,
                            product_code = %s,
                            price = %s,
                            description = %s,
                            quantity = %s
                            WHERE id = %s
            """
        cursor.execute(
            qry,(
                title,
                category,
                url,
                product_code,
                price,
                description,
                quantity,
                baseId,
            )
        )
        
        mysql.connection.commit()
        cursor.close()
        
        flash("Product editted successfully","success")
        return redirect(url_for("products2"))
    else:
        return render_template("editproduct2.html",form = form)  


#Dashboard
#@app.route("/dashboard", methods = ["GET"])
#@login_required
#def dashboard():
#    if request.method == 'GET':
#        cursor = mysql.connection.cursor()
#        qry = "Select * From product where product_code = %s"
#        result = cursor.execute(qry,(session["product_code"],))
#
#        if result > 0:
#            articles = cursor.fetchall()
#            return render_template("dashboard.html", articles = articles)
#        else:
#            return render_template("dashboard.html")


# register 
@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        createdAt = date.today()
        count = 0
                    
        cursor = mysql.connection.cursor()
                    
        qry = "Insert into users(name,email,username,password,createdAt) VALUES(%s,%s,%s,%s,%s)"
        addQueryInto = "Insert into userlog(email,createdAt,count) VALUES(%s,%s,%s)"
        cursor.execute(qry,(name,email,username,password,createdAt))
        cursor.execute(addQueryInto,(email,createdAt,count))
        
        mysql.connection.commit()

        cursor.close()
        
        flash( "Registered...","success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form = form)


#update profile
@app.route("/profile",methods = ["GET","POST"])
def profile():
    form = ProfileForm(request.form)
    if request.method == "POST" and form.validate():
        email = session["email"]
        name = form.name.data
        password = sha256_crypt.encrypt(form.password.data)
                    
        cursor = mysql.connection.cursor()
        qry = "Update users Set name = %s , password = %s where email = %s"             
        cursor.execute(qry,(name,password,email))
        mysql.connection.commit()
        cursor.close()

        flash( "Registered...","success")
        return redirect(url_for("profile"))
    else:
        return render_template("profile.html",form = form)


#Login
@app.route("/login", methods = ["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        email = form.email.data
        password_entered = form.password.data
        
        cursor = mysql.connection.cursor()
        qry = "Select * From users where email = %s"
        result =  cursor.execute(qry,(email,))

        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password_entered, real_password):
                    flash("success enter","success")                    

                    cursor.execute("SELECT * FROM userlog WHERE email = '%s'" % email)
                    rows = cursor.fetchall()

                    cursor.execute("SELECT * FROM users WHERE email = '%s'" % email)
                    rows1 = cursor.fetchall()

                    count = rows[0]["count"]+1
                    id = rows[0]["id"]    
                    isLogin = 1  # if its for login = 1 if someone login the system  

                    qry2 = "Update userlog Set count = %s where id =%s"             
                    cursor.execute(qry2,(count,id))

                    qry3 = "Update users Set isLogin = %s where email =%s"             
                    cursor.execute(qry3,(isLogin,email))

                    mysql.connection.commit()


                    session["logged_in"] = True
                    session["username"] = rows1[0]["username"]                    
                    session["email"] = rows1[0]["email"]   
                    cursor.close()

                    return redirect(url_for("index"))
            else:
                    flash("invalid password...", "danger")
                    return redirect(url_for("login")) 
        else:
            flash("has no users....","danger")
            return redirect(url_for("login"))    

    return render_template("login.html",form=form)


#log out
@app.route("/logout")
def logout():
    cursor = mysql.connection.cursor()                    
    email = session["email"]     
    isLogin = 0  # if its for login = 1 if someone login the system  
    qry = "Update users Set isLogin = %s where email =%s"             
    cursor.execute(qry,(isLogin,email))
    mysql.connection.commit()
    cursor.close()

    session.clear()
    return redirect(url_for("index"))

#add-product 1
@app.route("/add-product",methods = ["GET","POST"])
def productSave():
    form = AddNewProductForm(request.form)
    if request.method== "POST" and form.validate():
        title = form.title.data
        category = form.category.data
        url = form.url.data
        product_code = form.product_code.data
        price = form.price.data
        description = form.description.data
        quantity = form.quantity.data
        whoIsAdd = session["email"]
        rank = 1
        isActive = 1

        cursor = mysql.connection.cursor()
        
        qry = """
                Insert into product(
                    quantity,
                    whoIsAdd,
                    title,
                    category,
                    url,
                    product_code,
                    price,
                    description,
                    rank,
                    isActive
                    ) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
              """ 
        
        cursor.execute(
            qry, 
            (
                quantity,
                whoIsAdd,
                title,
                category,
                url,
                product_code,
                price,
                description,
                rank,
                isActive,
            )
        )
        mysql.connection.commit()
        cursor.close()
        
        flash("Product added successfully","success")
        return redirect(url_for("products"))
    else:
        return render_template("addproduct.html", form=form)

#add-product 2
@app.route("/add-product2",methods = ["GET","POST"])
def product2Save():
    form = AddNewProductForm(request.form)
    if request.method== "POST" and form.validate():
        title = form.title.data
        category = form.category.data
        url = form.url.data
        product_code = form.product_code.data
        price = form.price.data
        description = form.description.data
        quantity = form.quantity.data
        whoIsAdd = session["email"]
        rank = 1
        isActive = 1

        cursor = mysql.connection.cursor()
        
        qry = """
                Insert into product_2(
                    quantity,
                    whoIsAdd,
                    title,
                    category,
                    url,
                    product_code,
                    price,
                    description,
                    rank,
                    isActive
                    ) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
              """ 
        
        cursor.execute(
            qry, 
            (
                quantity,
                whoIsAdd,
                title,
                category,
                url,
                product_code,
                price,
                description,
                rank,
                isActive,
            )
        )
        mysql.connection.commit()
        cursor.close()
        
        flash("Product added successfully","success")
        return redirect(url_for("products2"))
    else:
        return render_template("addproduct2.html", form=form)

#delete 1
@app.route("/product-delete/<int:id>", methods = ["GET","POST"])
@login_required
def productDelete(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        qry = "delete from product where id = %s"
        cursor.execute(qry,(id,))
        mysql.connection.commit()
        cursor.close()
        flash("Product deleted successfully","danger")
        return redirect(url_for("products"))


#delete 2
@app.route("/product2-delete/<int:id>", methods = ["GET","POST"])
@login_required
def product2Delete(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        qry = "delete from product_2 where id = %s"
        cursor.execute(qry,(id,))
        mysql.connection.commit()
        cursor.close()
        flash("Product deleted successfully","danger")
        return redirect(url_for("products2"))

if __name__ == "__main__":
    app.run(debug=True)
