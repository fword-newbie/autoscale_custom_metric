import os
import time
import yaml


def check_file_exists():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "999.yaml")

    if os.path.exists(file_path):
        return True
    else:
        return False


def check_yaml_contains_deployment():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "999.yaml")
    with open(file_path, "r") as f:
        yaml_content = yaml.load_all(f,yaml.FullLoader)
        yaml_content = list(yaml_content)
        for i in yaml_content:
            if yaml_content[0]["kind"] == "Deployment":
                return True
            else:
                return False

def check_deployment_label():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "999.yaml")
    with open(file_path, "r") as f:
        yaml_content = yaml.load_all(f,yaml.FullLoader)
        yaml_content = list(yaml_content)
        if "auto_build_vpa" in yaml_content[0]["metadata"]["labels"]:
            if yaml_content[0]["metadata"]["labels"]["auto_build_vpa"] == "ye":
                return True
            else:
                return False
        

def export_deployment_yaml():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "999.yaml")

    with open(file_path, "r") as f:
        deployment_yaml = list(yaml.load_all(f,yaml.FullLoader))
        deployment_name = deployment_yaml[0]["metadata"]["name"]
        deployment_yaml[0]["spec"]["template"]["metadata"]["labels"]["version"] = "v2"
        new_file_name = f"{deployment_name}.yaml"
        new_file_path = os.path.join(current_dir, new_file_name)

        with open(new_file_path, "w") as new_file:
            yaml.dump(deployment_yaml[0], new_file)

        os.remove(file_path)

while True:
    if not check_file_exists():
        time.sleep(1)
        continue

    if not check_yaml_contains_deployment():
        print("nd")
        os.remove("999.yaml")
        continue

    if not check_deployment_label():
        os.remove("999.yaml")
        continue
    
    export_deployment_yaml()

