以下のQiitaの記事で扱っているバックエンドのリポジトリです。

[CI/CDパイプラインを構築してReact × DjangoRestFrameworkで作ったSPAをGKEクラスタにデプロイする](https://qiita.com/maeple5/items/0967a7c41115257a1564)

テンプレートにしてあるので、利用したい場合はcloneするのではなく「Use this template」>「Create a new repository」をクリックして新規リポジトリを作成してください。

以下のコマンドにより仮想環境とライブラリをインストールしてください。不要なライブラリがいくつかあると思いますが気にしないでください。

    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt

必要な作業として、「local.example.env」を「local.env」にリネームしてください。
このファイルはconfig.settings.localでdjango-environにより読み込まれます。

また、ローカルではデフォルトでsqlite3を使うようになっています。PostgreSQLを使いたい場合は適宜config.settings.localを変更してください。
