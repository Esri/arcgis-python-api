FROM ubuntu:24.04

ARG python_version="3.11"
ARG arcgis_version="2.3.1"
ARG sampleslink="https://github.com/Esri/arcgis-python-api/releases/download/v${arcgis_version}/samples.zip"
ARG githubfolder="arcgis-python-api"

# Heavily influenced from
# https://github.com/jupyter/docker-stacks/blob/main/images/base-notebook/Dockerfile
# using miniconda instead of micromamba
ARG NB_USER="ubuntu"
ARG NB_UID="1000"
ARG NB_GID="1000"

LABEL org.opencontainers.image.authors="jroebuck@esri.com"
LABEL org.opencontainers.image.description="Jupyter Notebook with the latest version of the ArcGIS API for Python and its Linux dependencies preinstalled"
# License applies to image only, not to the software running inside the image
LABEL org.opencontainers.image.licenses=Apache
LABEL org.opencontainers.image.source=https://github.com/Esri/arcgis-python-api

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

ENV CONDA_DIR=/home/${NB_USER}/miniconda \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8

ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

# Copy a script that we will use to correct permissions after running certain commands
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

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

# Create NB_USER with name jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN mkdir -p "${CONDA_DIR}" && \
    chown "${NB_USER}:${NB_GID}" "${CONDA_DIR}" && \
    chmod g+w /etc/passwd && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions ${HOME}

USER ${NB_UID}

WORKDIR ${HOME}

EXPOSE 8888

# install miniconda
RUN wget -O ${HOME}/miniconda3.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
  bash ${HOME}/miniconda3.sh -b -f -p "${CONDA_DIR}" && \
  rm ${HOME}/miniconda3.sh && \
  conda init bash && \
  conda install -n base --yes python=${python_version} --quiet && \
  conda clean --all -f -y

# Install Python API from Conda
RUN conda install --override-channels -c esri -c defaults arcgis=${arcgis_version} --yes --quiet \
    && conda clean --all -f -y \
    && find ${CONDA_DIR} -name __pycache__ -type d -exec rm -rf {} +

# Fetch and extract samples from GitHub
RUN mkdir ${HOME}/$githubfolder && \
    wget -O ${HOME}/samples.zip $sampleslink \
    && unzip -q ${HOME}/samples.zip -d ${HOME}/$githubfolder \
    && rm ${HOME}/samples.zip

RUN mkdir -p ${CONDA_DIR}/lib/python${python_version}/site-packages/notebook/static/base/images && rm -f ${CONDA_DIR}/lib/python${python_version}/site-packages/notebook/static/base/images/logo.png
COPY --chown=${NB_USER}:users jupyter_esri_logo.png ${CONDA_DIR}/lib/python${python_version}/site-packages/notebook/static/base/images/logo.png