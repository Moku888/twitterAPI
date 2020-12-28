from GetTweetUtil import GetTweet
import CommonUtil as Util
import GetTweetUtil as tUtil
import logging, Const

def main():
    # ログ初期化
    lg = Util.setLoggerCon()
    lg.info("<開始>")

    # twitterAPI初期化
    getTweet = GetTweet()

    # ファイル削除
    #Util.delFile()

    logMessage = ""
    lineCount = 0
    whileCount = 0

    # Const.GET_TWEET_MAX 件数取得できるまでループ
    while True:
        if lineCount >= Const.GET_TWEET_MAX:
            break
        whileCount += 1
        logMessage = str(whileCount) + "回目"

        # 100ツイート取得する
        result = getTweet.searchWord(Const.SEARCH_WORD)
        lg.debug("取得ツイート数："+str(len(result)))

        # 取得件数が1件(これ以上取得できない)場合
        if len(result) == 1:
            lg.info("これ以上ツイートがありません。処理を終了します。")
            break


        # リプライだけをリストに詰める
        repTweetList = tUtil.getRepOnly(result, Const.GET_REPLY_COUNT)
        lg.debug("リプライツイート数："+str(len(repTweetList)))


        # リプライ元のIDリスト作成
        idList = [data.in_reply_to_status_id_str for data in repTweetList]

        # リプライがなければ次のループ
        if len(idList) <= 0:
            logMessage += " ファイル出力なし"
            lg.info(logMessage)
            continue

        # リプライ元のツイートを取得
        tweetList = getTweet.searchStatusId(idList)

        # リプと元ツイートのペアを作成
        pairList = tUtil.createPair(tweetList, repTweetList)

        # input,outputファイルに出力
        tUtil.fileWrite(pairList)
        logMessage += " ファイル出力完了"

        #ファイル行数取得
        lineCount = tUtil.countFileLine(Const.INPUT_FILE)
        logMessage += " ファイル行数：" + str(lineCount)

        lg.info(logMessage)

    lg.info("<終了>")



if __name__ == '__main__':
    main()
