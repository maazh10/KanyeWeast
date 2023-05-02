FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt /app
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY lyrics /app/lyrics
COPY database.db /app
COPY roasts.txt /app
COPY secrets.json /app
COPY play.mp3 /app
COPY banned_users.pkl /app
COPY commit_message.txt /app

COPY cogs /app/cogs
COPY main.py /app

# Run app.py when the container launches
CMD ["python", "main.py"]
