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
- Git

### Instalação
1. **Iniciar prompt de comando**
   #### Windows:
    - Pressionar as teclas Windows + R ao mesmo tempo
    - Digitar "cmd" na caixa Executar e apertar enter no teclado
   #### Linux:
    - Pressionar as teclas Ctrl + Alt + T ao mesmo tempo
2. **Clonar o repositório**
   - Já no terminal, siga os próximos passos, copiando os códigos, colando no terminal e pressionando Enter em cada passo
     
    ```bash
    git clone https://github.com/SergioRPAguiar/portifolio_frame_web
    ```
   ```bash
   cd portifolio_frame_web 
4. **Criar e Ativar ambiente virtual**
    #### Windows:
       python -m venv .venv
    ```
    .\.venv\Scripts\activate
    ```
    
    #### Linux:
       python3 -m venv .venv
   ```
   source .venv/bin/activate
   ```

5. **Instalar dependências**
    ```bash
    pip install -r requirements.txt
    
### Configuração

1. **Criar arquivo de configuração (.env)**
   #### Windows:
       echo SECRET_KEY=sua_chave_secreta_aqui > .env
       echo DEBUG=True >> .env
       echo UPLOAD_FOLDER=uploads >> .env
   
   #### Linux:
   ```bash
   echo "SECRET_KEY=sua_chave_secreta_aqui" > .env
   echo "DEBUG=True" >> .env
   echo "UPLOAD_FOLDER=uploads" >> .env

3. **Criar diretório para uploads**
    ```bash
    mkdir uploads

### Executando a Aplicação
    python app.py

- A aplicação estará disponível em: http://localhost:5000

## 🖥 Como Usar
1. **Página Inicial**
  - Acesse http://localhost:5000 no seu navegador
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
