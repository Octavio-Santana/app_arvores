import base64
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static

# Read DataSet
df = pd.read_csv('data/data.csv')
select_id = df['ID'].values

# Create an empty dataframe to store user inputs
df_registro = pd.DataFrame(columns=['ID', 'ESPECIES', 'ALTURA', 'Distância de Toque', 'DAP'])

# Function to handle map click event
def on_map_event(sample):
    especie_da_arvore = st.text_input("Espécie da Árvore:", value='Não Especificado')
    altura_da_arvore = st.number_input("Altura da Árvore (m):", value=0.0, min_value=0.0, step=0.5)
    distancia_de_toque = st.number_input("Distância de Toque (cm):", value=0.0, min_value=0.0, step=5.0)
    dap = st.number_input("DAP (cm):", value=0.0, min_value=0.0, step=5.0)

    user_inputs = {
    'ID': [sample], 
    'ESPECIES': [especie_da_arvore], 
    'ALTURA': [altura_da_arvore], 
    'Distância de Toque': [distancia_de_toque], 
    'DAP': [dap]
    }

    user_inputs = pd.DataFrame(user_inputs)
    return user_inputs 

def app(df_registro):

    st.set_page_config(layout="wide")
    st.title('Plano de Testes VERA ESE')

    sample = st.selectbox("Escolha uma árvore para registro:", list(select_id))

    m = folium.Map(location=[df.LATITUDE.mean(), df.LONGITUDE.mean()], 
                zoom_start=10, control_scale=True)

    user_inputs = on_map_event(sample)
    if st.button("Registrar Informações"):
        df_registro = pd.concat([df_registro, user_inputs], ignore_index=True)
        print(df_registro)

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
        
        #Add each row to the map
        if ID == sample:
            folium.Marker(location=[LAT,LON], popup=popup, c=ID, icon=folium.Icon(color='lightred')).add_to(m)
        else:
            folium.Marker(location=[LAT,LON], popup=popup, c=ID).add_to(m)

    st_data = folium_static(m, width=1100, height=750)
    return df_registro

if __name__ == '__main__':    

    df_registro = app(df_registro)
