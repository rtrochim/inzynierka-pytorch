mkdir ./app/checkpoints/lr/lr001 -p && python ./app/main.py train --save_path ./app/checkpoints/lr/lr001 --save_step 100 --episodes 10000 --name lr001 --alpha 0.01 --hidden_units 40
mkdir ./app/checkpoints/lr/lr005 -p && python ./app/main.py train --save_path ./app/checkpoints/lr/lr005 --save_step 100 --episodes 10000 --name lr005 --alpha 0.05 --hidden_units 40
mkdir ./app/checkpoints/lr/lr01 -p && python ./app/main.py train --save_path ./app/checkpoints/lr/lr01 --save_step 100 --episodes 10000 --name lr01 --alpha 0.1 --hidden_units 40
mkdir ./app/checkpoints/lr/lr03 -p && python ./app/main.py train --save_path ./app/checkpoints/lr/lr03 --save_step 100 --episodes 10000 --name lr03 --alpha 0.3 --hidden_units 40
mkdir ./app/checkpoints/lr/lr05 -p && python ./app/main.py train --save_path ./app/checkpoints/lr/lr05 --save_step 100 --episodes 10000 --name lr05 --alpha 0.5 --hidden_units 40
mkdir ./app/checkpoints/lr/lr07 -p && python ./app/main.py train --save_path ./app/checkpoints/lr/lr07 --save_step 100 --episodes 10000 --name lr07 --alpha 0.7 --hidden_units 40
mkdir ./app/checkpoints/lr/lr09 -p && python ./app/main.py train --save_path ./app/checkpoints/lr/lr09 --save_step 100 --episodes 10000 --name lr09 --alpha 0.9 --hidden_units 40
mkdir ./app/checkpoints/lr/lr1 -p && python ./app/main.py train --save_path ./app/checkpoints/lr/lr1 --save_step 100 --episodes 10000 --name lr1 --alpha 1 --hidden_units 40

mkdir ./app/checkpoints/lambda/lambda001 -p && python ./app/main.py train --save_path ./app/checkpoints/lambda/lambda001 --save_step 100 --episodes 10000 --name lambda001 --alpha 0.1 --lambda_param 0.01 --hidden_units 40
mkdir ./app/checkpoints/lambda/lambda005 -p && python ./app/main.py train --save_path ./app/checkpoints/lambda/lambda005 --save_step 100 --episodes 10000 --name lambda005 --alpha 0.1 --lambda_param 0.05 --hidden_units 40
mkdir ./app/checkpoints/lambda/lambda01 -p && python ./app/main.py train --save_path ./app/checkpoints/lambda/lambda01 --save_step 100 --episodes 10000 --name lambda01 --alpha 0.1 --lambda_param 0.1 --hidden_units 40
mkdir ./app/checkpoints/lambda/lambda03 -p && python ./app/main.py train --save_path ./app/checkpoints/lambda/lambda03 --save_step 100 --episodes 10000 --name lambda03 --alpha 0.1 --lambda_param 0.3 --hidden_units 40
mkdir ./app/checkpoints/lambda/lambda05 -p && python ./app/main.py train --save_path ./app/checkpoints/lambda/lambda05 --save_step 100 --episodes 10000 --name lambda05 --alpha 0.1 --lambda_param 0.5 --hidden_units 40
mkdir ./app/checkpoints/lambda/lambda07 -p && python ./app/main.py train --save_path ./app/checkpoints/lambda/lambda07 --save_step 100 --episodes 10000 --name lambda07 --alpha 0.1 --lambda_param 0.7 --hidden_units 40
mkdir ./app/checkpoints/lambda/lambda09 -p && python ./app/main.py train --save_path ./app/checkpoints/lambda/lambda09 --save_step 100 --episodes 10000 --name lambda09 --alpha 0.1 --lambda_param 0.9 --hidden_units 40
mkdir ./app/checkpoints/lambda/lambda1 -p && python ./app/main.py train --save_path ./app/checkpoints/lambda/lambda1 --save_step 100 --episodes 10000 --name lambda1 --alpha 0.1 --lambda_param 1 --hidden_units 40

mkdir ./app/checkpoints/hu/hu5 -p && python ./app/main.py train --save_path ./app/checkpoints/hu/hu5 --save_step 100 --episodes 10000 --name hu5 --alpha 0.1 --hidden_units 5
mkdir ./app/checkpoints/hu/hu10 -p && python ./app/main.py train --save_path ./app/checkpoints/hu/hu10 --save_step 100 --episodes 10000 --name hu10 --alpha 0.1 --hidden_units 10
mkdir ./app/checkpoints/hu/hu20 -p && python ./app/main.py train --save_path ./app/checkpoints/hu/hu20 --save_step 100 --episodes 10000 --name hu20 --alpha 0.1 --hidden_units 20
mkdir ./app/checkpoints/hu/hu40 -p && python ./app/main.py train --save_path ./app/checkpoints/hu/hu40 --save_step 100 --episodes 10000 --name hu40 --alpha 0.1 --hidden_units 40
mkdir ./app/checkpoints/hu/hu60 -p && python ./app/main.py train --save_path ./app/checkpoints/hu/hu60 --save_step 100 --episodes 10000 --name hu60 --alpha 0.1 --hidden_units 60
mkdir ./app/checkpoints/hu/hu90 -p && python ./app/main.py train --save_path ./app/checkpoints/hu/hu90 --save_step 100 --episodes 10000 --name hu90 --alpha 0.1 --hidden_units 90
mkdir ./app/checkpoints/hu/hu120 -p && python ./app/main.py train --save_path ./app/checkpoints/hu/hu120 --save_step 100 --episodes 10000 --name hu120 --alpha 0.1 --hidden_units 120
mkdir ./app/checkpoints/hu/hu150 -p && python ./app/main.py train --save_path ./app/checkpoints/hu/hu150 --save_step 100 --episodes 10000 --name hu150 --alpha 0.1 --hidden_units 150
