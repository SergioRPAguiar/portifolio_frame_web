# Portfólio de Frameworks Web com Flask

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)

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
    git clone https://github.com/SergioRPAguiar/portifolio_frame_web
    ```
   ```bash
   cd seu-projeto
    

2. **Criar ambiente virtual (recomendado)**
    ```bash
    python -m venv .venv

3. **Ativar ambiente virtual**
    #### Windows:
       .\.venv\Scripts\activate
    
    #### Linux/MacOS:
       source venv/bin/activate

5. **Instalar dependências**
    ```bash
    pip install -r requirements.txt
    
### Configuração

1. **Criar arquivo de configuração (.env)**
   ```env
   SECRET_KEY=sua_chave_secreta_aqui
   DEBUG=True
   UPLOAD_FOLDER=uploads

2. **Criar diretório para uploads**
    ```bash
    mkdir uploads

### Executando a Aplicação
    python app.py

- A aplicação estará disponível em: http://localhost:5000

## 🖥 Como Usar
1. **Página Inicial**
  - Acesse http://localhost:5000
  - Navegação principal através do menu

2. **Rotas Principais**
   - /: Página inicial
   - /activities: Lista de atividades
   - /lesson_summaries: Resumos das aulas
   - /login: Sistema de autenticação
   - /grades: Sistema de gestão de notas

3. **Para teste de autenticação no site**
   - Usuários padrão:
     - admin (usuário) / 1234 (senha)
     - usuario (usuário) / 123456 (senha)

4. **Upload de Arquivos**
   - Formatos permitidos: PNG, JPG, JPEG, GIF
   - Tamanho máximo: 5MB
    
## 🙌 Créditos

- Desenvolvido por Sérgio Roberto Paro Aguiar
- Design e implementação original
