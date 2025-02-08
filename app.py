from datetime import datetime
from flask import (
    Flask, render_template, request, session, abort,
    redirect, url_for, jsonify, flash, send_from_directory
)
import hashlib
import os
from werkzeug.utils import secure_filename
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


class User:
    def __init__(self, user_id, username, password, email, full_name, role='user', is_active=True):
        self.user_id = user_id
        self.username = username
        self.password_hash = self._hash_password(password)
        self.email = email
        self.full_name = full_name
        self.role = role
        self.is_active = is_active
        self.created_at = datetime.now()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == self._hash_password(password)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }


users = [
    User(1, 'admin', '1234', 'admin@example.com', 'Administrador', 'admin'),
    User(2, 'usuario', '123456', 'user@example.com', 'Usuário Padrão')
]

posts = []
uploaded_files = []
auth_users = {'admin': '1234'}


@app.template_filter('datetime_format')
def format_datetime(value):
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    return value.strftime('%d/%m/%Y às %H:%M')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/lesson_summaries')
def lesson_summaries():
    summaries = [
        {
            "title": "Contexto Geral",
            "content": """
                <div class="lesson-section">
                    <h3>Linguagem e Ferramentas</h3>
                    <p>Python + Flask (framework) e SQLAlchemy (ORM).</p>
                    <p>Desenvolvimento de aplicações web com integração a banco de dados, APIs, validações e boas práticas.</p>
                </div>
            """
        },
        {
            "title": "AULA 01 (09/10)",
            "content": """
                <div class="lesson-section">
                    <h3>Avaliações</h3>
                    <div class="evaluation-grid">
                        <div class="evaluation-item">
                            <h4>Prova Prática</h4>
                            <div class="evaluation-details">
                                <p><strong>Datas:</strong> 11/12 e 18/12</p>
                                <p>Desenvolver uma aplicação ao vivo com requisitos específicos.</p>
                            </div>
                        </div>
                        <div class="evaluation-item">
                            <h4>Portfólio</h4>
                            <div class="evaluation-details">
                                <p><strong>Entrega:</strong> 12/02</p>
                                <p>Documentação de atividades e projetos.</p>
                            </div>
                        </div>
                        <div class="evaluation-item">
                            <h4>Projeto Final</h4>
                            <div class="evaluation-details">
                                <p><strong>Entrega:</strong> 22/01</p>
                                <div class="requirements-box">
                                    <h5>Requisitos:</h5>
                                    <ul>
                                        <li>Pelo menos 1 API funcional.</li>
                                        <li>Endpoint documentado.</li>
                                        <li>Validações de dados e código limpo.</li>
                                        <li>Integração com banco de dados.</li>
                                        <li>Bônus por escalabilidade.</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="lesson-section">
                    <h3>Configuração Inicial</h3>
                    <ul>
                        <li>Uso de ambiente virtual Python (venv).</li>
                        <li>Arquivo requirements.txt para dependências.</li>
                        <li>Instalação do Python 3.11.</li>
                    </ul>
                </div>

                <div class="lesson-section">
                    <h3>Boas Práticas</h3>
                    <ul>
                        <li>Pastas templates (HTML) e static (CSS/JS).</li>
                        <li>Nomes em inglês, sem comentários redundantes.</li>
                    </ul>
                </div>
            """
        },
        {
            "title": "Aula 02 (16/10)",
            "content": """
                <div class="lesson-section">
                    <h3>Temas dos Projetos</h3>
                    <ul>
                        <li>Sistema de chamada por câmera.</li>
                        <li>Análise de emoções em imagem.</li>
                        <li>Scanner para documentos PDF.</li>
                    </ul>
                </div>
            """
        },
        {
            "title": "AULA 03 (23/10)",
            "content": """
                <div class="lesson-section">
                    <h3>Ambiente Virtual no Windows</h3>
                    <ul>
                        <li>Criar ambiente: <code>python -m venv nome_do_ambiente</code>.</li>
                        <li>Autorizar no PowerShell: <code>Get-ExecutionPolicy</code>, <code>Set-ExecutionPolicy RemoteSigned -Scope CurrentUser</code>.</li>
                        <li>Ativar: <code>nome_do_ambiente\Scripts\activate</code>.</li>
                        <li>Desativar: <code>deactivate</code>.</li>
                        <li>Instalar pacotes: <code>pip install nome_pacote</code>.</li>
                        <li>Pacotes instalados: Flask, Flask-SQLAlchemy, numpy.</li>
                    </ul>
                </div>

                <div class="lesson-section">
                    <h3>Padrões de Arquivo e Organização de Código</h3>
                    <ul>
                        <li>Frameworks trabalham com padrão.</li>
                        <li>Arquivos .html devem estar na pasta templates.</li>
                        <li>Código limpo e nomes relevantes. Zero comentários.</li>
                        <li>Nomes todos em inglês, nada em português - classes, variáveis, nomes, arquivos.</li>
                        <li>Variáveis snake_case (padrão da linguagem), nada de acentos ou caracteres especiais.</li>
                    </ul>
                </div>
            """
        },
        {
            "title": "AULA 04 (30/10): Desenvolvimento com Flask",
            "content": """
                <div class="lesson-section">
                    <h3>Conceitos Fundamentais</h3>
                    <ul>
                        <li>Aplicações web seguem o modelo requisição e resposta (request & response).</li>
                        <li>O Flask mantém o código Python ativo, aguardando requisições e respondendo a elas.</li>
                        <li>Funciona de forma reativa, ou seja, só executa algo quando recebe uma solicitação.</li>
                    </ul>
                </div>

                <div class="lesson-section">
                    <h3>Configuração Inicial</h3>
                    <ul>
                        <li>Importação do Flask: <code>from flask import Flask</code>.</li>
                        <li>Criação da aplicação Flask: <code>app = Flask(__name__)</code>.</li>
                        <li>Execução do servidor com recarregamento automático: <code>app.run(debug=True)</code>.</li>
                        <li>Definição de porta específica: <code>app.run(debug=True, port=5001)</code>.</li>
                        <li>Disponibilização para dispositivos na mesma rede: <code>app.run(debug=True, port=5001, host='0.0.0.0')</code>.</li>
                    </ul>
                </div>

                <div class="lesson-section">
                    <h3>Criação de Rotas</h3>
                    <p>Para tornar a aplicação interativa, criamos rotas associadas a funções:</p>
                    <div class="code-block">
                        <code>@app.route('/contact')<br>
                        def contact():<br>
                        &nbsp;&nbsp;return 'This is the user page'</code>
                    </div>
                </div>

                <div class="lesson-section">
                    <h3>Lista de Atividades 1</h3>
                    <ol>
                        <li>Crie uma rota para uma página web com a tag canvas que permite ao usuário deslocar uma fotografia para a direita e esquerda com as setinhas do teclado.</li>
                        <li>Crie uma rota para a atividade 2 que permita ao usuário capturar uma fotografia pela webcam e mostrar na tela.</li>
                        <li>Crie uma rota para a atividade 3 com python app que exiba uma tabela (sem usar table) com 997 linhas e 5 colunas: nas colunas id, nome, sobrenome, e-mail, ações.</li>
                        <li>Crie uma rota com 3 links, um para cada uma das atividades anteriores, porém todas elas bonitas.</li>
                        <li>Crie 6 rotas, sendo cada uma estilizada, bonita e etc. Sendo que em cada rota deve conter o currículo de um integrante do grupo.</li>
                    </ol>
                </div>
            """
        },
        {
            "title": "Aula 05 (06/11)",
            "content": """
                <div class="lesson-section">
                    <h3>Passagem de Parâmetros</h3>
                    <p>Exemplo: <code>render_template('index.html', nome=nome)</code>.</p>
                </div>

                <div class="lesson-section">
                    <h3>Lista de Atividades 2</h3>
                    <ol>
                        <li>Considerando um usuário e uma senha mocados (dados fictícios) faça uma página de autenticação que retorne uma mensagem caso a autenticação funcione (bom dia, tarde, noite a depender do horário), se não, diz que o login não bateu.</li>
                        <li>Limite as tentativas de autenticação do usuário em 2x, se ele errar duas vezes, tire a opção de login e exiba uma mensagem de erro.</li>
                        <li>Estilizar de forma bonita a página de identificação.</li>
                        <li>Escreva um script python que gere automaticamente um template HTML contendo um formulário para input de dados com os campos que serão recebidos por JSON (gerar o .html e o formulário, a outra parte do código recebe os dados em JSON, trata ele e devolve como uma lista de strings).</li>
                        <li>Incremente o script 4 para que após gerar o template, ele construa automaticamente uma rota que permita visualiza-lo.</li>
                        <li>Crie uma classe em python que encapsule dados de usuário entre 5 e 6 campos, e desenvolva uma função de autenticação (validar dados, criar uma sessão para guardar e autenticar).</li>
                    </ol>
                </div>
            """
        },
        {
            "title": "AULA 06 (13/11)",
            "content": """
                <div class="lesson-section">
                    <h3>Regras Básicas</h3>
                    <ul>
                        <li>Validar dados recebidos.</li>
                        <li>Garantir integridade e consistência dos dados.</li>
                        <li>Trabalhar de forma síncrona ou assíncrona.</li>
                        <li>Tratar exceções para evitar falhas no backend.</li>
                    </ul>
                </div>

                <div class="lesson-section">
                    <h3>Lista de Atividades 3</h3>
                    <ol>
                        <li>Fazer todas as validações possíveis para garantir que as informações foram enviadas corretamente pelo usuário.</li>
                        <li>Tratar exceções para evitar que seja exibida a mensagem de erro padrão.</li>
                        <li>Garantir que o usuário seja redirecionado com a possibilidade de fazer a autenticação novamente quando um dos dados estiver incorreto.</li>
                        <li>Limitar em duas tentativas de autenticação errada.</li>
                        <li>Alterar todos os retornos usando dados formatados em json (conjunto chave:valor).</li>
                    </ol>
                </div>
            """
        },
        {
            "title": "Aulas 07-09 (20/11 a 04/12)",
            "content": """
                <div class="lesson-section">
                    <h3>Desenvolvimento Prático</h3>
                    <ul>
                        <li>Tempo para implementar atividades e protótipos do projeto final.</li>
                        <li>Apresentação de protótipos dos grupos (Aula 08).</li>
                    </ul>
                </div>
            """
        },
        {
            "title": "Aula 10 (11/12)",
            "content": """
                <div class="lesson-section">
                    <h3>Preparação para Prova</h3>
                    <ul>
                        <li>Formato definido: distribuição 48h antes.</li>
                        <li>Incentivo à participação em evento cultural (orquestra no campus).</li>
                    </ul>
                </div>
            """
        },
        {
            "title": "AULA 11 (18/12)",
            "content": """
                <div class="lesson-section">
                    <h3>Atividades para Praticar Antes da Prova</h3>
                    <ol>
                        <li>
                            <h4>Mini-blog Pessoal</h4>
                            <p><strong>Objetivo:</strong> Criar uma aplicação simples para postar pequenos textos com data e hora.</p>
                            <p><strong>Funcionalidades:</strong></p>
                            <ul>
                                <li>Formulário para adicionar novos posts.</li>
                                <li>Lista de posts na página inicial, ordenados por data.</li>
                                <li>Utilização de templates para formatar a página.</li>
                            </ul>
                            <p><strong>Dicas:</strong></p>
                            <ul>
                                <li>Utilizar uma lista em Python para armazenar os posts.</li>
                                <li>Usar o módulo datetime para registrar a data e hora de cada post.</li>
                                <li>Criar um template básico com HTML e CSS para estilizar a página.</li>
                            </ul>
                            <p><strong>Tempo:</strong> 30 minutos.</p>
                        </li>
                        <li>
                            <h4>Página de Autenticação Básica</h4>
                            <p><strong>Objetivo:</strong> Criar uma aplicação simples para comparar se o usuário e a senha digitados estão corretos.</p>
                            <p><strong>Funcionalidades:</strong></p>
                            <ul>
                                <li>Formulário para informar usuário e senha.</li>
                                <li>Dicionário para armazenar o usuário e senha cadastrados.</li>
                                <li>Utilização de templates para formatar a página.</li>
                                <li>Retornar mensagens de sucesso ou falha na autenticação.</li>
                            </ul>
                            <p><strong>Dicas:</strong></p>
                            <ul>
                                <li>Utilizar lista para armazenar as tentativas de autenticação.</li>
                                <li>Usar o módulo datetime para registrar a data e hora de login.</li>
                                <li>Criar um template básico com HTML e CSS para estilizar a página.</li>
                            </ul>
                            <p><strong>Tempo:</strong> 30 minutos.</p>
                        </li>
                        <li>
                            <h4>Página de Upload de Fotos</h4>
                            <p><strong>Objetivo:</strong> Criar uma aplicação simples para fazer upload de imagens.</p>
                            <p><strong>Funcionalidades:</strong></p>
                            <ul>
                                <li>Formulário para escolher o arquivo a partir do computador do usuário.</li>
                                <li>Armazenar os arquivos enviados pelos usuários em uma pasta.</li>
                                <li>Utilização de templates para formatar a página.</li>
                                <li>Retornar mensagens de sucesso ou falha na autenticação. Em caso de sucesso, deve-se retornar também o path de onde o arquivo foi armazenado no servidor.</li>
                            </ul>
                            <p><strong>Dicas:</strong></p>
                            <ul>
                                <li>Utilizar lista para armazenar os arquivos enviados.</li>
                                <li>Usar o módulo datetime para registrar a data e hora do upload do arquivo.</li>
                                <li>Criar um template básico com HTML e CSS para estilizar a página.</li>
                            </ul>
                            <p><strong>Tempo:</strong> 30 minutos.</p>
                        </li>
                    </ol>
                </div>
            """
        },
        {
            "title": "Provas e Feedback",
            "content": """
                <div class="lesson-section">
                    <h3>Aulas 12-14 (08-22/01)</h3>
                    <ul>
                        <li>Prova prática dividida em grupos (problemas técnicos adiaram parte das avaliações).</li>
                    </ul>
                </div>

                <div class="lesson-section">
                    <h3>Aula 15 (29/01)</h3>
                    <ul>
                        <li>Feedback final e divulgação de notas.</li>
                    </ul>
                </div>
            """
        }
    ]
    return render_template('lesson_summaries.html', summaries=summaries)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            if not request.is_json:
                abort(400, description="Content-Type deve ser application/json")

            data = request.get_json()

            required_fields = ['user', 'password']
            if not all(field in data for field in required_fields):
                abort(400, description="Campos obrigatórios faltando: user e password")

            username = data['user'].strip()
            password = data['password'].strip()

            if not username or not password:
                return jsonify({
                    'status': 'error',
                    'message': 'Usuário e senha são obrigatórios'
                }), 400

            user = authenticate(username, password)

            if user:
                session['attempts'] = 0
                session['logged_in'] = True
                session['user_id'] = user.user_id

                hora_atual = datetime.now().hour
                saudacao = 'Bom dia' if 5 <= hora_atual < 12 else 'Boa tarde' if 12 <= hora_atual < 18 else 'Boa noite'

                return jsonify({
                    'status': 'success',
                    'message': f'{saudacao}, {user.full_name}! Login bem-sucedido.',
                    'user': user.to_dict()
                })
            else:
                session['attempts'] = session.get('attempts', 0) + 1
                attempts_remaining = 2 - session['attempts']

                if session['attempts'] >= 2:
                    return jsonify({
                        'status': 'error',
                        'message': 'Acesso bloqueado! Tente novamente mais tarde.',
                        'attempts_remaining': 0
                    }), 403

                return jsonify({
                    'status': 'error',
                    'message': 'Credenciais inválidas!',
                    'attempts_remaining': attempts_remaining
                }), 401

        session['attempts'] = 0
        return render_template('/auth/login.html')

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/logout')
def logout_route():
    session.clear()
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    user = next((u for u in users if u.user_id ==
                session.get('user_id')), None)
    if user:
        return render_template('auth/profile.html', user=user.to_dict())
    return redirect(url_for('login'))


@app.route('/activities')
def activities():
    activities_list = [
        {
            "title": "Atividade 1: Canvas Interativo",
            "description": "Implementar movimento de imagem com teclado usando HTML5 Canvas",
            "route": "/activity1"
        },
        {
            "title": "Atividade 2: Captura de Webcam",
            "description": "Desenvolver sistema de captura de imagem via navegador",
            "route": "/activity2"
        },
        {
            "title": "Atividade 3: Tabela Dinâmica",
            "description": "Criar tabela com 997 registros usando divs e CSS grid",
            "route": "/activity3"
        },
        {
            "title": "Atividade 4: Sistema de Login",
            "description": "Implementar autenticação com limite de tentativas e respostas JSON",
            "route": "/login"
        },
        {
            "title": "Atividade 5: Gerador de Formulários",
            "description": "Criação automática de templates HTML a partir de JSON",
            "route": "/form-generator"
        }
    ]
    return render_template('activities.html', activities=activities_list)


@app.route('/activity1')
def activity1():
    return render_template('activities/activity1.html')


@app.route('/activity2')
def activity2():
    return render_template('activities/activity2.html')


@app.route('/activity3')
def activity3():
    return render_template('activities/activity3.html')


grades = [
    {"id": 1, "student": "João Silva", "subject": "Matemática", "grade": 9.5},
    {"id": 2, "student": "Maria Oliveira", "subject": "História", "grade": 8.7}
]


@app.route('/grades')
def grades_index():
    sorted_grades = sorted(grades, key=lambda x: x['grade'], reverse=True)
    return render_template('grades/index.html', grades=sorted_grades)


@app.route('/grades/add', methods=['GET', 'POST'])
def grades_add():
    if request.method == 'POST':
        new_id = max(g['id'] for g in grades) + 1 if grades else 1
        new_grade = {
            "id": new_id,
            "student": request.form['student'],
            "subject": request.form['subject'],
            "grade": float(request.form['grade'])
        }
        grades.append(new_grade)
        flash('Nota adicionada com sucesso!', 'success')
        return redirect(url_for('grades_index'))
    return render_template('grades/add.html')


@app.route('/grades/delete/<int:id>')
def grades_delete(id):
    global grades
    grades = [g for g in grades if g['id'] != id]
    flash('Nota excluída com sucesso!', 'info')
    return redirect(url_for('grades_index'))


@app.route('/grades/edit/<int:id>', methods=['GET', 'POST'])
def grades_edit(id):
    grade = next((g for g in grades if g['id'] == id), None)
    if not grade:
        flash('Nota não encontrada!', 'error')
        return redirect(url_for('grades_index'))

    if request.method == 'POST':
        grade.update({
            "student": request.form['student'],
            "subject": request.form['subject'],
            "grade": float(request.form['grade'])
        })
        flash('Nota atualizada com sucesso!', 'success')
        return redirect(url_for('grades_index'))

    return render_template('grades/edit.html', grade=grade)


@app.route('/mini_blog', methods=['GET', 'POST'])
def mini_blog():
    if request.method == 'POST':
        post_content = request.form.get('content')
        if post_content:
            new_post = {
                'content': post_content,
                'timestamp': datetime.now().isoformat()
            }
            posts.append(new_post)
    return render_template('practice_test/mini_blog.html', posts=sorted(posts, key=lambda x: x['timestamp'], reverse=True))


@app.route('/basic_auth', methods=['GET', 'POST'])
def basic_auth():
    if request.method == 'GET' and not session.get('from_post'):
        session['auth_attempts'] = 0

    message = session.pop('auth_message', None)
    attempts = session.get('auth_attempts', 0)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if auth_users.get(username) == password:
            session['auth_attempts'] = 0
            session['auth_message'] = 'Autenticação bem-sucedida!'
        else:
            session['auth_attempts'] = attempts + 1
            session['auth_message'] = 'Credenciais inválidas!'

        session['from_post'] = True
        return redirect(url_for('basic_auth'))

    if 'from_post' in session:
        session.pop('from_post')

    return render_template('practice_test/basic_auth.html',
                           message=message,
                           attempts=session.get('auth_attempts', 0))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


@app.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            file.save(file_path)

            new_upload = {
                'filename': filename,
                'path': file_path,
                'timestamp': datetime.now().isoformat()
            }
            uploaded_files.append(new_upload)
            return render_template('practice_test/file_upload.html', success=True, file=new_upload)

    return render_template('practice_test/file_upload.html', success=False)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


app.secret_key = 'abacate'


def authenticate(username, password):
    user = next((u for u in users if u.username ==
                username and u.is_active), None)
    if user and user.verify_password(password):
        session['user_id'] = user.user_id
        session['logged_in'] = True
        session['attempts'] = 0
        return user
    return None


def get_current_user():
    if 'user_id' in session:
        user_id = session['user_id']
        return next((u for u in users if u.user_id == user_id), None)
    return None


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def handle_errors(e):
    return jsonify({
        'status': 'error',
        'message': e.description if hasattr(e, 'description') else str(e)
    }), e.code


generated_templates: dict[str, str] = {}


@app.route('/form-generator', methods=['GET', 'POST'])
def form_generator():
    if request.method == 'POST':
        data = request.get_json()
        fields = data.get('fields', [])

        if not fields:
            return jsonify({'error': 'No fields provided'}), 400

        template_name = f'form_{len(generated_templates) + 1}'
        generated_templates[template_name] = render_template(
            'form/generated_form.html', fields=fields)

        return jsonify({'status': 'success', 'template_url': f'/generated/{template_name}'})

    return render_template('form/form_generator.html')


@app.route('/generated/<template_name>')
def generated_form(template_name):
    template_content = generated_templates.get(template_name)
    if not template_content:
        return jsonify({'error': 'Template not found'}), 404
    return template_content


@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    processed_data = [f"{key}: {value}" for key, value in data.items()]

    return jsonify({'status': 'success', 'data': processed_data})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
