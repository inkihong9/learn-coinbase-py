# Crypto Portfolio Tracker
This project is a Python-based application designed to provide a high-level overview of cryptocurrency trading activities by integrating with the Coinbase Advanced API.

The system automatically:
- Fetches account balances and order history from Coinbase
- Tracks investments, realized and unrealized profit/loss
- Breaks down performance by individual coins as well as overall portfolio
- Stores data in a MySQL database for persistence and analysis

The backend is written in Python with SQLAlchemy for ORM and uses Docker for containerization. The architecture consists of:
- Python app container – interacts with Coinbase API, processes trades, and calculates metrics
- MySQL container – stores transactions, balances, and calculated results

The long-term goal of the project is to expose this backend as a service and eventually build a single-page application (SPA) dashboard (likely in React) hosted on AWS for visualization.

# Setup Instructions
1. i went to the directory where i wanna clone my repository
2. then i cloned it - `git clone https://github.com/inkihong9/learn-coinbase-py.git`
3. i changed directory to the repository's root directory
4. run command `docker compose up --build -d`
5. i also need to run `git config --global user.email "my@email.com"`
6. and run `git config --global user.name "my name"`

# What to do when docker-compose.yml is edited

1. for database, as long as i don't delete the volume, data will persist
2. need to delete (or rename) the containers first
3. then run command `docker compose up --build -d`
