# labomen-bot

discord.py を使った BOT アプリです。
じゃんけんをしたり、おみくじを引いたりすることができます。

## 機能

1. Discord から自動的にメッセージを吸い上げる
2. 特定語句を判定し、条件に一致した場合に処理を行う

### 現在実装済みの機能

- じゃんけん機能
- おみくじ機能
- 特定ワード反応機能

`./texts/`のテキストファイルをいじることで自由にメッセージを設定可能です。

## 動作条件

- Python 3.7 以上
- もしくは Docker 環境

## 関連リポジトリ

- [discord.py](https://github.com/Rapptz/discord.py)

## 推奨開発環境

- [Docker](https://www.docker.com/)
- [VSCode](https://azure.microsoft.com/ja-jp/products/visual-studio-code/)
- [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## 使い方

`discord-test.py`と同じ階層に下記のような環境変数設定用ファイル`.env`を作ってください。`DISCORD_ACCESS_TOKEN=`の後に DiscordAPP 用のアクセストークン、`DISCORD_CHANNEL_IDS=`の後にターゲットとなるチャンネル ID を`,(カンマ)`で区切って入力してください。

```env
DISCORD_ACCESS_TOKEN=
DISCORD_CHANNEL_IDS=
```

### Docker 環境で動かす場合

```shell
$ sudo docker-compose up -d
```

### 通常の Python3 環境で動かす場合

```shell
$ pip3 install -r requirements.txt
$ python3 -m labomen_bot
```

## 備考

基本的に`Ubuntu 20.04`環境でテストしています

## License

MIT License
