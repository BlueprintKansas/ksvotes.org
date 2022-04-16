FROM revolutionsystems/python:3.10.4-wee-optimized-lto

# build ImageMagick with gslib for formfiller
USER root
WORKDIR /tmp

ARG IMAGE_MAGICK_VERSION=6.9.12-44

RUN apt-get update && \
    apt-get install --yes --no-install-recommends wget xz-utils build-essential \
      postgresql-client libpq-dev libffi-dev libgs-dev ghostscript fonts-liberation

RUN mkdir src && \
    cd src && \
    wget --no-check-certificate -nv https://www.imagemagick.org/download/releases/ImageMagick-${IMAGE_MAGICK_VERSION}.tar.xz && \
    tar xf ImageMagick-${IMAGE_MAGICK_VERSION}.tar.xz && \
    cd ImageMagick-${IMAGE_MAGICK_VERSION} && \
    ./configure --with-gslib=yes && \
    make && \
    make install && \
    ldconfig && \
    cd .. && \
    rm -rf src

WORKDIR /app

COPY requirements*.txt ./
COPY Makefile .
COPY manage.py .
COPY bin ./bin
COPY app ./app
COPY migrations ./migrations
COPY babel.cfg .
COPY config.py .
COPY county-clerks.csv .
COPY Procfile .
COPY scss ./scss
COPY translations.json .
COPY start-server.sh .

RUN pip install -r requirements.txt && make locales

# finish with app user and app
RUN groupadd ksvotesapp && \
  useradd -g ksvotesapp ksvotesapp && \
  rm -f requirements*.txt && \
  apt-get purge -y --auto-remove build-essential && \
  apt-get -y install make && \
  chown -R ksvotesapp:ksvotesapp /app

USER ksvotesapp
EXPOSE 8081

CMD ["./start-server.sh"]
