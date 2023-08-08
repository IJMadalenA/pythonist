# Establecer la imagen base
FROM python:3.7.5

# Instalar dependencias del sistema operativo
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    git \
    gcc \
    g++ \
    libopenmpi-dev \
    mpich \
    wget \
    curl \
    ca-certificates \
    libsox-fmt-all \
    llvm-dev \
    python3-mpi4py


# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.9.2-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh
ENV PATH="/opt/conda/bin:${PATH}"

# 4 - Crear el entorno Conda
RUN  conda update -n base -c defaults conda && \
     conda create --name jukebox python=3.7.5 && \
     echo "conda activate jukebox" >> ~/.bashrc

SHELL ["conda", "run", "-n", "jukebox", "/bin/bash", "-c"]

# Instalar las dependencias del proyecto. Preparamos el entorno antes de copiar el código fuente.
RUN conda install -y mpi4py=3.0.3 && \
    conda install cudatoolkit=10.0 && \
    conda install -y pytorch=1.1 torchvision=0.3 cudatoolkit=10.0 -c pytorch && \
    conda install av=7.0.01 -c conda-forge && \
    conda install PyTorch -c PyTorch

COPY ./ ./

RUN pip install -r requirements.txt && \
    pip install ./tensorboardX && \
    pip install -e .

# Configurar el punto de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
