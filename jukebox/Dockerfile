# Establecer la imagen base
FROM ubuntu:latest

# Instalar dependencias del sistema operativo
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    git \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instalar Miniconda
ENV MINICONDA_VERSION py37_4.9.2
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh
ENV PATH /opt/conda/bin:$PATH

# Crear el entorno Conda
RUN conda create --name jukebox python=3.7.5 && \
    echo "conda activate jukebox" >> ~/.bashrc
SHELL ["conda", "run", "-n", "jukebox", "/bin/bash", "-c"]

# Clonar el repositorio Jukebox
RUN git clone https://github.com/openai/jukebox.git
WORKDIR /jukebox

# Instalar las dependencias del proyecto
RUN conda install mpi4py=3.0.3 && \
    conda install cudatoolkit=10.0 && \
    conda install pytorch=1.4 -c pytorch && \
    conda install av=7.0.01 -c conda-forge && \
    pip install torch --no-cache-dir && \
    pip install torchvision --no-cache-dir && \
    conda install PyTorch -c PyTorch && \
    conda install torchvision

RUN pip install -r requirements.txt
RUN pip install -e .

# Configurar el punto de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
