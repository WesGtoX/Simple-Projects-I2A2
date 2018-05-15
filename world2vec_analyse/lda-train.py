import gensim, nltk, logging, multiprocessing, os, json, re, logging
from gensim.models import Word2Vec
from gensim.parsing.preprocessing import stem_text, split_alphanum
from nltk.tokenize import RegexpTokenizer
from gensim.models.word2vec import LineSentence
from gensim import corpora

tokenizer = RegexpTokenizer(r'\w+')
stop_words = nltk.corpus.stopwords.words('english')


logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)
log = logging.getLogger("my-logger")



tokenizer = RegexpTokenizer(r'\w+')
stop_words = nltk.corpus.stopwords.words('english')

pt_stop = []
for stop_word in stop_words:
    pt_stop.append(stop_word.encode('utf-8'))

def funcao_limpa_tudo(artigo):
    tokenizer = RegexpTokenizer(r'\w+')
    lista_nova = []
    #logger.info('Setting it to 0, do not use it in your scoring function.')
    #print(docs)
    artigo = stem_text(artigo)
    artigo = split_alphanum(artigo)
    artigo = tokenizer.tokenize(artigo)

    list_artigo = list(artigo)
    try:
        for palavra in list_artigo:
            palavra = palavra.encode('utf-8')
            if re.match('^\d+$', palavra):
                #artigo.remove(palavra)
                pass
            elif palavra in pt_stop:
                #artigo.remove(palavra)
                pass

            elif len(palavra) < 3:
                #artigo.remove(palavra)
                pass
            else:
                lista_nova.append(palavra)
    except Exception as erro:
        print(erro)
        #numero_palavra = artigo.index(palavra)
        #artigo.pop(numero_palavra) #achou lixo
        pass
    del list_artigo
    del artigo
    #log.info("Lista de Tokens: %s", docs)
    if len(lista_nova) < 5:
        return None
    else:
        return lista_nova

maximo = 50
ja_passou = False

fname = 'enwiki-latest-completo.json'

class MySentences(object):


    def __init__(self, dirname, lista_final):
        self.dirname = dirname
        self.lista_final = lista_final

    def __iter__(self):
        cont = 0
        for fname in os.listdir(self.dirname):
            if cont >= maximo:
                break
            for line in open(os.path.join(self.dirname, fname)):
                line = json.loads(line)
                if cont >= maximo:
                    break
                for paragrafo_artigo in line[u'section_texts']:
                    funct = funcao_limpa_tudo(paragrafo_artigo)
                    if funct != None:
                        self.lista_final.append(funct)
                        if (cont % 1000) == 0:
                            log.info(funct)

                if len(self.lista_final) != 0:
                    dictionary = corpora.Dictionary(self.lista_final)
                    corpus = [dictionary.doc2bow(text) for text in self.lista_final]
                    cont = cont + 1
                    yield corpus, dictionary


for corpus, dictionary in MySentences('/home/marco/projetos/nlp/wikipedia/', []):
    #if ja_passou == False:
    lda = gensim.models.ldamulticore.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=5, chunksize=500, passes=50,  workers=3)
    '''
    topicos = lda.print_topics(num_topics=1, num_words=15)
    topicos = re.findall('([0-9]\.[0-9]{3})\*"([^"]*)"', topicos[0][1])
    top_topics = lda.top_topics(corpus, topn=20)
    
    3 linhas acima eu extraio os topicos usando expressao regular, pro Turing era util.
    '''
    # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
    avg_topic_coherence = sum([t[1] for t in top_topics]) / 5
    print('Average topic coherence: %.4f.' % avg_topic_coherence)
    from pprint import pprint
    pprint(top_topics)


