FROM jupyter/scipy-notebook:latest

# Install additional packages for Shipsmart
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    scikit-learn \
    xgboost \
    lightgbm \
    catboost \
    matplotlib \
    seaborn \
    plotly \
    shap \
    tqdm \
    pyyaml \
    python-dotenv

# Set working directory
WORKDIR /home/jovyan

# Copy requirements if exists
COPY requirements.txt /home/jovyan/ 2>/dev/null || true

# Install from requirements
RUN if [ -f requirements.txt ]; then \
    pip install --no-cache-dir -r requirements.txt; \
    fi

# Create notebooks directory
RUN mkdir -p /home/jovyan/notebooks

# Set Jupyter config
RUN echo "c.NotebookApp.contents_manager_class = 'LargeFileManagerAdapter'" >> /home/jovyan/jupyter_notebook_config.py
RUN echo "c.NotebookApp.max_buffer_size = 104857600" >> /home/jovyan/jupyter_notebook_config.py