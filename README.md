# Ferramenta de Mapeamento Automático de Ocorrências

## 📜 Visão Geral

Esta é uma aplicação web desenvolvida em Python com Streamlit que automatiza o processo de classificação e mapeamento de ocorrências textuais. A ferramenta foi projetada para resolver um problema comum em áreas de atendimento, qualidade e operações: a necessidade de associar manualmente um grande volume de "Fatos Geradores" (descrições de eventos, reclamações, etc.) a uma lista padronizada de "Problemas".

Utilizando técnicas de Processamento de Linguagem Natural (NLP), a aplicação analisa o conteúdo de dois arquivos fornecidos pelo utilizador e gera uma tabela "DE-PARA" que correlaciona cada fato gerador ao problema mais relevante, economizando horas de trabalho manual e aumentando a consistência da classificação.

---

## ✨ Funcionalidades Principais

* **Interface Web Interativa:** Interface simples e intuitiva que não exige conhecimento de programação para ser utilizada.
* **Upload Flexível de Ficheiros:** Suporte para o carregamento de ficheiros nos formatos `.csv` e `.xlsx`.
* **Análise Automatizada:** Mapeamento realizado com um único clique após o upload dos ficheiros.
* **Visualização de Resultados:** Apresentação de uma amostra dos resultados e um resumo dos problemas mais recorrentes diretamente no ecrã.
* **Exportação de Dados:** Geração de um ficheiro `.xlsx` com o mapeamento completo para download e análise posterior.

---

## ⚙️ Como Funciona

O processo de mapeamento é realizado através das seguintes etapas:

1.  **Carregamento e Preparação dos Dados:** O utilizador carrega dois ficheiros: um contendo os "Fatos Geradores" e outro com a lista de "Problemas". O código combina as colunas textuais dos fatos geradores para criar um contexto mais rico para cada ocorrência.
2.  **Aplicação de Regras de Negócio:** Uma regra específica é aplicada para filtrar e remover categorias de problemas que não são relevantes para a análise (neste caso, problemas iniciados com o código "14").
3.  **Vetorização de Texto (TF-IDF):** A técnica **TF-IDF (Term Frequency-Inverse Document Frequency)** é utilizada para converter cada texto (tanto dos fatos geradores quanto dos problemas) num vetor numérico. Essa representação permite que o computador entenda a importância de cada palavra no contexto dos documentos.
4.  **Cálculo de Similaridade de Cossenos:** Para cada fato gerador, o sistema calcula a **similaridade de cossenos** entre o seu vetor e os vetores de todos os problemas. Essa métrica determina quão "próximos" em significado os textos são.
5.  **Mapeamento Final:** O problema que apresentar a maior pontuação de similaridade é associado ao respetivo fato gerador, criando a tabela final de-para.

---

## 🚀 Como Executar o Projeto Localmente

Para executar esta aplicação na sua máquina, siga os passos abaixo.

### Pré-requisitos

* Python 3.8 ou superior instalado.

### 1. Clone o Repositório

```bash
git clone [https://github.com/ofuislelipe/Synapse-fgeradores.git](https://github.com/ofuislelipe/Synapse-fgeradores.git)
cd Synapse-fgeradores
```

### 2. Crie um Ambiente Virtual (Recomendado)

É uma boa prática isolar as dependências do projeto.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

As bibliotecas necessárias estão listadas no ficheiro requirements.txt. Instale todas com um único comando:

```bash
pip install -r requirements.txt
```

### 4. Execute a Aplicação Streamlit

Com as dependências instaladas, inicie a aplicação:

```bash
streamlit run app.py
```

O seu navegador padrão abrirá automaticamente no endereço <http://localhost:8501> com a aplicação em funcionamento.

### 💻 Tecnologias Utilizadas

* **Streamlit:** Para a criação da interface web interativa.
* **Pandas:** Para manipulação e processamento dos dados.
* **Scikit-learn:** Para a implementação do TF-IDF e cálculo da similaridade de cossenos.
