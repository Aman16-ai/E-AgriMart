FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code

RUN pip install --no-cache-dir -r requirements.txt

# RUN python manage.py makemigrations 

# RUN python manage.py migrate

# COPY start.sh /start.sh
# RUN chmod +x /start.sh

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "E_Agrimart.wsgi:application"]
# ENTRYPOINT ["/start.sh"]