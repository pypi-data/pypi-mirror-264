import requests
import json

class ModelRunner:

    server_url = "http://localhost:8088/save_data"

    def run_model(self, model_name, project_name, input_data, api_key, output_data=None):
        
        # 결과를 JSON 형식으로 변환
        json_output = self._format_output(model_name, project_name, input_data, output_data, api_key)
        
        print(json_output)
        
        # 결과를 서버로 전송하여 저장
        self._save_to_server(json_output)
        
        # 결과 반환
        return json_output

    def _format_output(self, model_name, project_name, input_data, output_data, api_key):
        # 결과를 JSON 형식으로 포맷팅합니다.
        result = {
            "model_name": model_name,
            "project_name": project_name,
            "input_data": input_data,
            "output_data": output_data,
            "api_key": api_key
        }
        return json.dumps(result)

    def _save_to_server(self, data):
        # 서버로 데이터를 전송하여 저장합니다.
        response = requests.post(self.server_url, json=data)
        if response.status_code == 200:
            print("Data successfully saved to server.")
        else:
            print("Failed to save data to server.")
            print(response.status_code)
