from locust import HttpUser, between, task


class LoadTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_all_books(self):
        self.client.get('/library/books')

    @task
    def post_book(self):
        self.client.post(
            '/library/book',
            json={
                'title': 'TituloX',
                'author': 'AutorX',
                'category': 'suspense',
            },
        )

    @task
    def get_byid_book(self):
        self.client.get('/library/book/1')

    @task
    def get_search_book(self):
        self.client.get('/library/book/?search=TituloX')

