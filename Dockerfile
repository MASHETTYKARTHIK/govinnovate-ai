FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install streamlit pandas plotly pytest

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app/app.py"]