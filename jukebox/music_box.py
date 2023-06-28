import openai

# Configura las credenciales de OpenAI
openai.api_key = 'TU_CLAVE_DE_API'


def generate_music(gene, estile, duration):
    # Define los parámetros y variables de entrada
    prompt = f"Genera una pista musical en el género {gene} con estilo {estile} de duración {duration}."

    # Hacer la solicitud a la API
    response = openai.Completion.create(
        engine='text-davinci-003',  # Selecciona el motor de Jukebox
        prompt=prompt,
        max_tokens=1000,  # Controla la longitud de la respuesta generada
        temperature=0.8,  # Controla la aleatoriedad de la generación (mayor valor = más aleatorio)
        n=1,  # Genera una sola respuesta
        stop=None,  # Opcional: define una frase para detener la generación
        timeout=60  # Opcional: establece un límite de tiempo en segundos para la solicitud
    )

    # Procesa la respuesta
    if response and response.choices:
        pista_musical = response.choices[0].text.strip()

        # Aquí puedes guardar la pista musical en un archivo de audio o realizar cualquier otro procesamiento necesario
        # También puedes realizar cualquier postprocesamiento adicional, como eliminar el texto del prompt de la pista generada

        return pista_musical

# Ejemplo de uso
genero = "pop"
estilo = "romántico"
duracion = "3 minutos"

pista_generada = generar_musica(genero, estilo, duracion)
print(pista_generada)
