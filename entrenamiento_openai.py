# -*- coding: utf-8 -*-
"""entrenamiento openai.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ktEEyUI9JTZZHr5yH6Phvx6fbNJaaHWf
"""

pip install --upgrade openai

from openai import OpenAI
from time import sleep

# Initialize OpenAI client
client = OpenAI(api_key ="TU_API_KEY_AQUI")

"""Subir archivo de entrenamiento de OpenAI"""

def upload_training_file(file_path):
    """Upload training file to OpenAI"""
    with open("/content/FineTuningTest/iocs_mejorado_chat.jsonl", "rb") as file:
        response = client.files.create(
            file=file,
            purpose="fine-tune"
        )
        return response.id
training_file_id = upload_training_file("training_data.jsonl")
training_file_id

"""Creando job de fine tuning"""

def create_fine_tuning_job(training_file_id, model="gpt-4o-mini-2024-07-18"):
    """Create a fine-tuning job"""
    response = client.fine_tuning.jobs.create(
        training_file=training_file_id,

        model=model
    )
    return response.id

# Start the fine-tuning job
model = "gpt-4o-mini-2024-07-18"
job_id = create_fine_tuning_job(training_file_id, model)
job_id

"""Monitorear progreso de entrenamiento"""

def monitor_job(job_id):
    """Monitor fine-tuning job progress"""
    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        print(f"Status: {job.status}")

        if job.status in ["succeeded", "failed"]:
            return job

        # List latest events
        events = client.fine_tuning.jobs.list_events(
            fine_tuning_job_id=job_id,
            limit=5
        )
        for event in events.data:
            print(f"Event: {event.message}")

        sleep(5)  # Check every 30 seconds
        # Monitor the job until completion
job = monitor_job(job_id)
if job.status == "succeeded":
    fine_tuned_model = job.fine_tuned_model
    print(f"Fine-tuned model ID: {fine_tuned_model}")
else:
    print("Fine-tuning failed.")

def get_job_events(job_id):
    """Retrieve the events of a specific fine-tuning job."""
    response = client.fine_tuning.jobs.list_events(
        fine_tuning_job_id=job_id,
        limit=20  # Opcional: ajusta el límite según tus necesidades
    )
    for event in response.data:
        print(f"Timestamp: {event.created_at}, Message: {event.message}")
    return response.data

# Reemplaza con tu Job ID
job_id = "TU_JOB_ID_AQUI"
events = get_job_events(job_id)

"""Testing del modelo"""

def get_job_events(job_id):
    """Retrieve the events of a specific fine-tuning job."""
    response = client.fine_tuning.jobs.list_events(
        fine_tuning_job_id=job_id,
        limit=20  # Opcional: ajusta el límite según tus necesidades
    )
    for event in response.data:
        print(f"Timestamp: {event.created_at}, Message: {event.message}")
    return response.data
job_id = "TU_JOB_ID_AQUI"
events = get_job_events(job_id)

def test_model(model_id, test_input):
    """Test the fine-tuned model for IoC analysis"""
    completion = openai.ChatCompletion.create(
        model=model_id,
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un analista de ciberseguridad experto en indicadores de compromiso (IoCs). "
                    "Tu tarea es analizar los eventos de seguridad y proporcionar análisis detallados "
                    "y recomendaciones claras basadas en las mejores prácticas de ciberseguridad."
                )
            },
            {"role": "user", "content": test_input}
        ]
    )
    return completion.choices[0].message

test_input = (
    "Analiza el siguiente evento de seguridad. Tipo: Dominio. Valor: streetsave.club. "
    "Fuente: https://www.malware-traffic-analysis.net/2017/12/22/index.html. "
    "Detalles: Standard query 0xb52d A streetsave.club"
)

# ID del modelo afinado (reemplázalo con el ID real de tu modelo afinado)
model_id = "fine_tuned_model_id"

# Probar el modelo
response = test_model(model_id, test_input)

# Mostrar la respuesta generada por el modelo
print("Respuesta del modelo:")
print(response["content"])