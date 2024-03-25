from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Define the DAG
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

{% for task in tasks %}
# Define the BashOperator task
{{ task.name }} = BashOperator(
    task_id='{{ task.name }}',
    bash_command='{{ task.command }}',
    dag=dag
)
{% endfor %}

# Define the task dependencies
{{ tasks_order }}

