import wikipedia
from bin.utils.ai_interaction import generate_response
#from bin.utils.spacy_interaction import get_wiki_query

def search(q, history=[]):
    #wiki_query = get_wiki_query(q)
    wiki_query = q
    print(f"Wikipedia search: {wiki_query}")
    useable_history = history.copy()
    try:
        page = wikipedia.page(wiki_query)
        summary = page.summary
        link = page.url
        useable_history.append({"role": "system", "content":'If you can\'t find the answer, generate a response as best you can but mention that it is not from wikipedia in bold.'})
        useable_history.append({"role": "user", "content":f'Context: {summary}\nQuestion: {q}\nAnswer: '})
        return '<' + link + '>\n' + generate_response(history=useable_history, personality=True)
    except Exception as e:
        print('Wikipedia error')
        useable_history = history.copy()
        useable_history.append({"role": "user", "content":f'Question: {q}\nAnswer: '})
        return generate_response(history=useable_history, personality=True)

if __name__ == "__main__":
    print(search('Whats the best weapon in elden ring?'))