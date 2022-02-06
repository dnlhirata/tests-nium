.PHONY: test
test:
	docker-compose exec web pytest app/tests