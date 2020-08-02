FROM python:3.8-slim-buster

ENV APP_DIR=/usr/src/app

# Create a directory for application
RUN mkdir -p ${APP_DIR} && mkdir ${APP_DIR}/staticfiles ${APP_DIR}/logs

RUN useradd --create-home smusr

# Make app as working directory
WORKDIR ${APP_DIR}

# Install requirements
COPY requirements.txt ${APP_DIR}
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN chown -R smusr:smusr ${APP_DIR}
USER smusr

# Copy rest of application
COPY . ${APP_DIR}

# Run the start script
CMD ["gunicorn", "-w", "4", "-b", ":8000", "shiftmanager.wsgi"]
