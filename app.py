from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chave_secreta_super_segura'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Definição da classe User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100))
    cpf = db.Column(db.String(14), unique=True)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(120), unique=True)
    senha = db.Column(db.String(100))
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cep = db.Column(db.String(10))
    tipo = db.Column(db.String(20))  # 'cliente' ou 'entregador'
    produtos = db.relationship('Produto', backref='user', lazy=True, foreign_keys='Produto.user_id')

# Definição da classe Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50))
    entregador_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    entregador = db.relationship('User', foreign_keys=[entregador_id])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rota para a landing page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = User.query.filter_by(email=email).first()
        
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            if usuario.tipo == 'cliente':
                return redirect(url_for('cliente_dashboard'))
            elif usuario.tipo == 'entregador':
                return redirect(url_for('entregador_dashboard'))
            else:
                flash('Tipo de usuário inválido', 'error')
                return redirect(url_for('index'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
            return redirect(url_for('index'))
    
    return render_template('login.html')

# Rota para cadastro de usuário
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome_completo = request.form['nome_completo']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        rua = request.form['rua']
        numero = request.form['numero']
        complemento = request.form['complemento']
        bairro = request.form['bairro']
        cep = request.form['cep']
        tipo = request.form['tipo']

        # Verifica se o usuário já existe pelo email
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado. Por favor, utilize outro email.', 'error')
            return redirect(url_for('cadastro'))

        novo_usuario = User(nome_completo=nome_completo, cpf=cpf, telefone=telefone, email=email,
                            senha=senha, rua=rua, numero=numero, complemento=complemento,
                            bairro=bairro, cep=cep, tipo=tipo)
        
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Erro ao cadastrar usuário: {str(e)}', 'error')
            db.session.rollback()

    return render_template('cadastro.html')

# Rota para o dashboard do cliente
@app.route('/cliente')
@login_required
def cliente_dashboard():
    produtos_usuario = current_user.produtos
    return render_template('cliente.html', current_user=current_user, produtos=produtos_usuario)

# Rota para o dashboard do entregador
@app.route('/entregador')
@login_required
def entregador_dashboard():
    produtos_disponiveis = Produto.query.filter_by(status='Aguardando entregador').all()
    produtos_pacote = Produto.query.filter_by(status='Pacote com entregador', entregador_id=current_user.id).all()
    return render_template('entregador.html', produtos_disponiveis=produtos_disponiveis, produtos_pacote=produtos_pacote)

# Rota para adicionar produto pelo cliente
@app.route('/adicionar_produto', methods=['POST'])
@login_required
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        
        novo_produto = Produto(nome=nome, descricao=descricao, user_id=current_user.id, status='Aguardando entregador')
        
        try:
            db.session.add(novo_produto)
            db.session.commit()
            flash('Produto cadastrado com sucesso!', 'success')
            return redirect(url_for('cliente_dashboard'))
        except Exception as e:
            flash(f'Erro ao cadastrar produto: {str(e)}', 'error')
            db.session.rollback()

    return redirect(url_for('cliente_dashboard'))

# Rota para o entregador pegar um produto
@app.route('/pegar_produto/<int:produto_id>', methods=['POST'])
@login_required
def pegar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    
    if produto.status == 'Aguardando entregador':
        produto.status = 'Pacote com entregador'
        produto.entregador_id = current_user.id
        try:
            db.session.commit()
            flash(f'Produto {produto.nome} foi pegue.', 'success')
        except Exception as e:
            flash(f'Erro ao pegar produto: {str(e)}', 'error')
            db.session.rollback()
    else:
        flash('Produto não está mais disponível para pegar.', 'error')
    
    return redirect(url_for('entregador_dashboard'))

# Rota para marcar um produto como entregue pelo entregador
@app.route('/produto_entregue/<int:produto_id>', methods=['POST'])
@login_required
def produto_entregue(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    
    if produto.entregador_id == current_user.id and produto.status == 'Pacote com entregador':
        produto.status = 'Produto Entregue'
        produto.entregador_id = None
        try:
            db.session.commit()
            flash(f'Produto {produto.nome} foi entregue.', 'success')
        except Exception as e:
            flash(f'Erro ao marcar produto como entregue: {str(e)}', 'error')
            db.session.rollback()
    else:
        flash('Você não pode marcar este produto como entregue.', 'error')
    
    return redirect(url_for('entregador_dashboard'))

# Rota para ver detalhes de um produto pelo entregador
@app.route('/detalhes_produto/<int:produto_id>', methods=['GET'])
@login_required
def detalhes_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    if produto.status == 'Pacote com entregador' and produto.entregador_id == current_user.id:
        cliente = User.query.get(produto.user_id)
        return render_template('detalhes_produto.html', produto=produto, cliente=cliente)
    else:
        flash('Produto não está mais disponível para detalhes.', 'error')
        return redirect(url_for('entregador_dashboard'))

# Rota para finalizar um pedido pelo entregador
@app.route('/finalizar_pedido/<int:produto_id>', methods=['POST'])
@login_required
def finalizar_pedido(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    produto.status = 'Pedido Finalizado'
    try:
        db.session.commit()
        flash(f'Pedido do produto {produto.nome} finalizado com sucesso.', 'success')
    except Exception as e:
        flash(f'Erro ao finalizar pedido: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('entregador_dashboard'))

# Rota para logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
