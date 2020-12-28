
# tweeterAPI
import tweepy, Const
import CommonUtil as cu
import os

class GetTweet:
    def __init__(self):
        # 各種キーを格納
        api_key = Const.API_KEY
        api_secret = Const.API_SECRET
        access_token = Const.ACCESS_TOKEN
        access_token_secret = Const.ACCESS_TOKEN_SECRET

        # Twitterオブジェクトの生成
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.maxId = "0"


    # 検索ワードで検索する。APIの制限で一度に取得できるのは100ツイートまで。
    def searchWord(self, word):
        # 検索開始
        result = self.api.search(q=word, count=100, max_id=self.maxId)
        self.maxId = result[len(result)-1].id_str
        # リストで返却
        return list(result)

    # IDで検索する
    # statusId : idリスト
    def searchStatusId(self, statusId):
        # 検索開始
        result = self.api.statuses_lookup(id_=statusId)
        # リストで返却
        return list(result)


# リプライIDがあるデータのみ取得
# リプが多すぎると困るので元IDが同じものはnum数だけ取得
def getRepOnly(result, num):
    resList = []
    idList = []

    # ファイルからも出力
    idList = cu.getIdToFile(Const.INPUT_FILE)

    for data in result:
        # リプライ元ID
        replyId = data.in_reply_to_status_id_str

        if replyId is None: continue

        idList.append(replyId)

        # 元IDが同じものがいくつあるか取得
        idNum = countRepId(idList, replyId)

        # numが3なら3個まで入る
        if idNum <= num:
            resList.append(data)

    return resList


# リプライを元ツイートとリプのペアに整形してリストに格納(id :\t text)
# return リスト[{"text":text,"repText":repText}]
def createPair(tweetList, repTweetList):
    res = []
    # リプライ分ループ
    for repData in repTweetList:
        repId = repData.id_str
        repText = repData.text
        textId = ""
        text = ""
        # リプライ元IDと一致するツイートのテキストを抽出
        for data in tweetList:
            if repData.in_reply_to_status_id_str == data.id_str:
                textId = data.id_str
                text = data.text
                break

        if len(repText) > 0 and len(text) > 0:
            tweetPair = {"textId":data.id_str,"text":text,"repId":repId, "repText":repText}
            res.append(tweetPair)

    return res

# ファイル出力
# peirList：リスト[辞書｛text,repText｝]
def fileWrite(peirList):

    inputWords = ""
    outputWords = ""
    # 行頭文字
    leadWord = ""
    # w=上書き,a=追記
    fileMode = "w"

    # ファイルが存在する場合は追記モード
    if os.path.isfile(Const.INPUT_FILE):
        fileMode = "a"
        leadWord = "\n"

    for i,data in enumerate(peirList):
        # 整形
        inputWord = cu.cleanWord(data["text"])
        outputWord = cu.cleanWord(data["repText"])

        if len(inputWord) <= 0 or len(outputWord) <= 0:
            continue

        # 連結
        inputWords += leadWord +  data["textId"] + ":\t" + inputWord
        outputWords += leadWord + data["repId"] + ":\t" + outputWord

        # 2週目以降は必ず改行
        leadWord = "\n"

    # inputファイルに書き出し
    with open(Const.INPUT_FILE, encoding=Const.fileEncod, mode=fileMode) as inputF:
        inputF.write(inputWords)

    # outputファイルに書き出し
    with open(Const.OUTPUT_FILE, encoding=Const.fileEncod, mode=fileMode) as outputF:
        outputF.write(outputWords)

# modelList内に同じリプ元IDがいくつあるか検索
def countRepId(idList, repId):
    count = 0
    for data in idList:
        if data == repId:
            count += 1

    return count

# ファイル行数取得
def countFileLine(fileName):
    count = 0
    with open(fileName, encoding=Const.fileEncod, mode="r") as f:
        count = sum(1 for c in f)
    return count
