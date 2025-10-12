ARG python_version="3.11"
FROM quay.io/jupyter/minimal-notebook:python-${python_version}

ARG python_version
ARG arcgis_version="2.4.1"
ARG gdal_version="3.10.2"
ARG sampleslink="https://github.com/Esri/arcgis-python-api/releases/download/v${arcgis_version}/samples.zip"
ARG githubfolder="arcgis-python-api"
ARG env_name=arcgis

LABEL org.opencontainers.image.authors="jroebuck@esri.com"
LABEL org.opencontainers.image.description="Jupyter environment preconfigured for ArcGIS API for Python"
LABEL org.opencontainers.image.licenses=Apache
LABEL org.opencontainers.image.source=https://github.com/Esri/arcgis-python-api

USER ${NB_UID}

# Create conda environment with specified python version
RUN conda create -n ${env_name} -c conda-forge python=${python_version} -y --quiet --override-channels \
    && conda clean --all -f -y \
    && find /opt/conda -name __pycache__ -type d -exec rm -rf {} +

# Install gdal
RUN conda install -n ${env_name} -c conda-forge gdal=${gdal_version} -y --quiet --override-channels \
    && conda clean --all -f -y \
    && find /opt/conda -name __pycache__ -type d -exec rm -rf {} +

# Install ArcGIS API for Python from pypi
RUN . activate ${env_name} \
    # adding .* ensures the latest patch version is installed
    && python -m pip install "arcgis==${arcgis_version}.*" \
    && conda clean --all -f -y \
    && find /opt/conda -name __pycache__ -type d -exec rm -rf {} +

# Install arcgis-mapping if arcgis_version >= 2.4.0
RUN (dpkg --compare-versions $arcgis_version ge 2.4.0 \
    && . activate ${env_name} \
    && python -m pip install arcgis-mapping \
    && conda clean --all -f -y \
    && find /opt/conda -name __pycache__ -type d -exec rm -rf {} +;) \
    || echo "[INFO] Skipped installing arcgis-mapping for version $arcgis_version (>= 2.4.0 required for arcgis-mapping)"

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
    # remove .DS_Store and __MACOSX from home directory:
    && find /home/${NB_USER} -name ".DS_Store" -delete \
    && rm -rf /home/${NB_USER}/__MACOSX \
    && fix-permissions /home/${NB_USER}

# See https://jupyter-docker-stacks.readthedocs.io/en/latest/using/recipes.html#add-a-custom-conda-environment-and-jupyter-kernel
# Create Python kernel and link it to jupyter
RUN "${CONDA_DIR}/envs/${env_name}/bin/python" -m ipykernel install --user --name="${env_name}" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"


# More information here: https://github.com/jupyter/docker-stacks/pull/2047
USER root

# Set DOCKER_STACKS_JUPYTER_CMD to "notebook" for versions less than 2.4.0
RUN \
    (dpkg --compare-versions $arcgis_version lt 2.4.0 \
    && echo 'DOCKER_STACKS_JUPYTER_CMD="notebook"' >> /etc/environment \
    && echo "[INFO] Set DOCKER_STACKS_JUPYTER_CMD to notebook for arcgis < 2.4.0") \
    || echo "[INFO] Using default DOCKER_STACKS_JUPYTER_CMD (lab) for arcgis >= 2.4.0"

RUN \
    # This changes a startup hook, which will activate the custom environment for the process
    echo conda activate "${env_name}" >> /usr/local/bin/before-notebook.d/10activate-conda-env.sh && \
    # This makes the custom environment default in Jupyter Terminals for all users which might be created later
    echo conda activate "${env_name}" >> /etc/skel/.bashrc && \
    # This makes the custom environment default in Jupyter Terminals for already existing NB_USER
    echo conda activate "${env_name}" >> "/home/${NB_USER}/.bashrc"

USER ${NB_UID}
