from bs4 import BeautifulSoup
import requests

def scrape_site(url) -> list:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        res = requests.get(url, headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')
        response = []
        #get all h1 tags
        h1s = soup.select('h1')
        if len(h1s) != 0:
            h1s = [h1.text for h1 in h1s]
            response.append({"role": "system", "content": "h1s: " + ", ".join(h1s)})
        
        h2s = soup.select('h2')
        if len(h2s) != 0:
            h2s = [h2.text for h2 in h2s]
            response.append({"role": "system", "content": "h2s: " + ", ".join(h2s)})
            
        h3s = soup.select('h3')
        if len(h3s) != 0:
            h3s = [h3.text for h3 in h3s]
            response.append({"role": "system", "content": "h3s: " + ", ".join(h3s)})

        h4s = soup.select('h4')
        if len(h4s) != 0:
            h4s = [h4.text for h4 in h4s]
            response.append({"role": "system", "content": "h4s: " + ", ".join(h4s)})

        h5s = soup.select('h5')
        if len(h5s) != 0:
            h5s = [h5.text for h5 in h5s]
            response.append({"role": "system", "content": "h5s: " + ", ".join(h5s)})

        ps = soup.select('p')
        if len(ps) != 0:
            ps = [p.text for p in ps]
            response.append({"role": "system", "content": "ps: " + ", ".join(ps)})

        return response
    except Exception as e:
        print(e.with_traceback)
        return [{"role": "system", "content": "Error: An error has occured while scraping the site. Please try again later."}]
