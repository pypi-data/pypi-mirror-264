from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

#------------------------------
# Airflow DAG definition
#------------------------------
dag = DAG(
    '{{ name }}',
    description='{{ description }}',
    {% if schedule_interval -%}
    schedule_interval='{{ schedule_interval }}',
    {% else -%}
    schedule=None,
    {% endif -%}
    start_date={{ start_date }},
    {% if catchup -%}
    catchup={{ catchup }},
    {% else -%}
    catchup=False,
    {% endif -%}
)

#------------------------------
# Airflow task defintions
#------------------------------
{% for task in tasks %}
{% if task.description -%}
"""
{{ task.description -}}
"""
{% endif -%}
{{ task.name }} = BashOperator(
    task_id='{{ task.name }}',
    bash_command='{{ task.command }}',
    dag=dag
)

{% endfor %}

#------------------------------
# Define the task dependencies
#------------------------------
{{ tasks_order }}

