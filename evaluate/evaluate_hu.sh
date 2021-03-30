SECONDS=0 # Reset seconds counter to measure execution time

#dirs="./app/checkpoints/lr/*/"
#dirs="./app/checkpoints/hu/*/"
dirs=(
  ./app/checkpoints/hu/hu5/
  ./app/checkpoints/hu/hu10/
  ./app/checkpoints/hu/hu20/
  ./app/checkpoints/hu/hu40/
  ./app/checkpoints/hu/hu60/
  ./app/checkpoints/hu/hu90/
  ./app/checkpoints/hu/hu120/
  ./app/checkpoints/hu/hu150/
)
hus=(5 10 20 40 60 90 120 150)
i=0

# Loop through each checkpoint file and start evaluation
for dir in "${dirs[@]}"; do
  for port in {8001..8003}; do
    container_ids+=("$(docker run -d -p "$port":8001 gnubg:latest)")
  done
  sleep 3 #Wait for the containers to boot properly
  for file in "$dir"*.tar; do
    echo "$file - ${hus[i]}"
    gnome-terminal --geometry 70x19+1920--90 --disable-factory -- python ./app/main.py evaluate \
      --episodes 100 --hidden_units0 "${hus[i]}" --model0 "$file" vs_random &
    pid1=$!
    gnome-terminal --geometry 70x19+1920+-10 --disable-factory -- python ./app/main.py evaluate \
      --episodes 100 --hidden_units0 "${hus[i]}" --model0 "$file" vs_gnubg --difficulty Beginner --host localhost --port 8001 &
    pid2=$!
    gnome-terminal --geometry 70x19--94--90 --disable-factory -- python ./app/main.py evaluate \
      --episodes 100 --hidden_units0 "${hus[i]}" --model0 "$file" vs_gnubg --difficulty Intermediate --host localhost --port 8002 &
    pid3=$!
    gnome-terminal --geometry 70x19--94+-10 --disable-factory -- python ./app/main.py evaluate \
      --episodes 100 --hidden_units0 "${hus[i]}" --model0 "$file" vs_gnubg --difficulty Expert --host localhost --port 8003 &
    pid4=$!
    wait $pid1 $pid2 $pid3 $pid4 # Wait for the above processes to finish
  done
  #Remove containers, they get too big after a while
  for id in "${container_ids[@]}"; do
    docker container stop $id
    docker container rm $id
  done
  unset container_ids
  i=$((i + 1))
done

echo "Total time: $((SECONDS / 3600))hrs $(((SECONDS / 60) % 60))min $((SECONDS % 60))sec"

#geometry 70x19+1920--90 - bottom left
#geometry 70x19+1920+344 - middle left
#geometry 70x19+1920+-10 - upper left
#geometry 70x19+2564+-23 - bottom middle
#geometry 70x19+2564--90 - upper middle
#geometry 70x19--94--90 - bottom right
#geometry 70x19--94+344 - middle right
#geometry 70x19--94+-10 - upper right
