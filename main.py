import streamlit as st
import requests
import os

# Encabezado de la aplicación
st.header('Desplegando asistente para extraer insights artículos')

# Contenedor para el contador de caracteres
char_count_container = st.empty()

# Función para actualizar el contador de caracteres
def update_char_count():
    char_count = len(st.session_state.contenido)
    char_count_container.text(f'Caracteres: {char_count}')

# Inicializar session_state para 'contenido'
if 'contenido' not in st.session_state:
    st.session_state['contenido'] = ""

# Campo para recibir una consulta
contenido = st.text_area('Ingresa el artículo que deseas procesar:', key='contenido', on_change=update_char_count)

# Llamar a la función para mostrar el contador de caracteres inicial
update_char_count()

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
                "contenido": st.session_state['contenido']
            },
            "response_mode": "blocking",
            "user": "javrezt"
        }

        # Realizar la petición POST
        response = requests.post(base_url, json=data, headers=headers)

        # Verificar y manejar la respuesta
        if response.status_code == 200:
            try:
                result = response.json()
                if 'code' in result and result['code'] == 'completion_request_error':
                    st.error('El número de tokens ha superado el límite permitido.')
                else:
                    st.markdown(result['answer'])
            except ValueError as e:
                st.error('Error al procesar la respuesta JSON')
                st.text(response.text)  # Muestra el contenido de la respuesta para depuración
        else:
            st.error('El contenido supera la cantidad máxima de caracteres')
            #st.text(response.text)  # Muestra el contenido de la respuesta para depuración
