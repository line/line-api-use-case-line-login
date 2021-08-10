# バックエンドの構築手順
## 周辺リソースのデプロイ

以下の周辺リソースをデプロイする必要があります。

1. 共通処理レイヤー(Layer)

### 1.共通処理レイヤー(Layer)

AWS Lambda では複数 Lambda 関数で共通化して利用したい処理をレイヤーとして記述することが出来ます。
本アプリではレイヤーを利用しているので、はじめに以下の手順で、レイヤーをデプロイしてください。

- template.yaml の修正  
  backend-> Layer フォルダ内の template.yaml を開き、EnvironmentMap の dev の以下のパラメータ項目を修正する。

  - `LayerName` 任意のレイヤー名

- 以下コマンドの実行

```
cd [backend -> Layerのフォルダ]
sam build --use-container
sam deploy --guided
※プロファイル情報(default)以外を使用する場合は指定必要 sam deploy --guided --profile xxx
    Stack Name : 任意のスタック名
    AWS Region : ap-northeast-1
    Parameter Environment: dev
    #Shows you resources changes to be deployed and require a 'Y' to initiate deploy Confirm changes before deploy [Y/n]: Y
    #SAM needs permission to be able to create roles to connect to the resources in your template Allow SAM CLI IAM role creation[Y/n]: Y
    Save arguments to samconfig.toml [Y/n]: Y

    SAM configuration file [samconfig.toml]: 入力せずEnter 
    SAM configuration environment [default]: 入力せずEnter
    
    Deploy this changeset? [y/N]: y
```

- レイヤーバージョンをメモ  
  デプロイ後、ターミナルの Outputs の項目に、レイヤー ARN とレイヤーバージョンが表示されるので、レイヤーバージョンをメモしておく。  
  レイヤーバージョンは末尾の数字。  
  ※バージョンはデプロイするたびに更新されるので、初めてのデプロイの場合バージョン 1 となっているのが正しいです。
  ![コマンドプロンプトのOutput部の画像](images/out-put-description.png)

- 【確認】AWS マネジメントコンソールで Lambda のコンソールを開き、左タブから「レイヤー」を選択し、今回デプロイしたレイヤーがあることを確認する。



## アプリのデプロイ(APP)

以下の手順で、アプリ本体をデプロイしてください。

- template.yaml の修正  
  backend -> APP フォルダ内の template.yaml を開き、EnvironmentMap の dev の以下のパラメータ項目を修正する。  
  ※S3のアクセスログが必要な場合、ACCESS LOG SETTING とコメントされている箇所のコメントを解除してください。

  - `LineChannelSecret` 【LINE チャネルの作成】で作成したMessaging API 用のチャネルのチャネルシークレット
  - `LineChannelAccessToken` 【LINE チャネルの作成】で作成したMessaging API 用のチャネルのチャネルアクセストークン
  - `LIFFChannelId` 【LINE チャネルの作成】で作成したLIFF 用のチャネルのチャネル ID
  - `LoginUsersInfoDBName` 任意のテーブル名（ログインしたユーザーの情報をを登録するテーブル）
  - `MessageOption` push 固定（※後のOSSバージョンでLINE MINIアプリのサービスメッセージを実装する予定です。）
  - `FrontS3BucketName` 任意のバケット名 ※フロント側モジュールを配置するための S3 バケット名になります。
  - `LayerVersion` 【1.共通処理レイヤー】の手順にてデプロイしたレイヤーのバージョン番号  
    例）LayerVersion: 1  
  - `LambdaMemorySize` Lambdaのメモリサイズ  
    例）LambdaMemorySize: 128 ※特に変更する必要がない場合、最小サイズの128を指定してください。
  - `TTL` True or False (DynamoDBテーブルに登録したユーザー情報を自動で削除するか否か)
  - `TTLDay` 任意の数値 （TTLがTrueのとき、予約情報を登録から何日後に削除するか指定。TTLがFalseのとき、0を入れてください。）
  - `LogS3Bucket` 任意のバケット名(アクセスログを保管するS3の名称)  
  ※アクセスログが必要な場合のみコメントを解除して記載してください。また、他UseCaseアプリを構築済みの方は、他UseCaseアプリのアクセスログバケット名と別名で指定してください。
  - `LogFilePrefix` 任意の名称（ログファイルの接頭辞）  
  ※アクセスログが必要な場合のみコメントを解除して記載してください。

- 以下コマンドの実行

```
cd [backend -> APP のフォルダ]
sam build --use-container
sam deploy --guided
※プロファイル情報(default)以外を使用する場合は指定必要 sam deploy --guided --profile xxx
    Stack Name : 任意のスタック名
    AWS Region : ap-northeast-1
    Parameter Environment: dev
    Parameter ChannelType [LIFF]: LIFF
    #Shows you resources changes to be deployed and require a 'Y' to initiate deploy Confirm changes before deploy [Y/n]: Y
    #SAM needs permission to be able to create roles to connect to the resources in your template Allow SAM CLI IAM role creation[Y/n]: Y
    ××××× may not have authorization defined, Is this okay? [y/N]: y (全てyと入力)  
    Save arguments to samconfig.toml [Y/n]: Y

    SAM configuration file [samconfig.toml]: 入力せずEnter 
    SAM configuration environment [default]: 入力せずEnter

    Deploy this changeset? [y/N]: y
```

- API Gateway URLとCloufFrontDomainNameのメモ  
デプロイ成功時にOutPutにて表示されるAPI Gateway endpoint URLとCloudFrontDomainNameのメモを取ってください。

## エラー対応
- デプロイ時、以下のようなエラーが出た場合、こちらの手順で解消してください。
  ```
  Export with name xxxxx is already exported by stack sam-app. Rollback requested by user.
  ```
  - backend -> Layer -> template.yamlを以下を参考に、修正後デプロイ
    ```
    Outputs:
      UseCaseLayerName:
        Description: "UseCaseLayerDev Layer Name"
        Value: !FindInMap [EnvironmentMap, !Ref Environment, LayerName]
        Export:
          Name: LineLoginLayerDev -> こちらを任意の名称に修正
    ```
  - backend -> batch -> template.yamlを、以下の記載を参考に修正する。複数あるので、すべて修正する。
    ```
    !ImportValue LineLoginLayerDev -> LineLoginLayerDev を先ほど入力した名称に修正
    ```
  - backend -> APP -> template.yamlを、以下の記載を参考に修正する。複数あるので、すべて修正する。
    ```
    !ImportValue LineLoginLayerDev -> LineLoginLayerDev を先ほど入力した名称に修正
    ```


※本番環境構築中の方はこちらのリンクで次の頁へ移動してください  
[次の頁へ（本番環境）](front-end-construction.md)

※ローカル環境構築中の方はこちらのリンクで次の頁へ移動してください  
[次の頁へ（ローカル環境）](front-end-development-environment.md)

[目次へ戻る](../README.md)