FROM python:slim

# Copy the requirements file and install the dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install cryptography gunicorn pymysql

# Copy application files
COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod a+x boot.sh

# Set the environment variable for the Flask app
ENV FLASK_APP microblog.py

# Compile translation files
RUN flask translate compile

# Expose the application port
EXPOSE 5000

# Set the default command to run the application
ENTRYPOINT ["./boot.sh"]
