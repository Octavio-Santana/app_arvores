import base64
import folium
import pandas as pd
import streamlit as st
from datetime import datetime
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Read DataSet
df = pd.read_csv('data/data.csv')
select_id = list(df['ID'].values)

# Read TREEKINDS
select_especie = pd.read_csv('data/TREEKINDS.csv', usecols=['NOM_POPULAR'])
select_especie = list(select_especie['NOM_POPULAR'].values)
select_especie = select_especie[:1] + sorted(select_especie[1:])

# Carregar o arquivo CSV existente
file_path = "data/registro_arvores.csv"
try:
    df_registro = pd.read_csv(file_path)
except FileNotFoundError:
    columns=['ID', 'ESPECIES', 'ALTURA', 'DT_BT', 'DT_MT', 'DT_AT', 'DAP', 'DATA_REGISTRO']
    df_registro = pd.DataFrame(columns=columns)

def save_to_csv(data):
    """
    Função para salvar os dados no arquivo CSV
    """
    try:
        # Adicionar data do registro
        data['DATA_REGISTRO'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Adicionar nova linha ao DataFrame
        df_registro.loc[len(df_registro)] = data
        # Salvar o DataFrame atualizado no arquivo CSV
        df_registro.to_csv(file_path, index=False)
        st.success("Dados salvos com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")

st.set_page_config(layout="wide")   
st.title('Plano de Testes VERA ESE')
st.subheader('Mapa com a Geolocalização das Árvores')

m = folium.Map(location=[df.LATITUDE.mean(), df.LONGITUDE.mean()], 
            zoom_start=10, control_scale=True)

marker_cluster = MarkerCluster().add_to(m)

#Loop through each row in the dataframe
for values in df.values:
    ID, ID_POSTE, ESP, LAT, LON, ALTURA, IMAGE_PATH = values

    # Lendo a imagem e codificando em base64
    with open(IMAGE_PATH, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode('utf-8')

    info = f'''
    <div>
        <p>ID: {ID}</p>
        <p>ID DO POSTE: {ID_POSTE}</p>
        <p>Espécie: {ESP}</p>
        <p>Altura: {ALTURA}</p>
        <img src="data:image/png;base64,{encoded_image}" alt="Imagem da árvore" style="width:300px;height:300px;">
    </div>
    '''
 
    iframe = folium.IFrame(info)
    
    #Initialise the popup using the iframe
    popup = folium.Popup(iframe, min_width=500, max_width=500)
    
    # folium.Marker(location=[LAT,LON], popup=popup, c=ID).add_to(m)
    folium.Marker(location=[LAT,LON], popup=popup, c=ID).add_to(marker_cluster)

st_data = folium_static(m, width=1100, height=750)

# """
# Função para registras os dados do streamlit no arquivo CSV
# """
st.subheader('Cadastro das Árvores')
with st.form('Registro'):   
    row1 = st.columns([1, 2, 2])
    id_arvore = row1[0].selectbox("Escolha uma árvore para registro:", select_id)
    # especie = row1[1].text_input('Espécie da Árvore:', value='Não Especificado')
    especie = row1[1].selectbox('Espécie da Árvore:', select_especie)
    altura = row1[2].number_input('Altura da Árvore (m):', value=None, min_value=0.0, step=0.5)

    header = st.columns([1])
    header[0].subheader('Distância de Toque')

    row2 = st.columns([1, 1, 1])
    distancia_baixa_tensao = row2[0].number_input('Baixa Tensão (cm):', value=None, min_value=0.0, step=5.0)
    distancia_media_tensao = row2[1].number_input('Média Tensão (cm):', value=None, min_value=0.0, step=5.0)
    distancia_alta_tensao = row2[2].number_input('Alta Tensão (cm):', value=None, min_value=0.0, step=5.0)
    
    row3 = st.columns([1])
    dap = row3[0].number_input('DAP (cm):', value=None, min_value=0.0, step=5.0)

    data = {
        'ID': id_arvore,
        'ESPECIES': especie,
        'ALTURA': altura,
        'DT_BT': distancia_baixa_tensao,
        'DT_MT': distancia_media_tensao,
        'DT_AT': distancia_alta_tensao,
        'DAP': dap
    }

    if st.form_submit_button('Salvar'):
        save_to_csv(data)

# """
# Função para mostrar os dados cadastrados e atualizar os dados quando modificados
# """

st.subheader('Dados Cadastrados')
modified_df = st.data_editor(df_registro, num_rows="dynamic")
if modified_df is not None:
    df_registro = modified_df
    df_registro.to_csv(file_path, index=False)
    st.success("Arquivo de registro atualizado com sucesso!")