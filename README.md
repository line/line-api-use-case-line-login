# Overview
[LINE API Use Caseサイト](https://lineapiusecase.com/ja/top.html)で提供している[LINEログイン](https://lineapiusecase.com/ja/api/login.html)のデモアプリケーションソースコードとなります。    
LINEログインは、ウェブアプリや、ネイティブアプリ（iOS、Android）に、LINEアカウントを利用したソーシャルログインを導入する機能です。
LINEログインを導入すると、ユーザーは使い慣れたLINEを使用して、ウェブアプリやネイティブアプリ（以降、サービスと呼びます）にログインできます。
以下手順に従って、LINEログインのデモアプリケーションを構築してください。

なお、このページで紹介しているソースコードの環境はAWSを利用しています。  

※ [The English version document is here.](./docs/en/README_en.md)

# Libraries
## Node.js
フロントエンド側の開発で使用する Node.js をローカル開発環境にインストールしてください。  
※ v10.13 以上 最新の LTS バージョンのインストールをおすすめします

【Node.jsダウンロードサイト】  
https://nodejs.org/ja/download/

## Python
Pythonのバージョン3.8以上がインストール済みでない場合、インストールしてください。  
コマンドプロンプト、又はターミナルにて以下のコマンドを入力し、インストール済みか確認できます。
```
python --version

Python 3.8.3 ← このように表示されたら、インストール済みです。
```

インストール済みでない場合、バックエンド側の開発で使用するPython（3.8以上）をローカル開発環境にインストールしてください。

【Pythonインストール参考サイト】  
Windows: https://www.python.jp/install/windows/install.html  
Mac: https://www.python.jp/install/macos/index.html

## AWS SAM
本アプリケーションのデプロイには、AWS サーバーレスアプリケーションモデル(AWS SAM)を利用します。
[AWS公式ドキュメント](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html
)を参考に、AWS アカウントの登録と設定、AWS SAM CLI と Docker のインストールを行ってください。  
※ SAM CLIの推奨バージョンは1.15.0以上  
※ Docker のインストールもローカルテストの有無に関わらず必要です。

### 公式ドキュメントの参考箇所
公式ドキュメントの以下の項目を完了させ、次の手順に進んでください。なお、既に導入済みのものは適宜飛ばして下さい。  
※本資料は 2020 年 12 月に作成しているため、最新の公式ドキュメントの内容と齟齬がある可能性があります。

1. AWS SAM CLI のインストール
1. AWS 認証情報の設定
1. （任意）チュートリアル: Hello World アプリケーションの導入

# Getting Started / Tutorial
こちらの手順では、アプリケーション開発に必要な「LINEチャネル作成、バックエンド・フロントエンドの構築、動作確認」について説明します。
以下リンク先の手順を参考にし、本番環境（AWS）とローカル環境の構築を行ってください。

### [LINE チャネルの作成](./docs/liff-channel-create.md)
### [バックエンドの構築](./docs/back-end-construction.md)
### [本番（AWS）フロントエンド環境構築](./docs/front-end-construction.md)
### [ローカルフロントエンド環境構築](./docs/front-end-development-environment.md)
***
### [動作確認](./docs/validation.md)
***
# License
LINELoginの全てのファイルは、条件なしで自由にご利用いただけます。
自由にdownload&cloneをして、LINE APIを活用した素敵なアプリケーションの開発を始めてください！

See [LICENSE](LICENSE) for more detail.(English)

# How to contribute

First of all, thank you so much for taking your time to contribute! LINE API Use Case Hair Salon is not very different from any other open source projects. It will be fantastic if you help us by doing any of the following:

- File an issue in [the issue tracker](https://github.com/line/line-api-use-case-line-login/issues) to report bugs and propose new features and improvements.
- Ask a question using [the issue tracker](https://github.com/line/line-api-use-case-line-login/issues).
- Contribute your work by sending [a pull request](https://github.com/line/line-api-use-case-line-login/pulls).

When you are sending a pull request, you'll be considered as being aware of and accepting the followings.
- Grant [the same license](LICENSE) to the contribution
- Represent the contribution is your own creation
- Not expected to provide support for your contribution
