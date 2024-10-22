from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

usuarios = {
    'admin': 'admin',
    'admin2': 'admin2',
}

produtos = [
    {'codigo': 1, 'nome': 'Prego', 'quantidade': 100, 'estoque_minimo': 20},
    {'codigo': 2, 'nome': 'Parafuso', 'quantidade': 50, 'estoque_minimo': 10},
    {'codigo': 3, 'nome': 'Porca', 'quantidade': 30, 'estoque_minimo': 5},
]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username in usuarios and usuarios[username] == password:
        session['username'] = username
        return redirect(url_for('index'))
    else:
        flash('Usuário ou senha incorretos!', 'danger')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'], produtos=produtos)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    codigo = int(request.form['codigo'])
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    estoque_minimo = int(request.form['estoque_minimo'])

    for produto in produtos:
        if produto['codigo'] == codigo:
            flash('Erro: Código de produto já existe!', 'danger')
            return redirect(url_for('index'))

    produtos.append({
        'codigo': codigo,
        'nome': nome,
        'quantidade': quantidade,
        'estoque_minimo': estoque_minimo
    })
    flash('Produto cadastrado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/adicionar', methods=['POST'])
def adicionar():
    if 'username' not in session:
        flash('Você precisa estar logado para adicionar produtos!', 'danger')
        return redirect(url_for('login'))

    codigo = int(request.form['codigo'])
    quantidade = int(request.form['quantidade'])

    for produto in produtos:
        if produto['codigo'] == codigo:
            produto['quantidade'] += quantidade
            flash('Estoque adicionado com sucesso!', 'success')
            return redirect(url_for('index'))

    flash('Produto não encontrado! Código inválido.', 'danger')
    return redirect(url_for('index'))

@app.route('/remover', methods=['POST'])
def remover():
    if 'username' not in session:
        flash('Você precisa estar logado para remover produtos!', 'danger')
        return redirect(url_for('login'))

    codigo = int(request.form['codigo'])
    quantidade = int(request.form['quantidade'])

    for produto in produtos:
        if produto['codigo'] == codigo:
            if produto['quantidade'] >= quantidade:
                produto['quantidade'] -= quantidade
                flash('Estoque removido com sucesso!', 'success')
            else:
                flash('Quantidade a remover maior que o disponível!', 'danger')
            return redirect(url_for('index'))

    flash('Produto não encontrado! Código inválido.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
