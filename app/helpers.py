import sys
import os
import json


def write_params_to_file(path, **kwargs):
    with open(f'{path}/parameters.txt', 'w+') as file:
        print("Parameters:")
        for key, value in kwargs.items():
            file.write(f"{key}={value}\n")
            print(f"{key}={value}")
        print()


def save_scores_for_model(model_path, scores, difficulty, episodes):
    eval_path = f"{'/'.join(model_path.split('/')[:-1])}/evaluation.json"
    model_name = model_path.split('/')[-1:][0]
    if os.path.exists(eval_path):
        with open(eval_path, 'r+') as file:
            data = json.load(file)
            if model_name in data:
                data[model_name][difficulty] = scores
            else:
                data[model_name] = {difficulty: scores}
            file.seek(0)
            json.dump(data, file)
    else:
        with open(eval_path, 'w') as file:
            data = {model_name: {difficulty: scores}}
            json.dump(data, file)


def path_exists(path):
    if os.path.exists(path):
        return True
    else:
        print(f"The path {path} does not exist")
        sys.exit()
