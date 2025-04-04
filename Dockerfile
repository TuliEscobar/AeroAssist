FROM public.ecr.aws/lambda/python:3.11

# Copiar los archivos de requerimientos primero para aprovechar la caché de capas de Docker
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app.py ${LAMBDA_TASK_ROOT}/
COPY rag_engine.py ${LAMBDA_TASK_ROOT}/
COPY faq_data.json ${LAMBDA_TASK_ROOT}/
COPY entry.sh ${LAMBDA_TASK_ROOT}/

# Hacer el script de entrada ejecutable
RUN chmod +x ${LAMBDA_TASK_ROOT}/entry.sh

# Configurar el comando de entrada
ENTRYPOINT [ "/var/task/entry.sh" ] 