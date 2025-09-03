import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import io

# --- Configuração da Página ---
st.set_page_config(page_title="Mapeamento Automático", layout="wide")

# --- Título e Descrição ---
st.title(" Ferramenta de Mapeamento Automático 🤖")
st.markdown("""
    Esta aplicação utiliza um modelo de análise de texto para criar uma tabela "DE-PARA", 
    associando uma lista de **Fatos Geradores** a uma lista de **Problemas**.
""")
st.markdown("---")

# --- Painel de Carregamento de Ficheiros ---
st.subheader("1. Carregue os seus ficheiros de dados")
col1, col2 = st.columns(2)

with col1:
    uploaded_fatos = st.file_uploader("Carregue o ficheiro de Fatos Geradores (CSV ou XLSX)", type=["csv", "xlsx"])

with col2:
    uploaded_problemas = st.file_uploader("Carregue o ficheiro de Problemas (CSV ou XLSX)", type=["csv", "xlsx"])

# --- Função para carregar dados (CSV ou Excel) ---
def load_data(file):
    if file is None:
        return None
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)
    except Exception as e:
        st.error(f"Erro ao ler o ficheiro: {e}")
        return None

# --- Lógica da Aplicação ---
if uploaded_fatos is not None and uploaded_problemas is not None:
    
    # Botão para iniciar a análise
    if st.button("Realizar Mapeamento", type="primary"):
        with st.spinner('A analisar os dados... Este processo pode demorar um momento.'):
            
            # Carregar os dados usando a função auxiliar
            df_fatos = load_data(uploaded_fatos)
            df_problemas = load_data(uploaded_problemas)

            if df_fatos is not None and df_problemas is not None:
                # --- Início da Lógica de Análise ---
                
                # 2. Preparar os Dados e Aplicar a Regra de Negócio
                df_problemas.dropna(subset=['Problema'], inplace=True)
                df_problemas_filtrado = df_problemas[~df_problemas['Problema'].astype(str).str.strip().str.startswith('14')].copy()
                
                df_fatos.dropna(subset=['Motivo__c', 'Natureza__c', 'Name'], inplace=True)
                df_fatos['texto_completo'] = df_fatos['Motivo__c'].astype(str) + '. ' + \
                                             df_fatos['Natureza__c'].astype(str) + '. ' + \
                                             df_fatos['Name'].astype(str)
                
                # 3. Vetorização com TF-IDF
                vectorizer = TfidfVectorizer()
                all_texts = pd.concat([df_problemas_filtrado['Problema'], df_fatos['texto_completo']], ignore_index=True)
                vectorizer.fit(all_texts)
                tfidf_problemas = vectorizer.transform(df_problemas_filtrado['Problema'])
                tfidf_fatos = vectorizer.transform(df_fatos['texto_completo'])

                # 4. Calcular a Similaridade
                cosine_scores = cosine_similarity(tfidf_fatos, tfidf_problemas)
                best_match_indices = cosine_scores.argmax(axis=1)
                best_match_scores = cosine_scores[np.arange(len(best_match_indices)), best_match_indices]

                # 5. Criar o DataFrame de resultados
                df_resultado = df_fatos.copy()
                df_resultado['problema_mapeado'] = df_problemas_filtrado['Problema'].iloc[best_match_indices].values
                df_resultado['similaridade'] = best_match_scores
                
                # --- Fim da Lógica de Análise ---

                st.success('Análise concluída com sucesso!')
                
                # --- Exibição dos Resultados ---
                st.markdown("---")
                st.subheader("Amostra do Resultado do Mapeamento")
                st.dataframe(df_resultado[['Motivo__c', 'Natureza__c', 'Name', 'problema_mapeado', 'similaridade']].head(10))
                
                st.subheader("Resumo da Análise")
                top_problemas = df_resultado['problema_mapeado'].value_counts().nlargest(5)
                st.write("Os 5 problemas mais frequentemente mapeados foram:")
                st.dataframe(top_problemas)

                # --- Lógica para Download do Ficheiro Completo ---
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_resultado[['Motivo__c', 'Natureza__c', 'Name', 'problema_mapeado', 'similaridade']].to_excel(writer, index=False, sheet_name='Mapeamento')
                
                processed_data = output.getvalue()

                st.download_button(
                    label="📥 Baixar Resultado Completo (Excel)",
                    data=processed_data,
                    file_name='mapeamento_final.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                )
else:
    st.info("Por favor, carregue ambos os ficheiros para habilitar a análise.")