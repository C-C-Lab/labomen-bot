# labomen-bot

discord.py を使った BOT アプリです。

<br/>

## 機能

1. discord.py を使用し、DiscordBOT から自動的にメッセージを吸い上げる
2. 特定語句を判定し、条件に一致した場合に処理を行う

<br/>

## 動作条件

- Python 3.7 以上

<br/>

## 関連公式ドキュメント

- [discord.py](https://discordpy.readthedocs.io/ja/latest/index.html)

<br/>

## 参考文献

- [Python で実用 Discord Bot(discordpy 解説)](https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f)
- [discord.py 入門](https://qiita.com/sizumita/items/9d44ae7d1ce007391699)
- [python3 の venv でプロジェクト毎にライブラリを管理する](https://akogare-se.hatenablog.com/entry/2019/01/02/220330)

<br/>

## 使い方

`discord-test.py`と同じ階層に下記のような環境変数設定用ファイル`.env`を作ってください。`DISCORD_ACCESS_TOKEN=`の後に DiscordAPP 用のアクセストークン、`DISCORD_CHANNEL_IDS=`の後にターゲットとなるチャンネル ID を`,(カンマ)`で区切って入力してください。

```env
DISCORD_ACCESS_TOKEN=
DISCORD_CHANNEL_IDS=
```

<br/>

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

Linux 環境でテスト済みです。
このリポジトリは、まだ開発段階のリポジトリです。

## License

MIT License
