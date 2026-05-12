# 💰 Controle de Finanças

Sistema web desenvolvido com Python + Streamlit para controle financeiro pessoal e gestão de serviços/vendas para autônomos.

O projeto começou como um simples controle financeiro pessoal e está evoluindo para um mini ERP focado em:
- organização financeira
- controle de vendas
- cobranças
- parcelamentos
- relatórios de lucro
- multiusuário

---

# 🚀 Tecnologias Utilizadas

- Python
- Streamlit
- SQLite
- Pandas

---

# 📌 Funcionalidades Atuais

## 🔐 Sistema de Login
- Cadastro de usuários
- Login individual
- Sessão por usuário
- Isolamento de dados por conta

---

## 💰 Financeiro
- Adicionar entradas e saídas
- Histórico de transações
- Categorias financeiras
- Controle de saldo
- Limites financeiros
- Banco de dados SQLite

---

## 🛠 Serviços e Vendas
- Cadastro de vendas/serviços
- Controle de clientes
- Parcelamento de vendas
- Controle de parcelas pagas e pendentes
- Histórico de cobranças
- Integração automática com financeiro

---

## 📊 Relatórios
- Controle de lucro
- Organização financeira por período
- Estrutura para:
  - diário
  - semanal
  - mensal

---

# 🧠 Objetivo do Projeto

Criar uma plataforma simples e eficiente para:
- autônomos
- vendedores
- pequenos prestadores de serviço

Com foco em:
- facilidade de uso
- organização financeira
- controle de cobranças
- produtividade

---

# 🏗 Estrutura Atual do Projeto

```bash
controle_de_financas/
│
├── app.py
├── database.py
├── storage/
│   └── banco.db
├── requirements.txt
└── README.md

🔥 Funcionalidades em Desenvolvimento

📌 UX e Interface
Sidebar profissional
Dashboard financeiro
Melhor experiência visual
Sistema sem IDs manuais

📌 Gestão Avançada
Categorias personalizadas
Limites mensais dinâmicos
Dashboard de faturamento
Controle de lucro diário/semanal/mensal

📌 Serviços
Perfil de autônomo
Áreas de atuação
Sistema de cobranças
Alertas de pagamentos pendentes

📌 Arquitetura
Separação em services/repositories
Melhor organização de código
Escalabilidade do sistema

📷 Preview
Tela Financeira
Controle de entradas e saídas
Histórico financeiro
Limites financeiros
Tela de Serviços
Cadastro de vendas
Parcelas
Controle de cobranças 

▶️ Como Executar o Projeto

1. Clone o repositório:
git clone https://github.com/joaordantas/controle_de_financas.git

2. Entre na pasta:
cd controle_de_financas

3. Instale as dependências:
pip install -r requirements.txt

4. Execute o projeto:
streamlit run app.py

🌐 Deploy

O projeto está hospedado via Streamlit Cloud.

📈 Status do Projeto

🚧 Em desenvolvimento contínuo.

Atualmente focado em:

estabilidade
multiusuário
integração entre módulos
experiência do usuário
👨‍💻 Desenvolvedor

João Dantas

GitHub:
https://github.com/joaordantas

📌 Observação

Este projeto está sendo utilizado tanto como:

projeto pessoal
estudo de engenharia de software
construção de portfólio
possível produto SaaS futuro
