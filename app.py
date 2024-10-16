import os
from google.cloud import storage, bigquery
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def load_csv_to_bigquery(bucket_name, csv_file_name, dataset_id, table_id, schema):
    storage_client = storage.Client()
    bigquery_client = bigquery.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(csv_file_name)

    table_ref = bigquery_client.dataset(dataset_id).table(table_id)

    job_config = bigquery.LoadJobConfig(
    schema=schema,
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # Added this line to truncate the table
)


    job = bigquery_client.load_table_from_file(
        file_obj=blob.open("rb"),
        destination=table_ref,
        job_config=job_config
    )

    job.result()

    return f"Dados inseridos com sucesso na tabela {table_id}."


@app.route('/load-data', methods=['POST'])
def load_data():
    try:
        logging.info("Iniciando o carregamento dos dados")

        data = request.get_json()

        bucket_name = data.get('BUCKET_NAME')
        csv_file_name = data.get('CSV_FILE_NAME')
        dataset_id = data.get('DATASET_ID')
        table_id = data.get('TABLE_ID')
        schema = data.get('schema', [])

        schema = [bigquery.SchemaField(field['name'], field['type']) for field in schema]

        result = load_csv_to_bigquery(bucket_name, csv_file_name, dataset_id, table_id, schema)
        
        logging.info("Carregamento concluído com sucesso")
        return jsonify({"message": result}), 200
    except Exception as e:
        logging.error(f"Erro ao carregar os dados: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
