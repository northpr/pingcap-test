# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/tidb_connect.ipynb (unless otherwise specified).

__all__ = ['PUBLIC_KEY', 'PRIVATE_KEY', 'REGION', 'APP_ID', 'cluster_id', 'database', 'Chat2QueryAPI',
           'print_pretty_result']

# Cell
import requests
import time

PUBLIC_KEY = '414VD1N0'
PRIVATE_KEY = 'aefec559-36eb-4cd1-b6c3-59fa74303d41'
REGION = 'ap-southeast-1'
APP_ID = 'WizQVcwy'

cluster_id = '10954456779882628977'
database = 'test'

# Cell
class Chat2QueryAPI:
    def __init__(self, public_key, private_key, region, app_id, cluster_id, database):
        self.public_key = public_key
        self.private_key = private_key
        self.region = region
        self.app_id = app_id
        self.cluster_id = cluster_id
        self.database = database
        self.base_url = f'https://{region}.data.tidbcloud.com/api/v1beta/app/chat2query-{app_id}'

    def _make_request(self, endpoint, method="get", params=None, json=None):
        url = f'{self.base_url}/{endpoint}'
        auth = requests.auth.HTTPDigestAuth(self.public_key, self.private_key)
        headers = {'Content-Type': 'application/json'}

        if method.lower() == "post":
            response = requests.post(url, auth=auth, headers=headers, json=json)
        else:
            response = requests.get(url, auth=auth, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return response.text

    def post_data_summary(self):
        payload = {'cluster_id': self.cluster_id, 'database': self.database}
        return self._make_request("endpoint/v2/dataSummaries", "post", json=payload)

    def get_data_summary(self):
        params = {'cluster_id': self.cluster_id, 'database': self.database}
        return self._make_request("endpoint/v2/dataSummaries", "get", params=params)

    def get_job_status(self, job_id):
        return self._make_request(f"endpoint/v2/jobs/{job_id}")

    def execute_sql(self, raw_question):
        payload = {'cluster_id': self.cluster_id, 'database': self.database, 'raw_question': raw_question}
        return self._make_request("endpoint/v2/chat2data", "post", json=payload)

    def get_sql_job_result(self, raw_question, full=False):
        execution_result = self.execute_sql(raw_question)
        job_id = execution_result.get('result', {}).get('job_id')

        if not job_id:
            return {"error": "Job ID not found in execution result"}
        print('Generating Result')
        time.sleep(10)  # Wait for the job to process
        job_status_result = self.get_job_status(job_id)

        if full:
            return job_status_result

        # Adjusting the structure to match the provided example
        job_result = job_status_result.get('result', {}).get('result', {})
        task_tree = job_result.get('task_tree', {}).get('0', {})

        simplified_result = {
            'clarified_task': task_tree.get('clarified_task', 'Not specified'),
            'sql_query': task_tree.get('sql', 'Not specified'),
            'columns': [col['col'] for col in task_tree.get('columns', [])] if 'columns' in task_tree else [],
            'rows': task_tree.get('rows', []) if 'rows' in task_tree else []
        }

        return simplified_result

def print_pretty_result(result):
    for key, value in result.items():
        if isinstance(value, list):  # For 'Columns' and 'Rows'
            print(f"{key}:")
            if key == "rows":
                # Assuming you want a tabular-like print for rows
                for row in value:
                    print("    ", ", ".join(str(item) for item in row))
            else:
                # Print the list items for 'Columns'
                print("    ", ", ".join(value))
        else:
            print(f"{key}: {value}")