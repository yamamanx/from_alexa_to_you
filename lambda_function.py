# coding:utf-8
import logging
import os
import traceback
import random

log_level = os.environ.get('LOG_LEVEL', 'DEBUG')
logger = logging.getLogger()


# --------------- Log level set ----------------------
def logger_level(level):
    if level == 'CRITICAL':
        return 50
    elif level == 'ERROR':
        return 40
    elif level == 'WARNING':
        return 30
    elif level == 'INFO':
        return 20
    elif level == 'DEBUG':
        return 10
    else:
        return 0


logger.setLevel(logger_level(log_level))


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output[0:2000]
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text[0:2000]
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = u'アレクサから君へ'
    reprompt_text = u'アレクサから君へ'
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    session_attributes = {}
    card_title = "Session Ended"
    speech_output = u'アレクサから君へを終了します'
    reprompt_text = u'アレクサから君へを終了します'
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def good_words():
    words = [
        u'ええやないの。勝手しとったら。人間いきとる事自体、わがままなんやから。'
        u'せやけど勝手しとって割食う人間の顔色見るのは卑怯ちゃうか？',
        u'大盤ぶるまい。お前らまとめて幸せにしてやる。俺の人生バラ色だからよお',
        u'力をあわせるなんてケチケチしたこと言わねえ。俺がいれば十分だ。',
        u'理想唱えて何が悪い、夢唱えたっていいじゃねえか。現実が怖くて夢が見れるかあ',
        u'ちくしょ。こんな事ぐらいで済むと思うなよ。この先、もっと上等な女扱いしてやる。覚えとけ。',
        u'会社という組織の中で個人的感情で動くやつをガキと呼ぶなら俺はそのままガキです。'
        u'個人の感情など捨て、会社の利益だけ考えて動く人を一流と呼ぶなら、俺、そんな人知りません。あわせてください。',
        u'うるせえよ。外野はひっこんでろ。俺に便乗すんじゃねえ。言いたいことあんならてめえの口で言え。ヘラヘラ笑って味方面すんなあ。',
        u'したり顔してさとりすますのやめろ。じじいども。',
        u'男やったら惚れた女とおかん以外は全部カス扱いせえよ。',
        u'きれいごと言うなよ。お前を認めた人間はお前に焼かれようが食われようが文句言う筋合いどこにもねえよ。'
        u'お前のそういう情けない人間が、お前を認めた人間をどれだけバカにしてるのかわかってんのか。'
        u'のぼせあがんなよ。ばかやろう。少なくとも俺はいつだって俺のためにやってんだ。文句あるか。',
        u'生き死ににかかわるような悩みなんざそうそうねえよ',
        u'上に立つ人間が、部下の可能性の間口狭めてどないするんですか。取引停止の一つや二つどないにでも穴うめ出来ますやろ',
        u'清い正論通る世の中にしよと努力せんかった人間が、しょせん世の中変わらんて言うたらあかんですやろ。',
        u'サラリーマンの経験の範囲だけで事の正誤 測るのは間違っちゃいませんか。どこか違いますよ。',
        u'クソたれたいなら、自分で紙用意せえよ。一人前の口ききたいなら、一人前になったれよ。働いとるんやで。力もない、役にも立たへんでは、許されへんやろ。',
        u'自分に自身のないやつは、自分の事しか考えられないんだって。余裕ないんだから。'
        u'自分に力のないやつほど誰かに一緒だとか、協力してだとか言い出すんだってば。'
        u'ねえ、そんな事一人で戦えない奴がいっちゃいけないでしょ？違う？',
        u'何ひとつ解決策は思いつかなかった。ただ僕が気持ちのどこかで、諦める理由を探しているうちは、諦めのは卑怯だと思った。',
        u'人の寿命が無限なら、仕事がただの生活の手段でも、日銭を稼ぐ手段でも構いません。生きてる時間が有限だから、仕事に意味や目的が欲しいです。',
        u'正しいか間違いかじゃなく、いいか悪いかじゃなく、好きか嫌いかで物事を判断してきました。我のつよい人間が好きです。',
        u'ものわかりの良すぎる若い人間が嫌いです。ものわかりの悪い年寄りが嫌いです。クソ意地持った男が好きです。気持ちに素直な女が好きです。',
        u'俺がかっこいいと思っているものを、そうじゃないって言う人間に認めさせたいです。',
        u'のんきに宝くじ買ってる人間に夢なんか語る資格はねえだろ。動かない人間がたれるのは能書きとたわごとって言うんだよ。',
        u'いまさらお前の男友達にはなれそうにないしな。父さんはお前の父親だそれでいい。',
        u'お前、前に言う撮ったやろ。「人間だから完全になれる」って。そら無理や。人間生きとる自体、わがまま通してるんやから。',
        u'心のうわっつらでしか悩めない自分の腹がたった',
        u'自分ひとりじゃ未練すら断ち切れなかった。身の程を知った。',
        u'だったら少しは動かんかい',
        u'ま 人におべんちゃら使えんちゅーんは、おのれに自身がないんやろな',
        u'敵や思うたらええやんか。 男一匹千人でも万人でも敵にまわしたれや。 お前そういう奴とちゃうんか？',
        u'てめえがいい顔すりゃ誰でも尻尾ふるとでも思ってんのか！ おらもう一息だ。 にくけりゃにくいとはっきり言えよ。 中途半端にしてんじゃねえ！',
        u'人は感動するために生きてっからよ。 ちまちま生きたって、のらりくらりやったって、事の大小に関係なく、'
        u'生まれてきてよかった、生きててよかったなんて思える瞬間が一生のうち、一度や二度くらいあるはずだ。 '
        u'けどなそいつを味わうにせよ、持ち続けるにせよ、信じる力がいるからよ。 我々は日々精進しなきゃなんねえのよ。なあ。',
        u'どうぞ。 俺の命。 使ってください。 俺 大丈夫ですから。だから絶対妻と子供だけは助けてやってください。お願いします。'
    ]
    return words


def get_random_good(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech = random.choice(good_words())

    speech_output = speech
    reprompt_text = speech

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def default_speech(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech = u'宮本から君へ、は、新井英樹による日本の漫画作品です'

    speech_output = speech
    reprompt_text = speech

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    logger.info("on_session_started requestId=" + session_started_request['requestId'] +
                ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    logger.info("on_launch requestId=" + launch_request['requestId'] +
                ", sessionId=" + session['sessionId'])
    return get_welcome_response()


def on_intent(intent_request, session):
    logger.info("on_intent requestId=" + intent_request['requestId'] +
                ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "SomethingGood":
        return get_random_good(intent, session)
    elif intent_name == "Default":
        return default_speech(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    logger.info("on_session_ended requestId=" + session_ended_request['requestId'] +
                ", sessionId=" + session['sessionId'])
    return handle_session_end_request()


# --------------- Main handler ------------------

def lambda_handler(event, context):
    try:
        logger.debug(event)
        logger.info("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

        if event['session']['new']:
            on_session_started({'requestId': event['request']['requestId']},
                               event['session'])

        if event['request']['type'] == "LaunchRequest":
            return on_launch(event['request'], event['session'])
        elif event['request']['type'] == "IntentRequest":
            return on_intent(event['request'], event['session'])
        elif event['request']['type'] == "SessionEndedRequest":
            return on_session_ended(event['request'], event['session'])

    except:
        logger.error(traceback.format_exc())
        raise Exception(traceback.format_exc())
