start:
	uvicorn main:app --reload

up:
	docker-compose up -d

down:
	docker-compose down

psql:
	psql -h 127.0.0.1 -U root -d chinese
