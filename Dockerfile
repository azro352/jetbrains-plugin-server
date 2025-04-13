ARG FROM_IMG

FROM ${FROM_IMG}

COPY src src
COPY main.py requirements.txt ./

RUN pip install -r requirements.txt

CMD ["uvicorn", "--workers", "1", "--host", "0.0.0.0", "--port", "5001", "main:app"]