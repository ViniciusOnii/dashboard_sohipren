import streamlit as st
import pandas as pd
from data_manager import DataManager

def main():
    st.title("Gestão de Manutenção e Peças")
    
    # Inicializa o gerenciador de dados
    data_manager = DataManager()
    
    # Sidebar para navegação
    pagina = st.sidebar.radio(
        "Selecione a Página",
        ["Manutenção", "Comparações", "Estado das Peças"]
    )
    
    if pagina == "Manutenção":
        st.header("Registros de Manutenção")
        
        # Formulário para adicionar novo registro
        with st.form("novo_registro"):
            st.subheader("Novo Registro de Manutenção")
            
            peca = st.text_input("Peça")
            tipo_manutencao = st.selectbox(
                "Tipo de Manutenção",
                ["Preventiva", "Corretiva", "Preditiva"]
            )
            descricao = st.text_area("Descrição")
            custo = st.number_input("Custo (R$)", min_value=0.0)
            
            if st.form_submit_button("Registrar"):
                registro = {
                    "peca": peca,
                    "tipo_manutencao": tipo_manutencao,
                    "descricao": descricao,
                    "custo": custo
                }
                data_manager.add_maintenance_record(registro)
                st.success("Registro adicionado com sucesso!")
        
        # Exibe histórico
        historico = data_manager.get_maintenance_history()
        if historico:
            st.subheader("Histórico de Manutenção")
            df = pd.DataFrame(historico)
            st.dataframe(df)
        else:
            st.info("Nenhum registro de manutenção encontrado.")
            
    elif pagina == "Comparações":
        st.header("Histórico de Comparações")
        
        # Formulário para adicionar nova comparação
        with st.form("nova_comparacao"):
            st.subheader("Nova Comparação")
            
            item1 = st.text_input("Item 1")
            item2 = st.text_input("Item 2")
            diferenca = st.number_input("Diferença", format="%.2f")
            
            if st.form_submit_button("Registrar Comparação"):
                data_manager.add_comparison(item1, item2, diferenca)
                st.success("Comparação registrada com sucesso!")
        
        # Exibe histórico de comparações
        historico = data_manager.get_comparison_history()
        if not historico.empty:
            st.subheader("Histórico de Comparações")
            st.dataframe(historico)
        else:
            st.info("Nenhuma comparação registrada.")
            
    else:  # Estado das Peças
        st.header("Estado das Peças")
        
        # Formulário para atualizar estado
        with st.form("atualizar_estado"):
            st.subheader("Atualizar Estado da Peça")
            
            part_id = st.text_input("ID da Peça")
            status = st.selectbox(
                "Status",
                ["Novo", "Em Uso", "Necessita Manutenção", "Em Manutenção", "Descartado"]
            )
            
            if st.form_submit_button("Atualizar"):
                data_manager.update_part_status(part_id, status)
                st.success("Status atualizado com sucesso!")
        
        # Exibe estado atual das peças
        estados = data_manager.get_part_status()
        if estados:
            st.subheader("Estado Atual das Peças")
            df = pd.DataFrame.from_dict(estados, orient='index')
            st.dataframe(df)
        else:
            st.info("Nenhuma peça cadastrada.")

if __name__ == "__main__":
    main() 