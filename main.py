import streamlit as st
import requests
import os

# Encabezado de la aplicación
st.header('Desplegando asistente para extraer insights artículos')

# Campo para recibir una consulta
contenido = st.text_area('Ingresa el artículo que deseas procesar:')

# Guardar los valores en variables
if st.button('Consultar'):
    base_url = "https://api.dify.ai/v1/completion-messages"
    # Debes reemplazar esto con tu API key real
    my_secret = os.getenv('DIFY_APP_SECRET')

    if not my_secret:
        st.error('No se ha encontrado la API key. Asegúrate de que DIFY_APP_SECRET esté configurada correctamente en el entorno.')
    else:
        # Encabezados para la petición
        headers = {
            'Authorization': f'Bearer {my_secret}',
            'Content-Type': 'application/json'
        }

        # Datos a enviar en la petición
        data = {
            "inputs": {
                "contenido": contenido
            },
            "response_mode": "blocking",
            "user": "javrezt"
        }

        # Realizar la petición POST
        response = requests.post(base_url, json=data, headers=headers)

        # Verificar y manejar la respuesta
        if response.status_code == 200:
            #st.success('Consulta enviada con éxito!')
            try:
                result = response.json()
                #st.markdown('### Resultado de la solicitud:')
                st.markdown(result['answer'])
            except ValueError as e:
                st.error('Error al procesar la respuesta JSON')
                st.text(response.text)  # Muestra el contenido de la respuesta para depuración
        else:
            st.error(f'Error al enviar la consulta: {response.status_code}')
            st.text(response.text)  # Muestra el contenido de la respuesta para depuración
