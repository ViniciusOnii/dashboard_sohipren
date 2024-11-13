import pandas as pd
import streamlit as st

def add_data():
    try:
        # Carrega o arquivo Excel da planilha de vendas
        df = pd.read_excel("base_2.xlsx")  # Substitua pelo caminho correto do seu arquivo
        

        # Formulário para entrada de dados com Streamlit
        with st.form("form_sales", clear_on_submit=True):
            # Campos de entrada para cada coluna da planilha
            col1, col2, col3 = st.columns(3)
            nf = col1.number_input("NF", min_value=0)
            st_field = col2.text_input("ST")
            cfop = col3.selectbox("CFOP", df["CFOP"].unique())
            
            col4, col5 = st.columns(2)
            emissao = col4.date_input("Data de Emissão")
            vendedor = col5.text_input("Vendedor")
            
            col6, col7 = st.columns(2)
            cliente = col6.selectbox("Razão Social Cliente", df["RAZÃO SOCIAL CLIENTE"].unique())
            uf = col7.selectbox("UF", df["UF"].unique())
            
            col8, col9 = st.columns(2)
            codigo_material = col8.selectbox("Código do Material", df["CÓD.MAT."].unique())
            descricao_material = col9.selectbox("Descrição do Material", df["DESCRIÇÃO MATERIAL"].unique())
            
            col10, col11, col12 = st.columns(3)
            unidade_medida = col10.text_input("Unidade de Medida", value="UN")
            quantidade = col11.number_input("Quantidade", min_value=1)
            valor_unitario = col12.number_input("Valor Unitário", min_value=0.0)
            
            # Campo calculado para Valor Total
            valor_total = quantidade * valor_unitario
            
            # Botão de envio
            btn = st.form_submit_button("Salvar Dados no Excel", type="primary")
            
            # Validação e salvamento dos dados
            if btn:
                # Verifica se campos obrigatórios estão preenchidos
                if not nf or not st_field or not cfop or not emissao or not cliente or not uf or not codigo_material or not descricao_material or quantidade <= 0 or valor_unitario <= 0.0:
                    st.warning("Todos os campos são obrigatórios")
                    return False
                else:
                    # Cria um novo DataFrame com os dados inseridos
                    new_data = pd.DataFrame.from_records([{
                        'NF': nf,
                        'ST': st_field,
                        'CFOP': cfop,
                        'EMISSÃO': emissao,
                        'VEND.': vendedor,
                        'RAZÃO SOCIAL CLIENTE': cliente,
                        'UF': uf,
                        'CÓD.MAT.': codigo_material,
                        'DESCRIÇÃO MATERIAL': descricao_material,
                        'UNID. MEDIDA': unidade_medida,
                        'QUANTIDADE': quantidade,
                        'VALOR UNITÁRIO': float(valor_unitario),
                        'VALOR TOTAL': float(valor_total),
                    }])
                    
                    # Concatena o novo registro ao DataFrame original
                    df = pd.concat([df, new_data], ignore_index=True)
                    
                    # Salva o DataFrame atualizado em um novo arquivo Excel
                    try:
                        df.to_excel("sales_updated.xlsx", index=False)
                        st.success(f"O produto '{descricao_material}' foi adicionado com sucesso!")
                        return True
                    except:
                        st.warning("Não foi possível salvar o arquivo. Por favor, feche o arquivo antes de tentar novamente.")
                        return False
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")

# Chama a função principal para exibir o formulário

