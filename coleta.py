from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import csv


class TwitterListener(StreamListener):

    def __init__(self):
        self.cont_tweet = 0
        self.max_tweet = 100



    def on_data(self, raw_data):
        try:
            tuite = json.loads(raw_data)
            lang = tuite.get('lang')
            if lang == "pt":
                self.cont_tweet = self.cont_tweet + 1
                criado = tuite.get('created_at')
                texto = tuite.get('text')

                print('Publicado em: {}\n Texto: {}\n'.format(criado, texto))

                with open('tuites.json', mode='a', encoding='utf-8')as meu_arquivo_json:
                    nTuite = [criado, texto]
                    json.dump(nTuite, meu_arquivo_json, indent=4)

                meu_arquivo_csv = open('tuites.csv', mode='a', encoding='utf-8')
                writer = csv.writer(meu_arquivo_csv)
                writer.writerow([criado, texto])
                meu_arquivo_csv.close()
            else:
                print('Procurando...\n')

        except BaseException as erro:
            print("Execão: {}".format(erro))

        if self.cont_tweet >= self.max_tweet:
            return False

    def on_error(self, status_code):
        print("Execão: {}".format(status_code))


def coleta():
    token = "1024536366040985601-EEt1z1385tAenpT9YpkQDtRNrnaeft"
    token_secret = "FOhdGNyyCWFMby3i7ocStbDkpIvolLdAdmIeBoJ6FfAkq"
    consumer = "EymuKUxT94W7aFq87WnM4N48R"
    consumer_secret = "mYuz8YoQxd0L1AuH80H2piNpkiXEbZkGIv2kvK5EnYDZJWJcrY"

    tw = TwitterListener()
    oauth = OAuthHandler(consumer, consumer_secret)
    oauth.set_access_token(token, token_secret)

    stream = Stream(oauth, tw)
    stream.filter(track=['bolsonaro', 'lula', 'eleicoes2018'])


coleta()
