# steps i took

1. i went to the directory where i wanna clone my repository
2. then i cloned it - `git clone https://github.com/inkihong9/learn-coinbase-py.git`
3. i changed directory to the repository's root directory
4. run command `docker compose up --build -d`
5. i also need to run `git config --global user.email "my@email.com"`
6. and run `git config --global user.name "my name"`

# in case docker-compose.yml is edited

1. for database, as long as i don't delete the volume, data will persist
2. need to delete (or rename) the containers first
3. then run command `docker compose up --build -d`