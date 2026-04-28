  💰 Controle de Finanças

Aplicação web para gerenciamento financeiro pessoal, com foco em **controle de gastos por categoria**, **limites personalizados** e **visualização clara de dados**.

---

  🚀 Visão Geral

O objetivo deste projeto é oferecer uma forma simples e eficiente de:

* Registrar receitas e despesas
* Categorizar gastos
* Definir limites por categoria
* Acompanhar o quanto já foi gasto
* Visualizar dados com gráficos

Além de ser uma ferramenta pessoal, este projeto também foi desenvolvido como **portfólio**, aplicando conceitos reais de desenvolvimento de software.

---

  🧠 Principais Funcionalidades

* ✔️ Cadastro de transações (entrada e saída)
* ✔️ Comentários em cada transação
* ✔️ Categorias personalizadas
* ✔️ Definição de limites por categoria
* ✔️ Alertas ao atingir limites de gasto
* ✔️ Dashboard com gráficos
* ✔️ Persistência de dados (JSON)
* ✔️ Interface interativa com Streamlit

---

  🖥️ Preview

> *(adicione aqui prints do seu app rodando)*

---

  🏗️ Arquitetura do Projeto

```bash
finance_app/
│
├── app.py            # Interface (Streamlit)
├── services/         # Regras de negócio
├── models/           # Estrutura dos dados
├── storage/          # Persistência (JSON)
├── data.json         # Transações
├── limites.json      # Limites por categoria
```

---

  ⚙️ Tecnologias Utilizadas

* Python
* Streamlit
* JSON (persistência de dados)

---

  🧩 Decisões Técnicas

* Uso de **JSON** para simplicidade e aprendizado inicial
* Separação entre **interface e lógica** para melhor organização
* Implementação de **regras de negócio (limites)** para simular aplicações reais
* Estrutura modular visando futura migração para banco de dados

---

  📊 Funcionalidade de Limites

O sistema permite definir um limite de gasto por categoria, exibindo:

* Valor já gasto
* Limite definido
* Valor restante

Além disso, o sistema fornece feedback visual:

* 🟢 Seguro
* 🟡 Atenção (acima de 80%)
* 🔴 Limite ultrapassado

---

  🔄 Melhorias Futuras

* [ ] Sistema de autenticação (login de usuários)
* [ ] Banco de dados (SQLite/PostgreSQL)
* [ ] Filtro por período (data)
* [ ] Deploy online
* [ ] Versão mobile

---

  ▶️ Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/controle_de_financas.git
cd controle_de_financas
```

### 2. Criar ambiente virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```bash
pip install streamlit
```

### 4. Executar o projeto

```bash
streamlit run app.py
```

---

  🎯 Objetivo do Projeto

Este projeto foi desenvolvido para:

* Praticar desenvolvimento com Python
* Aplicar conceitos de lógica e estrutura de dados
* Simular um sistema real com regras de negócio
* Servir como base para evolução para aplicações maiores

---

  📌 Status

🚧 Em desenvolvimento — melhorias contínuas sendo adicionadas

---

  👨‍💻 Autor

Desenvolvido por **João Dantas**
GitHub: https://github.com/joaordantas
