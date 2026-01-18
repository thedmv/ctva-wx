# syntax=docker/dockerfile:1
FROM ubuntu:24.04

# ============================================================================
# Environment Setup
# ============================================================================
ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/root/.local/bin:${PATH}" \
    GDAL_CONFIG=/usr/bin/gdal-config \
    PROJ_LIB=/usr/share/proj \
    FIONA_USE_GDAL_FROM_PATH=YES \
    SHELL=/bin/bash \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG GEOSTACK_REV=1
WORKDIR /code

# ============================================================================
# Base Tools + Add PPAs
# ============================================================================
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
      ca-certificates curl wget gnupg software-properties-common \
      build-essential pkg-config git vim less zip unzip htop procps cmake ninja-build patchelf \
  && add-apt-repository -y ppa:deadsnakes/ppa \
  && add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable \
  && rm -rf /var/lib/apt/lists/*

# ============================================================================
# Python 3.13 + Geo Stack + All System Dependencies
# ============================================================================
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
      python3.13 python3.13-dev python3.13-venv \
      gdal-bin libgdal-dev \
      proj-bin libproj-dev proj-data \
      libgeos-dev libspatialindex-dev \
      libtiff-dev libjpeg-turbo8-dev libpng-dev libopenjp2-7 \
      zlib1g-dev libzstd-dev libdeflate-dev \
      hdf5-tools libhdf5-dev netcdf-bin libnetcdf-dev \
      nco libeccodes0 libeccodes-dev libeccodes-tools \
      libudunits2-dev libxml2-dev libssl-dev bash-completion readline-common \
  && rm -rf /var/lib/apt/lists/* \
  && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1 \
  && update-alternatives --install /usr/bin/python python /usr/bin/python3.13 1

# ============================================================================
# Create non-root user & directories
# ============================================================================
RUN useradd -m -s /bin/bash dev \
  && mkdir -p /code /in-data /out-data /plots \
  && chown -R dev:dev /code /in-data /out-data /plots /home/dev

# ============================================================================
# uv + Base Python Packages (single layer)
# ============================================================================
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
  && export PATH="/root/.local/bin:${PATH}" \
  && uv pip install --python /usr/bin/python3.13 --system \
      pip setuptools wheel cython setuptools_scm scikit-build-core meson-python \
      hatchling hatch-vcs hatch-fancy-pypi-readme flit-core poetry-core numpy \
      jupyterlab ipykernel \
  && GDAL_VERSION=$(gdal-config --version) \
  && uv pip install --python /usr/bin/python3.13 --system --no-binary=gdal "GDAL==${GDAL_VERSION}"

# ============================================================================
# Build Geo Packages + Generate Constraints (single layer)
# ============================================================================
RUN --mount=type=cache,target=/root/.cache/uv \
    JOBS="$(nproc)" \
  && export MAKEFLAGS="-j${JOBS}" CMAKE_BUILD_PARALLEL_LEVEL="${JOBS}" \
  && uv pip install --python /usr/bin/python3.13 --no-binary=:all: --system \
      pyproj==3.6.1 fiona==1.9.6 rasterio==1.4.2 \
  && python -c "import importlib.metadata as im; \
      names=['pyproj','Fiona','rasterio']; \
      pins=[f'{n}=={im.version(n)}' for n in names]; \
      open('/code/constraints-geo.txt','w').write('\n'.join(pins)+'\n'); \
      print(f'Constraints: {pins}')"

# ============================================================================
# Install Application Dependencies + Shapely (single layer)
# ============================================================================
COPY --chown=dev:dev requirements.txt /code/requirements.txt
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --python /usr/bin/python3.13 --system \
      --constraint /code/constraints-geo.txt -r /code/requirements.txt \
  && uv pip install --python /usr/bin/python3.13 --system shapely

# ============================================================================
# Verify GDAL Bindings
# ============================================================================
COPY --chown=dev:dev verify_gdal_bindings.py /code/verify_gdal_bindings.py
RUN python /code/verify_gdal_bindings.py

# ============================================================================
# Jupyter & Shell Configuration
# ============================================================================
RUN mkdir -p /etc/jupyter \
  && printf "c.ServerApp.terminado_settings = {'shell_command': ['/bin/bash']}\n" \
      > /etc/jupyter/jupyter_server_config.py \
  && printf '\n# Bash completion and prompt\n\
if [ -f /usr/share/bash-completion/bash_completion ]; then\n\
  . /usr/share/bash-completion/bash_completion\n\
fi\n\
case "$-" in\n\
  *i*) PS1="\\u@\\h:\\w\\$ " ;;\n\
esac\n' >> /etc/bash.bashrc

# ============================================================================
# Runtime
# ============================================================================
USER dev
# Let the compose handle the below commands
# EXPOSE 50000
# CMD ["python", "-m", "jupyterlab", \
    #  "--ServerApp.ip=0.0.0.0", \
    #  "--ServerApp.port=50000", \
    #  "--ServerApp.open_browser=False"]

# Windows runtime info:
# Days              : 0
# Hours             : 0
# Minutes           : 3
# Seconds           : 31
# Milliseconds      : 728
# Ticks             : 2117289978
# TotalDays         : 0.00245056710416667
# TotalHours        : 0.0588136105
# TotalMinutes      : 3.52881663
# TotalSeconds      : 211.7289978
# TotalMilliseconds : 211728.9978