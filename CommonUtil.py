import os
import Const
import re
import neologdn # 正規化
import emoji    # 絵文字削除
import MeCab
import logging

# twitterAPIの戻り値を表示する
def printResult(result):
    print("<表示開始>")
    # リストの場合は全て表示
    if type(result) in (Const.SEARCH_RESULTS, list):
        for data in result:
            print("="*20)
            print("ユーザーID："+data.user._json['screen_name'])
            print("ツイートID："+str(data.id))
            print("ユーザー名："+data.user.name)
            print("ユーザーのコメント："+data.text)
            print("リプライ元："+str(data.in_reply_to_status_id_str))
            print("="*20)

    elif type(result) is Const.STATUS:
        print("="*20)
        print("ユーザーID："+result.user._json['screen_name'])
        print("ツイートID："+str(result.id))
        print("ユーザー名："+result.user.name)
        print("ユーザーのコメント："+result.text)
        print("リプライ元："+str(result.in_reply_to_status_id_str))
        print("="*20)

    print("<表示終了>")

# twitterAPIの戻り値を表示する(IDのみ)
def printResultId(result):
    print("<表示開始>")
    # リストの場合は全て表示
    if type(result) in (Const.SEARCH_RESULTS, list):
        for data in result:
            print("ツイートID："+str(data.id))
    elif type(result) is Const.STATUS:
        print("ツイートID："+str(result.id))
    print("<表示終了>")

# input,outputファイル削除
def delFile():
    try:
        os.remove(Const.INPUT_FILE)
        print("inputファイル削除")
        os.remove(Const.OUTPUT_FILE)
        print("outputファイル削除")
    except OSError as e:
        print("削除対象ファイルなし")

# ファイルからIDを取得
def getIdToFile(fileName):
    fileIdList = []
    # ファイルが存在する場合はファイルからも出力
    if os.path.isfile(fileName):
        with open(fileName, encoding=Const.fileEncod) as fd:
            for i, line in enumerate( fd.readlines() ):
                lineList = line.split(':\t', 2)
                fileIdList.append(lineList[0])

    return fileIdList


# データ整形
def cleanWord(word):
    # 改行削除
    word = re.sub("\n","",word)
    word = re.sub("\r\n","",word)
    # タブ削除
    word = re.sub("\t","",word)

    # httpsから始まる文字を削除
    word = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", word)

    # リプライ文字列(@Lize等)を削除
    word = re.sub("@.* ","",word)

    # 手間だけど一つずつ処理
    #===============================
    # 英数字を半角に統一
    word = neologdn.normalize(word)
    # 記号を半角に変換
    word = re.sub("？","?",word)
    word = re.sub("！","!",word)
    # "～"を"ー"に統一
    word = re.sub("～","ー",word)
    # "ー"が2回以上連続で出る場合、1つにする
    word = re.sub("ー{2,}","ー",word)
    # "っ"が2回以上連続で出る場合、1つにする
    word = re.sub("っ{2,}","っ",word)
    # "!"が2回以上連続で出る場合、1つにする
    word = re.sub("!{2,}","!",word)
    # "?"が2回以上連続で出る場合、1つにする
    word = re.sub("\?{2,}","?",word)
    #===============================

    # かっこ書き削除（顔文字も消える）必要な情報も消えそうだけど妥協
    word = re.sub("\(.*\)","",word) #半角
    word = re.sub("（.*）","",word)   #全角
    word = re.sub("【.*】","",word)

    # 小数点削除
    word = re.sub(r'(\d)([,.])(\d+)', r'\1\3', word)
    # 数字をすべて0にする(機械学習には不要のため)
    word = re.sub(r'\d+', '0', word)

    # 絵文字削除
    word = ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in word])

    # Constに定義した文字削除
    word = ''.join(['' if c in Const.BAN_WORD else c for c in word])

    # 先頭、末尾の空白を削除
    word = word.strip()

    # おかしな日本語削除 AND 形態素区切り
    word = mecabFunc(word)

    return word

# mecabを使っておかしな日本語を削除し、空白区切りにして返す
def mecabFunc(word):
    # 整形済み文字列をいれる変数
    afterWord = ""

    wakati = MeCab.Tagger()
    # 形態素解析したデータ
    node=wakati.parseToNode(word)

    while node :
        # 正しい単語フラグ
        japFlg = True
        # 元単語
        origin = str(node.surface)

        # 残しておきたい記号の場合
        if origin in Const.SAVE_WORD_LIST:
            #スペース区切りで結合
            afterWord = wordJoin(afterWord,origin,Const.JOIN_STR)
            node=node.next
            continue

        # リスト型にキャスト
        # [0:品詞,1:品詞細分類1,2:品詞細分類2,3:品詞細分類3,4:活用型,5:活用形,6:原形,7:読み,8:発音]
        nodeList = node.feature.split(",")

        # [細分類1:数]はリストが6までしかないので先に処理
        if japFlg and nodeList[1] == "数":
            #スペース区切りで結合
            afterWord = wordJoin(afterWord,origin,Const.JOIN_STR)
            node=node.next
            continue

        # BOS/EOS は削除
        if japFlg and nodeList[0] == "BOS/EOS":
            japFlg = False

        # 数字以外で何故か6までしかない単語の削除(絵文字とか)
        if japFlg and len(nodeList) < 9:
            japFlg = False

        # 品詞=記号の場合削除
        if japFlg and nodeList[0] == "記号":
            japFlg = False

        # 名詞　且つ　読みがない場合削除
        if japFlg and nodeList[0] == "名詞" and nodeList[7] == "*":
            japFlg = False

        if japFlg:
            #スペース区切りで結合
            afterWord = wordJoin(afterWord,origin,Const.JOIN_STR)

        node=node.next
    return afterWord

# 文字列をjoinWordで結合
def wordJoin(fromWord, toWord, joinWord):
    reWord = ""
    if not fromWord:
        reWord = toWord
    else:
        reWord = fromWord + joinWord + toWord
    return reWord

# ログ設定
def setLoggerCon():
    # ロガー作成
    lg = logging.getLogger("getTweetCon")
    lg.setLevel(logging.DEBUG)

    # ストリームハンドラ 追加
    sh1 = logging.StreamHandler()
    sh1.setLevel(logging.INFO)
    sh1.setFormatter(logging.Formatter('[%(asctime)s:%(levelname)s]:%(message)s'))
    lg.addHandler(sh1)
    del sh1

    # ファイルハンドラ 追加
    sh2 = logging.FileHandler(filename=Const.LOG_FILE)
    sh2.setLevel(logging.DEBUG)
    sh2.setFormatter(logging.Formatter('[%(asctime)s:%(levelname)s]:%(message)s'))
    lg.addHandler(sh2)
    del sh2

    return lg
