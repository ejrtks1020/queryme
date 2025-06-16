FROM python:3.12.5-slim AS builder

RUN pip install uv

ENV UV_VIRTUALENVS_CREATE=1 \
    UV_VIRTUALENVS_IN_PROJECT=1 \
    UV_NO_INTERACTION=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config

WORKDIR /app

COPY app/pyproject.toml app/uv.lock /app/

RUN uv venv --seed && \
    uv pip install .

FROM python:3.12.5-slim AS runtime

ENV DEBIAN_FRONTEND=noninteractive \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update --fix-missing && apt-get install -y \
    software-properties-common \
    net-tools \
    curl \
    procps \
    supervisor \
    vim \
    binutils \
    pandoc \
    sudo

ARG UID=1000
ARG GID=1000
ARG UNAME=genos
ARG GNAME=genos

# Add Group with designated GID
RUN getent group $GID || groupadd -g $GID $GNAME

# Add User with designated UID and GID
RUN getent passwd $UID || useradd -m -u $UID -g $GID -s /bin/bash $UNAME

# Add user to sudoers with no password prompt
RUN UNAME=$(getent passwd "$UID" | cut -d: -f1); \
    usermod -aG sudo $UNAME && \
        echo "$UNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN chown -R $UID:$GID /run /var/log /etc/supervisor

USER $UID:$GID

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="/app/.venv/bin:$PATH"
COPY --chown=$UID:$GID app/deployment/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY --chown=$UID:$GID app/ /app

CMD ["/app/entrypoint.sh"]
