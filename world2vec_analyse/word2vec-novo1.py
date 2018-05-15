import multiprocessing, gc
from gensim.corpora.wikicorpus import WikiCorpus
from gensim.models.word2vec import Word2Vec
import gensim, smart_open, json, re, nltk, logging
from gensim.corpora import MmCorpus
from nltk.tokenize import RegexpTokenizer
from gensim.summarization import textcleaner
from gensim.parsing.preprocessing import split_alphanum, stem_text

import time, json
import sys
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)
log = logging.getLogger("my-logger")


#wiki = WikiCorpus('/home/marco/projetos/nlp/wikipedia/enwiki-latest-pages-articles.xml.bz2', lemmatize=False)


# word2vec
lista = ['See also', 'References', 'External links']
docs = []
cont = 0
cont_aux = 0

pt_stop = nltk.corpus.stopwords.words('english')    # nltk.download('stopwords')
tokenizer = RegexpTokenizer(r'\w+')
stop_words = []

for stop_word in pt_stop:
    stop_words.append(stop_word.encode('utf-8'))

del pt_stop

lista_nova = []

def funcao_limpa_tudo(artigo):  #limpa a palavra, limita a palavra em uma
    lista_nova = []
    #logger.info('Setting it to 0, do not use it in your scoring function.')
    #print(docs)
    artigo = stem_text(artigo)
    artigo = split_alphanum(artigo)
    artigo = tokenizer.tokenize(artigo) #artigo vira uma lista com todas as palavras

    list_artigo = list(artigo)  #pesquisar o que é o list
    try:
        for palavra in list_artigo:
            palavra = palavra.encode('utf-8')
            if re.match('^\d+$', palavra):
                #artigo.remove(palavra)
                pass
            elif palavra in stop_words:
                #artigo.remove(palavra)
                pass

            elif len(palavra) < 3:
                #artigo.remove(palavra)
                pass
            else:
                lista_nova.append(palavra)  #recebe palavra util
    except Exception as erro:   #evita travar o codigo e continua, 
        numero_palavra = artigo.index(palavra)
        artigo.pop(numero_palavra) #achou lixo

    del list_artigo #garbage do python
    #log.info("Lista de Tokens: %s", docs)
    if len(lista_nova) < 5:
        return None
    else:
        return lista_nova


filename = 'D:\CURSOS\I2A2\Projects-I2A2\world2vec_analyse_py\enwiki-latest.json.json'

with open(filename, 'r') as file:
    for line in file:
        artigo = json.loads(line) #transforma a linha no objeto


        if cont > 1000:    #limita a quantidade de memória usada
            break
        if (cont % 100) == 0:   #imprimir o log de arquivo
            log.info("Lido com sucesso %s" , str(cont))
        for paragrafo_artigo in artigo[u'section_texts']:
            paragraph_pre = funcao_limpa_tudo(paragrafo_artigo)
            if paragraph_pre != None:
                docs.append(paragraph_pre)  #junção de todos os artigos 
            #print(paragrafo_artigo)
                #cont = cont + 1
        cont = cont + 1
        gc.collect()

print('Acabei pre processamento')
print('Tamanho do docs: ', len(docs))

'''#time.sleep(20)

print('Comecar bigram')
bigram_transformer = gensim.models.Phrases(docs)
print('Comecar trigram')
trigram_transformer = gensim.models.Phrases(bigram_transformer[docs])
print('Salvar modelo trigram.')
trigram_transformer.save("/home/administrator/projects/mrturing/models/trigram-model.model")
del bigram_transformer
params = {'size': 300, 'window': 10, 'min_count': 40,'workers': max(1, multiprocessing.cpu_count() - 1), 'sample': 1e-3, }
print('Comecar treinar word2vec')
word2vec = Word2Vec(trigram_transformer[docs], **params)
word2vec.save('/home/administrator/projects/mrturing/models/wiki.word2vec-teste.model')'''
