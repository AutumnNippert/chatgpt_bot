# https://github.com/Nv7-GitHub/googlesearch/tree/0f15c701bf08005675f3d9bd4752dc003e071a05

from requests import get
from bs4 import BeautifulSoup
from time import sleep
from ai_interaction import generate_response
def _req(term, results, lang, start, proxies):
    resp = get(
        url="https://www.google.com/search",
        headers={
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
        },
        params=dict(
            q=term,
            num=results + 2,  # Prevents multiple requests
            hl=lang,
            start=start,
        ),
        proxies=proxies,
    )
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0):
    escaped_term = term.replace(" ", "+")

    # Proxy
    proxies = None
    if proxy:
        if proxy.startswith("https"):
            proxies = {"https": proxy}
        else:
            proxies = {"http": proxy}

    # Fetch
    start = 0
    while start < num_results:
        # Send request
        resp = _req(escaped_term, num_results - start, lang, start, proxies)

        # Parse
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", attrs={"class": "g"})
        for result in result_block:
            # Find link, title, description
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find("div", {"style": "-webkit-line-clamp:2"})
            if description_box:
                description = description_box.find("span")
                if link and title and description:
                    start += 1
                    if advanced:
                        yield SearchResult(link["href"], title.text, description.text)
                    else:
                        yield link["href"]
        sleep(sleep_interval)

def digest(url, q):
    resp = get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text()
    #send through ai
    return generate_response(text + '\n\nQuestion, on this article, ' + q)

def google_search(q):
    result = search(q, 1, advanced=True)
    url = next(result).url
    print(url)
    return digest(url, q)

if __name__ == "__main__":
    print(google_search('what is the capital of the united states'))