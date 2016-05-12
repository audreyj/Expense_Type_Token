FROM continuumio/miniconda3

# Update conda and install python packages
RUN conda update -y conda
RUN conda install -y pandas=0.17.0 \
					 tornado=4.2.1 \
					 scikit-learn=0.17
# Copy data in
COPY Type_Server.py /opt/api/data/
COPY Type_Classifier.py /opt/api/

WORKDIR /opt/api
EXPOSE 8889
