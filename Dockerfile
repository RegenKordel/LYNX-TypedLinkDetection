FROM continuumio/anaconda3:2022.05

WORKDIR /lynx
COPY conda.yml .

RUN conda env create -f conda.yml

CMD [ "conda", "run", "--no-capture-output", "-n", "tld", "jupyter", "notebook", "--allow-root", "--ip", "0.0.0.0", "--port", "8888" ]
