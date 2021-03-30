SECONDS=0 # Reset seconds counter to measure execution time

files=(
#  "./app/checkpoints/best2/best2_100000.tar"
  "./app/checkpoints/best3/best3_100000.tar"
  )

difficulties=( "Beginner" "Casual" "Intermediate" "Advanced" "Expert" "WorldClass" "Supremo" "Grandmaster")

for file in "${files[@]}"; do
  for port in {8001..8001}; do
    container_ids+=("$(docker run -d -p "$port":8001 gnubg:latest)")
  done
  sleep 3 #Wait for the containers to boot properly
  for difficulty in "${difficulties[@]}"; do
    python ./app/main.py evaluate --episodes 100 --hidden_units0 20 --model0 "$file" vs_gnubg --difficulty "$difficulty" --host localhost --port 8001
  done
  for id in "${container_ids[@]}"; do
    docker container stop $id
    docker container rm $id
  done
  unset container_ids
done

echo "Total time: $((SECONDS / 3600))hrs $(((SECONDS / 60) % 60))min $((SECONDS % 60))sec"
