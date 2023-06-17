# Imagen base
FROM python:3.7

# Configura el directorio de trabajo
WORKDIR /jukebox

# Instala las dependencias necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libopenmpi-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip wheel && \
    pip install git+https://github.com/openai/jukebox.git

RUN git clone https://github.com/openai/jukebox.git .

# Instala las dependencias de Python
RUN pip install -r requirements.txt
RUN pip install -e .

# Define el comando por defecto al iniciar el contenedor
CMD ["python"]