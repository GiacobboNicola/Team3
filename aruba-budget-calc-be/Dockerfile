ARG PYTHON_VERSION=3.12-slim

#==== stage runtime ====
FROM python:${PYTHON_VERSION} AS runtime

ARG ENV=development

ENV \
  # allow statements and log messages to immediately appear
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=random \
  # disable a pip version to reduce runtime & log-spam (on/1)
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  # cache is useless in docker image, so disale to reduce image size
  DEBIAN_FRONTEND=noninteractive \
  LANG=C.UTF-8 \
  LC_ALL=C.UTF-8

# create the app user
RUN if [ -n "$(grep 'ID=alpine' /etc/os-release)" ]; then \
  (addgroup -S -g 1000 app && adduser -S -u 1000 app app) \
  else \
  (addgroup --system --gid 1000 app && adduser --system --uid 1000 --group app) \
  fi
RUN chown -R app:app $HOME

#==== stage pdm ====
FROM runtime AS pdm

# install PDM and configure pdm in PEP 582 mode (__pypackages__)
RUN pip install -U pip setuptools wheel
RUN pip install pdm pdm-pep517
RUN pdm config python.use_venv false


#==== stage lib ====
FROM pdm AS lib

# install dependencies and project in /project/__pypackages__
WORKDIR /project
COPY ./team3-lib/team3_lib ./team3_lib
COPY team3-lib/pyproject.toml team3-lib/pdm.lock team3-lib/README.md ./
RUN pdm install --prod --no-lock --no-editable --no-isolation
# install development env
RUN if [ "$ENV" = "development" ]; then \
   pdm install --dev --no-lock --no-editable ; fi


#==== stage core-lib ====
FROM pdm AS core-lib

WORKDIR /project
COPY ./team3-core/team3_core ./team3_core
COPY team3-core/pyproject.toml team3-core/pdm.lock team3-core/README.md ./
RUN pdm install --prod --no-lock --no-editable --no-isolation
# install development env
RUN if [ "$ENV" = "development" ]; then \
   pdm install --dev --no-lock --no-editable ; fi


#==== stage core ====
FROM runtime AS core

# copy modules
WORKDIR /app
COPY ./team3-lib/team3_lib ./team3_lib
COPY ./team3-core/team3_core ./team3_core
# copy pkgs folder with lib, bin, etc
COPY --from=lib /project/__pypackages__/3* /app/pkgs
COPY --from=core-lib /project/__pypackages__/3* /app/pkgs
ENV PYTHONPATH=/app/pkgs/lib:/app:$PYTHONPATH
ENV PATH=/app/pkgs/bin:$PATH
# switch to a not-root user
USER app


#==== stage api-lib ====
FROM pdm AS api-lib

WORKDIR /project
COPY ./team3-api/team3_api ./team3_api
COPY ./team3-api/pyproject.toml team3-api/pdm.lock team3-api/README.md ./
RUN pdm install --prod --no-lock --no-editable --no-isolation
# install development env
RUN if [ "$ENV" = "development" ]; then \
  pdm install --dev --no-lock --no-editable ; fi


#==== stage api ====
FROM runtime AS api

# copy modules
WORKDIR /app
COPY ./team3-lib/team3_lib ./team3_lib
COPY ./team3-api/team3_api ./team3_api
# copy pkgs folder with lib, bin, etc
COPY --from=lib /project/__pypackages__/3* /app/pkgs
COPY --from=api-lib /project/__pypackages__/3* /app/pkgs
ENV PYTHONPATH=/app/pkgs/lib:/app:$PYTHONPATH
ENV PATH=/app/pkgs/bin:$PATH
# switch to a not-root user
USER app


#==== stage test-lib ====
FROM pdm AS test-lib

WORKDIR /project
COPY ./team3-test/team3_test ./team3_test
COPY ./team3-test/pyproject.toml team3-test/pdm.lock team3-test/README.md ./
RUN pdm install --prod --no-lock --no-editable --no-isolation
# install development env
RUN if [ "$ENV" = "development" ]; then \
  pdm install --dev --no-lock --no-editable ; fi


#==== stage test ====
FROM runtime AS test

# copy modules
WORKDIR /app
COPY ./team3-lib/team3_lib ./team3_lib
COPY ./team3-test/team3_test ./team3_test
# copy pkgs folder with lib, bin, etc
COPY --from=lib /project/__pypackages__/3* /app/pkgs
COPY --from=test-lib /project/__pypackages__/3* /app/pkgs
ENV PYTHONPATH=/app/pkgs/lib:/app:$PYTHONPATH
ENV PATH=/app/pkgs/bin:$PATH
# switch to a not-root user
USER app
