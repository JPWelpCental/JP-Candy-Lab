from flask import *
import sqlite3
from createdb import *
import ast
from datetime import date

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def home():

    invs = get_inv()

    if 'mem_id' in session:
        return render_template('index.html', invs=invs, mem_id=session['mem_id'])
    else:
        return render_template('index.html', invs=invs)


@app.route('/checkout', methods=['POST'])
def checkout():
    qty = request.form.getlist('quantity')
    qty = [int(q) for q in qty]
    if qty == [0, 0, 0, 0, 0]:
        return redirect(url_for('home'))

    invs = get_inv()
    invs = [(invs[i][1], invs[i][3], qty[i], invs[i][3]*qty[i]) for i in range(len(invs)) if int(qty[i]) > 0]  # Filter out items with qty = 0
    total = sum([inv[3] for inv in invs])
    total = float(total)*0.9 if 'mem_id' in session else float(total)

    if 'mem_id' in session:
        return render_template('checkout.html',qty=qty , invs=invs, total=total, mem_id=session['mem_id'])
    else:
        return render_template('checkout.html',qty=qty , invs=invs, total=total)

@app.route('/receipt', methods=['POST'])
def receipt():
    qty = request.form.get('qty')
    qty = ast.literal_eval(qty)

    mem_id = session['mem_id'] if 'mem_id' in session else "Guest"
    is_member = True if 'mem_id' in session else False
    today = date.today()
    invs = get_inv()
    invs = [(invs[i][0], invs[i][1], float(invs[i][3]), int(invs[i][4]), int(qty[i]), invs[i][3]*int(qty[i])) for i in range(len(invs)) if int(qty[i]) > 0]
    desc = ", ".join([f"{inv[1]}, {inv[4]}" for inv in invs])
    total = sum([inv[5] for inv in invs])
    total = float(total)*0.9 if is_member else float(total)

    for inv in invs:
        update_inv(inv[0], inv[3]-inv[4])

    insert_trans_log(mem_id, today, desc, is_member, total)

    if 'mem_id' in session:
        return render_template('receipt.html', invs=invs, total=total, mem_id=mem_id)
    else:
        return render_template('receipt.html', invs=invs, total=total)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']

        mem = get_mem(email, pw)

        if mem:
            session['mem_id'] = mem[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        mem_id = request.form['username']
        email = request.form['email']
        pw = request.form['password']

        insert_mem(mem_id, email, pw)

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('mem_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)