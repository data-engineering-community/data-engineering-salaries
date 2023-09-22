FROM python:3.10

COPY . /app
WORKDIR /app

# Install packages required for Streamlit app
RUN pip install -r requirements.txt

# Command to run streamlit app
ENTRYPOINT ["streamlit", "run", "app.py"]
