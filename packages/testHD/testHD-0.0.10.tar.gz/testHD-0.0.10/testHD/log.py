import json
import requests

class ModelRunner:
    def __init__(self, server_url):
        self.server_url = server_url

    def run_model(self, model_name, project_name, input_data, api_key, output_data):
        # 모델 실행 및 결과 반환
        output_data = self._execute_model(model_name, project_name, input_data, api_key)
        
        # 결과를 JSON 형식으로 변환
        json_output = self._format_output(model_name, project_name, input_data, output_data, api_key)
        
        # 결과를 서버로 전송하여 저장
        self._save_to_server(json_output)
        
        # 결과 반환
        return json_output

    def _execute_model(self, model_name, project_name, input_data):
        # 여기에 모델 실행 로직을 구현합니다.
        # 입력 데이터를 사용하여 모델을 실행하고 결과를 반환합니다.
        pass

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

if __name__ == "__main__":
    # 예시 실행 코드
    server_url = "http://localhost:8088/save_data"
    runner = ModelRunner(server_url)
    model_name = "example_model"
    project_name = "example_project"
    input_data = {"key": "value"}
    api_key = "example_api_key"
    output = runner.run_model(model_name, project_name, input_data)
    print(output)