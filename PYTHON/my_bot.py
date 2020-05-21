import tweepy
import time
import random
import API_data_covid


CONSUMER_KEY = '********'
CONSUMER_SECRET = '******'

ACESS_KEY = '*********'
ACESS_SECRET = '*********'

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACESS_KEY,ACESS_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)



mentions = api.mentions_timeline()
nome_Arq = 'ultimoVisto.txt'


def ultimo_visto(nomeArquivo):
    f_read = open(nome_Arq)
    ultimo = int(f_read.read().strip())
    f_read.close()
    return ultimo

def armazenar_Ultimo_Visto(ultimo_id_visualizado, nome_Arq):
    f_write = open(nome_Arq,'w')
    f_write.write(str(ultimo_id_visualizado))
    f_write.close()

def responder_Mensionado():
    ultimo_id = ultimo_visto(nome_Arq)
    mentions = api.mentions_timeline(ultimo_id,
                                tweet_mode='extended')
    for mention in (mentions):
        print(str(mention.id) +' - '+ mention.full_text)
        ultimo_id = mention.id
        armazenar_Ultimo_Visto(ultimo_id,nome_Arq)
        if'brasil' in mention.full_text.lower():
            time.sleep(5)
            mensagem_com_informacoes = API_data_covid.consultaBrasil()
            quem_mensionou = '@' + mention.user.screen_name
            if len(quem_mensionou) <= 14:
                tweet_a_postar = quem_mensionou + " "+ mensagem_com_informacoes
            else:
                tweet_a_postar = mensagem_com_informacoes

            if tweet_duplicado(tweet_a_postar,quem_mensionou, mention.id):
                id_tweet_para_deletar = pegar_id_tweet(tweet_a_postar,quem_mensionou)
                deletar_tweet(id_tweet_para_deletar)
                api.update_status(tweet_a_postar)
            else:
                api.update_status(tweet_a_postar)
            if not api.create_favorite(mention.id):
                api.create_favorite(mention.id)
            break
        if 'global' or 'mundo' in mention.full_text.lower():
            time.sleep(5)
            mensagem_com_informacoes = API_data_covid.consultaMundo()
            quem_mensionou = '@' + mention.user.screen_name
            if len(quem_mensionou)<= 14:
                tweet_a_postar = quem_mensionou + " "+mensagem_com_informacoes
            else:
                tweet_a_postar = mensagem_com_informacoes
            if tweet_duplicado(tweet_a_postar,quem_mensionou,mention.id):
                id_tweet_para_deletar = pegar_id_tweet(tweet_a_postar, quem_mensionou)
                deletar_tweet(id_tweet_para_deletar)
                api.update_status(tweet_a_postar)
            else:
                api.update_status(tweet_a_postar)
            if not api.create_favorite(mention.id):
                api.create_favorite(mention.id)
            break
        else:
            break

def tweet_duplicado(mensagem = str, quem_mensionou = "", id_tweet = int):
    if quem_mensionou != "":
        todos_tweets = api.user_timeline(include_rts=True)
        for tweets in todos_tweets:
            if  mensagem[0:20] in tweets.text[0:20] and '@'+tweets.in_reply_to_screen_name == quem_mensionou or tweets.id == id_tweet:
                return True
    else:
        todos_tweets = api.user_timeline(include_rts=True)
        for tweets in todos_tweets:
            if mensagem in tweets.text and tweets.id == id_tweet:
                return True
    return False

def pegar_id_tweet(tweet_text = str, quem_mensionou = str):
    todos_tweets = api.user_timeline(include_rts = True)
    for tweets in todos_tweets:
        if tweets.text[0:20] == tweet_text[0:20] and '@'+tweets.in_reply_to_screen_name == quem_mensionou:
            return tweets.id
    return 666


def deletar_tweet(id_tweet = int):
    api.destroy_status(id_tweet)
    return
