FROM revolutionsystems/python:3.10.4-wee-optimized-lto as ksvotes

# build ImageMagick with gslib for formfiller
USER root

RUN apt-get update && \
    apt-get install --yes --no-install-recommends wget xz-utils build-essential \
      postgresql-client libpq-dev libffi-dev libgs-dev ghostscript fonts-liberation imagemagick wait-for-it

WORKDIR /app

COPY requirements*.txt ./
COPY Makefile .

RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

COPY manage.py .
COPY bin ./bin
COPY app ./app
COPY migrations ./migrations
COPY babel.cfg .
COPY config.py .
COPY county-clerks.csv .
COPY ks-zip-by-county.csv .
COPY Procfile .
COPY scss ./scss
COPY translations.json .
COPY start-server.sh .

RUN make locales

# finish with app user and app
RUN groupadd ksvotesapp && \
  useradd -g ksvotesapp ksvotesapp && \
  apt-get purge -y --auto-remove build-essential && \
  apt-get -y install make && \
  chown -R ksvotesapp:ksvotesapp /app

ARG ENV_NAME=""
ENV ENV_NAME=${ENV_NAME}
ARG GIT_SHA=""
ENV GIT_SHA=${GIT_SHA}

USER ksvotesapp
CMD ["./start-server.sh"]

