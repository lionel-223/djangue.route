ARG DOCKER_IMAGE=python:3.10-slim
FROM $DOCKER_IMAGE AS install-deps

WORKDIR /app

COPY ./scripts .

CMD ./scripts/run.sh
EXPOSE 5000

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt


FROM install-deps as copy-files

COPY . .

LABEL org.label-schema.schema-version="1.0" \
	  org.label-schema.build-date="10-05-2022" \
	  org.label-schema.name="1lettre1sourire" \
	  org.label-schema.description="dev-environment" \
	  org.label-schema.version="1.0" \
	  org.label-schema.vendor="1lettre1sourire" \
	  org.label-schema.url="https://1lettre1sourire.org/" \
	  org.label-schema.vcs-url="https://github.com/1lettre1sourire/1lettre1sourire" \
	  org.label-schema.vcs-ref=$VCS_REF \
	  org.label-schema.docker.cmd=""
