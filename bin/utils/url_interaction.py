from bs4 import BeautifulSoup
import requests
from bin.utils.misc import num_tokens_from_messages
import re

CLEANR = re.compile('<[^>]*>')


def scrape_site(url) -> list:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        res = requests.get(url, headers=headers)
        class_names = ['article__main', 'mw-body-content', 'inner-content', 'content', 'article', 'main']
        response = []

        soup = BeautifulSoup(res.text, 'html.parser')
        content = None

        # content = soup.main
        # print(content)
        # if content != None:
        #     print ("Main way")
        #     content = str(content)
        #     content = cleanhtml(content)
        #     list_content = content.split('\n')
        #     for item in list_content:
        #         if item != '':
        #             response.append({"role": "system", "content": item})
        #             if num_tokens_from_messages(response) > 3800:
        #                 print ("Content is too long to digest. Consuming only the first 4000 tokens.")
        #                 response.append({"role": "system", "content": "Notify user: The Content is too long to digest. Consuming only the first 4000 tokens."})
        #                 break
            
        #     return response

        # if content == None:
        #     content = soup.find('div', {'class': 'main-content'})
        #     for class_name in class_names:
        #         content = soup.find('div', {'class': class_name})
        #         if content != None:
        #             break
        #     print ("New way")
        #     #break down str(content) into a list of strings
        #     content_str = str(content)
        #     content_str = cleanhtml(content_str)
        #     list_content = content_str.split('\n')
        #     for item in list_content:
        #         if item != '':
        #             response.append({"role": "system", "content": item})
        #             if num_tokens_from_messages(response) > 3800:
        #                 print ("Content is too long to digest. Consuming only the first 3800 tokens.")
        #                 response.append({"role": "system", "content": "Notify user: The Content is too long to digest. Consuming only the first 4000 tokens."})
        #                 break

        if content == None: # Old way of doing it
            print ("Consuming URL")
            content = soup.body
            #remove nav
            #remove script

            to_delete = ['script', 'nav', 'footer', 'aside', 'style']
            for tag in to_delete:
                for match in content.findAll(tag):
                    match.decompose()
                
            
            #break down str(content) into a list of strings
            content_str = str(content)
            content_str = cleanhtml(content_str)
            print(content_str)
            list_content = content_str.split('\n')
            for item in list_content:
                if item != '':
                    response.append({"role": "system", "content": item})
                    if num_tokens_from_messages(response) > 3800:
                        print ("Content is too long to digest. Consuming only the first 3800 tokens.")
                        #remove last item
                        print('only got as far as ' + str(response.pop()))
                        response.append({"role": "system", "content": "Notify user: The Content is too long to digest. Consuming only the first 3800 tokens."})
                        break

        # if content == None: # Old way of doing it
        #     print ("Old way")
        #     #get all h1 tags
        #     h1s = soup.select('h1')
        #     if len(h1s) != 0:
        #         h1s = [h1.text for h1 in h1s]
        #         response.append({"role": "system", "content": "h1s: " + ", ".join(h1s)})
            
        #     h2s = soup.select('h2')
        #     if len(h2s) != 0:
        #         h2s = [h2.text for h2 in h2s]
        #         response.append({"role": "system", "content": "h2s: " + ", ".join(h2s)})
                
        #     h3s = soup.select('h3')
        #     if len(h3s) != 0:
        #         h3s = [h3.text for h3 in h3s]
        #         response.append({"role": "system", "content": "h3s: " + ", ".join(h3s)})

        #     h4s = soup.select('h4')
        #     if len(h4s) != 0:
        #         h4s = [h4.text for h4 in h4s]
        #         response.append({"role": "system", "content": "h4s: " + ", ".join(h4s)})

        #     h5s = soup.select('h5')
        #     if len(h5s) != 0:
        #         h5s = [h5.text for h5 in h5s]
        #         response.append({"role": "system", "content": "h5s: " + ", ".join(h5s)})

        #     ps = soup.select('p')
        #     if len(ps) != 0:
        #         ps = [p.text for p in ps]
        #         response.append({"role": "system", "content": "ps: " + ", ".join(ps)})

        return response
    
    except Exception as e:
        print(e)
        return None

def cleanhtml(raw_html):
    if raw_html == None:
        return None
    #remove javascript (accounting for parameters within the script tag)
    cleantext = re.sub(r'<script.*?>.*?</script>', '', raw_html)

    #remove css
    cleantext = re.sub(r'<style.*?>.*?</style>', '', cleantext)

    #remove html comments
    cleantext = re.sub(r'<!--.*?-->', '', cleantext)

    #remove CDATA
    cleantext = re.sub(r'<!\[CDATA\[.*?\]\]>', '', cleantext)


    #remove html tags
    cleantext = re.sub(CLEANR, '', cleantext)

    #remove newlines only if there are 1 or more
    cleantext = re.sub(r'\n{1,}', '\n', cleantext)


    return cleantext