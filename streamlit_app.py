import base64
import pandas as pd
import folium
from streamlit_folium import st_folium, folium_static

df = pd.read_csv('data/data.csv')
df = df[~df['image_path'].isnull()]
df.reset_index(drop=True, inplace=True)


m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], 
               zoom_start=12, control_scale=True)

#Loop through each row in the dataframe
for i,row in df.iterrows():

    # Lendo a imagem e codificando em base64
    with open(row['image_path'], 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode('utf-8')

    #Setup the content of the popup    
    info = f'''
    <div>
        <p>ID: {row['ID']}</p>
        <p>ID DO POSTE: {row['ID DO POSTE']}</p>
        <p>Altura: {row['altura']}</p>
        <p>DT_BT (cm): {row['DT_BT']}</p>
        <p>DT_MT (cm): {row['DT_MT']}</p>  
        <img src="data:image/png;base64,{encoded_image}" alt="Imagem da árvore" style="width:300px;height:300px;">      
    </div>
    '''
    iframe = folium.IFrame(info)
    
    #Initialise the popup using the iframe
    popup = folium.Popup(iframe, min_width=500, max_width=500)
    
    #Add each row to the map
    folium.Marker(location=[row['latitude'],row['longitude']],
                  popup = popup, c=row['ID']).add_to(m)

# st_data = st_folium(m, width=700)  
st_data = folium_static(m, width=700)              