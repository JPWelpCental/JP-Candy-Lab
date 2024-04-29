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
        return render_template('checkout.html', invs=invs, total=total, mem_id=session['mem_id'])
    else:
        return render_template('checkout.html', invs=invs, total=total)

@app.route('/receipt', methods=['POST'])
def receipt():
    invs = request.form.get('invs')

    mem_id = session['mem_id'] if 'mem_id' in session else "Guest"
    is_member = True if 'mem_id' in session else False
    today = date.today()
    invs = ast.literal_eval(invs)
    desc = ", ".join([f"{inv[0]}, {inv[2]}" for inv in invs])
    total = sum([inv[3] for inv in invs])
    total = float(total)*0.9 if is_member else float(total)

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