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
SEARCH_WORD_1 = "lang:ja (to:ratna_petit OR to:rei_Toya_rei OR to:saku_sasaki OR to:sibuya_hajime OR to:sukosuko_sukoya OR to:yuika_siina)"

# 複数回検索したい時のためにリストで保持（別のワードでも検索したい場合はこのリストに追加）
SEACH_WORD_LIST =[SEARCH_WORD_1]

# 追加する場合こんな感じ
# SEACH_WORD_LIST =[SEARCH_WORD_1,"魔王城でおやすみ","幼女戦記"]

# 取得ツイート数
GET_TWEET_MAX = 10000

# 1ツイートに対して何リプライ取得するか
GET_REPLY_COUNT = 3

# inputファイル
INPUT_FILE = "./input.txt"

# outputファイル
OUTPUT_FILE = "./output.txt"

# ログ出力先
LOG_FILE = "./log.log"

# 残しておきたい記号
SAVE_WORD_LIST = ["?","!","!?","?!"]

# 削除する文字列
BAN_WORD = []
#===============================================================================

# 編集不可
#===============================================================================
# 戻り値の型
STATUS = tweepy.models.Status
SEARCH_RESULTS = tweepy.models.SearchResults

# ファイルエンコード
fileEncod = "UTF-8"

# 結合文字列
JOIN_STR = " "
#===============================================================================

