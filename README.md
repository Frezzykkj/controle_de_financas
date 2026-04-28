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

<img width="946" height="696" alt="{52ED988D-3014-4770-B607-AD5E86E65D45}" src="https://github.com/user-attachments/assets/3e7c5304-ab81-4d71-ac80-dc07239afaa7" />
<img width="806" height="544" alt="{67DAE384-BFEB-4C7C-BF68-A2B083980249}" src="https://github.com/user-attachments/assets/5b6be0a1-1229-463a-9f69-ab635c4c10b4" />
<img width="800" height="458" alt="{AFC45BC1-DDEC-453C-A909-F92DA8D7D5EB}" src="https://github.com/user-attachments/assets/b06d27ec-a5d4-4e6a-a9ff-589b92367859" />
<img width="763" height="836" alt="{ECCCA1D9-30D7-40DD-AF7D-B2F4E2BE26B8}" src="https://github.com/user-attachments/assets/9144c1d6-d3a1-441a-92b0-cbe6b2bc8dfd" />


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
git clone https://github.com/joaordantas/controle_de_financas.git
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
streamlit run streamlit_app.py
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
