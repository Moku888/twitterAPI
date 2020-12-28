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

    wakati = MeCab.Tagger("-Owakati")

    # 改行削除
    word = re.sub("\n","",word)
    word = re.sub("\r\n","",word)
    # タブ削除
    word = re.sub("\t","",word)

    # httpsから始まる文字を削除
    word = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", word)

    # リプライ文字列(@Lize等)を削除
    word = re.sub("@.* ","",word)

    # 英数字を半角に統一
    word = neologdn.normalize(word)

    # 絵文字削除
    word = ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in word])
    # 文字化け絵文字削除（空白に見えるけど化けたのがある）
    word = re.sub("️","",word)

    # かっこ書き削除（顔文字も消える）必要な情報も消えそうだけど妥協
    word = re.sub("\(.*\)","",word) #半角
    word = re.sub("（.*）","",word)   #全角
    word = re.sub("【.*】","",word)

    # 小数点削除
    word = re.sub(r'(\d)([,.])(\d+)', r'\1\3', word)
    # 数字をすべて0にする(機械学習には不要のため)
    word = re.sub(r'\d+', '0', word)

    # 半角記号の置換
    word = re.sub(r'[!-/:-@[-`{-~]', r' ', word)

    # 全角記号の置換 (ここでは0x25A0 - 0x266Fのブロックのみを除去)
    word = re.sub(u'[■-♯]', ' ', word)

    # Constに定義した文字削除
    word = ''.join(['' if c in Const.banWord else c for c in word])

    # 先頭、末尾の空白を削除
    word = word.strip()

    # 形態素区切り
    wakatiList = wakati.parse(word).split()
    word =" ".join(wakatiList)

    return word


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
