# A Makefile gives you short, memorable commands instead of long docker
# commands. This is our "light DevOps from day one" — not a full CI/CD
# pipeline yet, just consistent local tooling.

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

logs:
	docker compose logs -f

restart: down up
