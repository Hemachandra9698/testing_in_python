import requests


def process_get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        print('Success!')
        return response.json()
    elif response.status_code == 404:
        print('Failed')
        return None


class HttpClass:
    def process_get_request(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            print('Success!')
            return response.json()
        elif response.status_code == 404:
            print('Failed')
            return None


class SearchRepo:
    def call_http_class(self, url):
        http_obj = HttpClass()
        res = http_obj.process_get_request(url)
        if res:
            return res
        raise ValueError("No response received from the API")

    def search_repo_with_name(self, url, repo_name):
        res = self.call_http_class(url)
        # search for key "repos" in the response
        if "repos" in res:
            repos = res["repos"]
            # find the repo_name
            if repo_name in repos:
                return True
            # if there is no repo then return False
            return False
        # if there is no "repos" key then raise error
        raise ValueError("repos not found in response")


if __name__ == "__main__":
    url = 'https://api.github.com'
    search_repo_obj = SearchRepo()
    repo_name = "donuts"
    found = search_repo_obj.search_repo_with_name(url, repo_name)
    print(found)
