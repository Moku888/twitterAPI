import tweepy

# 編集必須
#===============================================================================
API_KEY = "自分で取得したものと書き替えてください"
API_SECRET = "自分で取得したものと書き替えてください"
ACCESS_TOKEN = "自分で取得したものと書き替えてください"
ACCESS_TOKEN_SECRET = "自分で取得したものと書き替えてください"
#===============================================================================

# お好みで編集
#===============================================================================
# 検索ワード
SEARCH_WORD = "to:H_KAGAMI2434 OR to:Hakase_Fuyuki OR to:HiguchiKaede OR to:Kanae_2434 OR to:Kanda_Shoichi OR to:Levi_E_2434"

# 取得ツイート数
GET_TWEET_MAX = 10000

# 1ツイートに対して何リプライ取得するか
GET_REPLY_COUNT = 3

# inputファイル
INPUT_FILE = "/input.txt"

# outputファイル
OUTPUT_FILE = "/output.txt"

# ログ出力先
LOG_FILE = "/log.log"

# 削除する文字列(見えない文字はメモ帳とかに張り付ければわかる)
banWord = ["︎","️","","",""]
#===============================================================================

# 編集不可
#===============================================================================
# 戻り値の型
STATUS = tweepy.models.Status
SEARCH_RESULTS = tweepy.models.SearchResults

# ファイルエンコード
fileEncod = "UTF-8"
#===============================================================================