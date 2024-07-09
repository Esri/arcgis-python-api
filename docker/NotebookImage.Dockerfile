FROM ubuntu:24.04

ARG python_version="3.11"
ARG arcgis_version="2.3.1"
ARG sampleslink="https://github.com/Esri/arcgis-python-api/releases/download/v${arcgis_version}/samples.zip"
ARG githubfolder="arcgis-python-api"

# Heavily influenced from
# https://github.com/jupyter/docker-stacks/blob/main/images/docker-stacks-foundation/Dockerfile
# and https://github.com/jupyter/docker-stacks/blob/main/images/base-notebook/Dockerfile
# using miniconda instead of micromamba
ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

LABEL org.opencontainers.image.authors="jroebuck@esri.com"
LABEL org.opencontainers.image.description="Jupyter Notebook with the latest version of the ArcGIS API for Python and its Linux dependencies preinstalled"
# License applies to image only, not to the software running inside the image
LABEL org.opencontainers.image.licenses=Apache
LABEL org.opencontainers.image.source=https://github.com/Esri/arcgis-python-api

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8

ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    bzip2 \
    ca-certificates \
    fonts-liberation \
    locales \
    pandoc \
    run-one \
    sudo \
    tini \
    unzip \
    wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    echo "C.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen

USER ${NB_UID}

# install miniconda
RUN cd /opt && wget -O miniconda3.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
  bash /opt/miniconda3.sh -b -p $CONDA_DIR && \
  rm miniconda3.sh
  
RUN conda init bash && \
  source activate base && \
  conda install --yes python=${python_version} && \
  conda clean --all -f -y

# Install Python API from Conda
RUN conda install --override-channels -c esri -c defaults arcgis=${arcgis_version} --yes --quiet \
    && conda clean --all -f -y \
    && find /opt/conda -name __pycache__ -type d -exec rm -rf {} +

# Fetch and extract samples from GitHub
RUN mkdir /home/${NB_USER}/$githubfolder && \
    wget -O samples.zip $sampleslink \
    && unzip -q samples.zip -d /home/${NB_USER}/$githubfolder \
    && rm samples.zip \
    && mv /home/${NB_USER}/$githubfolder/* ./ \
    && rm -rf $githubfolder/ \
           apidoc/ \
           work/ \
           talks/ \
           environment.yml\
    && fix-permissions /home/${NB_USER}

RUN rm /opt/conda/lib/python${python_version}/site-packages/notebook/static/base/images/logo.png
COPY --chown=${NB_USER}:users jupyter_esri_logo.png /opt/conda/lib/python${python_version}/site-packages/notebook/static/base/images/logo.png