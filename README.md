# FabricによるDebian Jessieの設定

* ~/.ssh/id_rsa.pub を SSH公開鍵としてユーザに設定
* ユーザをパスワードなしでrootにできるようにsudoコマンドを設定する
* sshdの設定を変更、公開鍵のみでログインできるようにする
* localeをLANG=Cにする
* dnssd, vim のセットアップ

コマンド

	fab -H [IPアドレス] -u [ユーザ] setup
	
最初のパスワードではユーザのパスワード、次のパスワードではrootのパスワードを入れる

# 資料

* [Welcome to Fabric’s documentation!(日本語)](http://fabric-ja.readthedocs.io/ja/latest/)
