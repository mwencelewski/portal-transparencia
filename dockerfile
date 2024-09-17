
FROM python:3.10.7 

RUN useradd -m seleniumuser && \
  mkdir -p /app && \
  chown -R seleniumuser:seleniumuser /app

USER seleniumuser
COPY --chown=seleniumuser:seleniumuser . /app

WORKDIR /app 

RUN pip install --no-cache-dir pipenv && \
  python -m pip install --upgrade pip && \
  python -m pipenv install 

CMD ["bash"]
