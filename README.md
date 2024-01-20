# VoteChain : Backend

This repo contains backend code for votechain. blockchain based e-votting system. This is used to accomplish the tasks the blockchain alone couldn't.

> hosted on : https://votechain-backend.vercel.app

### Tech Stack

- django
- django restframework
- djongo

### Setup

- clone repo
- install requirements

  ```bash
  pip install -r requirements.txt
  ```

- setup environment and database
- run the server

  ```
  python manage.py runserver
  ```

- For running websockets you want to setup redis server and corresponding envs

```bash
redis-server
```
