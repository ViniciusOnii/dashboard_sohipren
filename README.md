## Passo a Passo de Instalação
1. **Baixar o Projeto**
   - Clique no botão verde "Code" no GitHub e selecione "Download ZIP" para baixar o projeto, ou clone-o usando o comando:
     ```bash
     git clone https://github.com/seu_usuario/nome_do_projeto.git
     ```
   - Extraia os arquivos do ZIP, caso tenha baixado dessa forma.

2. **Abrir o Projeto no VS Code**
   - No VS Code, vá em **File** > **Open Folder** e selecione a pasta do projeto.

3. **Criar e Ativar o Ambiente Virtual**
   - No terminal do VS Code, navegue até a pasta do projeto, caso ainda não esteja nela:
     ```bash
     cd caminho/para/a/pasta_do_projeto
     ```
   - Crie um ambiente virtual com o comando:
     ```bash
     python -m venv v
     ```
   - **Ativar o ambiente virtual**:
     - **Windows**:
       ```bash
       v\Scripts\activate
       ```
     - **Linux/Mac**:
       ```bash
       source v/bin/activate
       ```

4. **Instalar as Bibliotecas do `requirements.txt`**
   - Com o ambiente virtual ativo, instale todas as bibliotecas necessárias com o comando:
     ```bash
     pip install -r requirements.txt
     ```

5. **Organizar as Imagens na Pasta `assets`**
   - Certifique-se de que todas as imagens do projeto estão na pasta `assets`. Se não existir, crie a pasta com o nome `assets` na raiz do projeto e mova as imagens para essa pasta.

6. **Executar o Projeto com o Streamlit**
   - Para iniciar o projeto, rode o seguinte comando:
     ```bash
     streamlit run main.py
     ```

7. **Acessar o Projeto no Navegador**
   - Após rodar o comando acima, o Streamlit abrirá automaticamente no navegador. Caso contrário, você pode acessar o projeto manualmente pelo link que aparecerá no terminal, como `http://localhost:8501`.

## Estrutura do Projeto


----------------------------------------------------------------------------------------------
🕐 VISUALIZE DADOS DO EXCEL COM PYTHON | PAINEL ANALÍTICO PARA WEB USANDO STREAMLIT
🕐 TRANSFORME DADOS EM CONHECIMENTO

NOTA: O mundo dos negócios hoje é altamente competitivo. Quem utiliza tecnologia avançada terá sucesso no mercado. Para competir no ambiente de negócios atual, é necessário investir em Sistemas de Informação, especialmente em Sistemas de Decisão Baseados em Inteligência de Negócios.

📌 No mundo de hoje, os negócios são geridos usando sistemas computacionais, o que leva a altos lucros e maior longevidade no mercado.

📌 Esses sistemas computacionais trabalham para transformar dados em conhecimento, permitindo decisões rápidas e fáceis com grande eficiência.

📌 Vamos aprender a criar um Painel de Análise usando dados do Microsoft Excel como fonte. Usaremos a linguagem de programação Python, CSS, HTML e a biblioteca Streamlit para criar um painel de análise visualmente atraente e dinâmico para a web.

📌 Você pode usar a lição de hoje como base para criar seu próprio sistema com os dados que você possui.

Página inicial | Gráfico de barras, gráfico de pontos, histograma, gráfico de dispersão, métricas analíticas
![image](https://github.com/user-attachments/assets/b01a4fbe-03b5-4fae-9caf-434db138e25e)

Página inicial2 | Gráfico de barras, gráfico de pontos, histograma, gráfico de dispersão, métricas analíticas
![image](https://github.com/user-attachments/assets/e4eb9313-e725-44a0-8b7e-bebbca85d03a)


DataFrame exibe dados do arquivo Excel com dataframe filtrado
![image](https://github.com/user-attachments/assets/2f040200-19ab-4c9f-8609-450d2c15cf94)


Gráficos:
DESCRIÇÃO MATERIAL & VALOR TOTAL:

![image](https://github.com/user-attachments/assets/6b31886c-f6cb-4d76-a008-2850d7592285)

Descrição dos Produtos & Quantidade:

![image](https://github.com/user-attachments/assets/e187babe-c510-4ba4-886f-19784c30dd0d)

Atributos por Frequência:

![image](https://github.com/user-attachments/assets/4809cc40-aaeb-49e1-905d-900c0b1bd9a5)

DESCRIÇÃO MATERIAL & QUANTIDADE:

![image](https://github.com/user-attachments/assets/fed1796a-e7b9-45b6-b12c-e36870baa542)
