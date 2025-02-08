# Sistema de Gestão Acadêmica com Flask

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Um sistema completo para gestão de atividades acadêmicas, resumos de aulas e avaliações, desenvolvido com Flask e tecnologias web modernas.

## 📋 Recursos Principais

- Sistema de autenticação de usuários
- Gestão de atividades práticas
- Upload de arquivos com validação
- Blog integrado para posts rápidos
- Sistema de notas completo (CRUD)
- Resumos organizados das aulas
- Gerenciamento de sessões
- API básica para formulários
- Interface responsiva e moderna

## 🚀 Começando

### Pré-requisitos

- Python 3.11 ou superior
- pip (Gerenciador de pacotes Python)
- Navegador moderno (Chrome, Firefox, Edge)

### Instalação

1. **Clonar o repositório**
   ```bash
   git clone https://github.com/seu-usuario/seu-projeto.git
   cd seu-projeto
   Criar ambiente virtual (recomendado)
   ```

bash
Copy
python -m venv venv
Ativar ambiente virtual

Windows:

bash
Copy
.\venv\Scripts\activate
Linux/MacOS:

bash
Copy
source venv/bin/activate
Instalar dependências

bash
Copy
pip install -r requirements.txt
Configuração
Criar arquivo de configuração (.env)

env
Copy
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
UPLOAD_FOLDER=uploads
Criar diretório para uploads

bash
Copy
mkdir uploads
Executando a Aplicação
bash
Copy
flask run

# ou

python app.py
A aplicação estará disponível em: http://localhost:5000

📂 Estrutura do Projeto
Copy
projeto-flask/
├── app.py
├── config.py
├── requirements.txt
├── uploads/
├── static/
│ ├── css/
│ │ ├── styles.css
│ │ ├── activities.css
│ │ └── lesson_summaries.css
│ └── js/
├── templates/
│ ├── includes/
│ ├── activities/
│ ├── auth/
│ ├── grades/
│ └── practice_test/
└── venv/
📦 Dependências Principais
Flask

Werkzeug

python-dotenv

Font Awesome (via CDN)

Lista completa em requirements.txt

🖥 Como Usar
Página Inicial

Acesse http://localhost:5000

Navegação principal através do menu

Rotas Principais

/: Página inicial

/activities: Lista de atividades

/lesson_summaries: Resumos das aulas

/login: Sistema de autenticação

/grades: Sistema de gestão de notas

Autenticação

Usuários padrão:

admin / 1234

usuario / 123456

Upload de Arquivos

Formatos permitidos: PNG, JPG, JPEG, GIF

Tamanho máximo: 5MB

👨💻 Desenvolvimento
Modo Debug

bash
Copy
FLASK_DEBUG=1 flask run
Testando Rotas

python
Copy
pytest tests/
Contribuição

Faça fork do projeto

Crie uma branch para sua feature

bash
Copy
git checkout -b feature/nova-feature
Faça commit das mudanças

bash
Copy
git commit -m 'Adiciona nova feature'
Push para a branch

bash
Copy
git push origin feature/nova-feature
Abra um Pull Request

🛠 Troubleshooting
Problema: Porta 5000 em uso
Solução:

bash
Copy
flask run --port=5001
Problema: Dependências não instaladas
Solução:

bash
Copy
pip install -r requirements.txt --force-reinstall
Problema: Erros de upload de arquivos
Solução:

bash
Copy
chmod 755 uploads
📄 Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

🙌 Créditos
Desenvolvido por [Seu Nome]

Template base por [Nome do Template]

Ícones por Font Awesome
