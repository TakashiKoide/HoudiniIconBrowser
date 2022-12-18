# Houdini Icon Browser

Houdiniにデフォルトで入ってるアイコンを一覧化し、検索、名前の取得、編集、書き出しが出来るスクリプトです。

![HoudiniIconBrowser](https://user-images.githubusercontent.com/50489494/208280012-6bde2aa1-8e6d-42c7-83f9-a198c98a5129.png)

## インストール

**Code > Download ZIP**からZIPファイルをダウンロードしてください。

解凍したフォルダ内のscriptsフォルダとpython_panelsフォルダを環境変数HOUDINI_PATHが通ってる場所、もしくドキュメント内のHoudiniフォルダへコピーしてください。

## スクリプトの起動

Houdiniを起動し、パネルタブを右クリックするとパネル一覧にIcon Browserが登録されてるので、選んでください。

## 機能

### ダブルクリック

![IconBrowserCopyName](https://user-images.githubusercontent.com/50489494/208280386-4b2c8819-86e5-4a6e-a547-c044d34a2c2e.png)

アイコンの名前をクリップボードにコピーします。<br>
コピーされたアイコン名をHDAやシェルフツールのアイコン設定欄にペーストする事でそのアイコンを設定できます。

### 右クリックメニュー

![IconBrowserContextMenu](https://user-images.githubusercontent.com/50489494/208280156-e54a67a7-c492-4327-b403-792b7381b7d9.png)

- **Copy Name**<br>
    ダブルクリックした時と同じで、アイコンの名前をクリップボードにコピーします。
- **Open Icon File**<br>
    アイコンファイルをsvgファイルの編集に紐づいてるソフトで開きます。<br>
    ソフトの紐づけを行ってない方は事前に適当なsvgファイルを右クリック > プログラムから開く > 別のプログラムを選択 > 紐づけるソフトを選び、常にこのアプリを使って.svgファイルを開くにチェックを入れた状態で開いて設定するのをお勧めします。<br>
    編集ソフトはIllustratorやPhotoshopがお勧めです。
- **Save Icon File**<br>
    アイコンファイルを別の場所にコピーします。<br>
    実行すると保存先のフォルダを選ぶダイアログが開きます。

### フィルタリング

![IconBrowserFilter](https://user-images.githubusercontent.com/50489494/208280215-09973416-51bd-457e-bf08-96db5c05ce28.png)

プルダウンメニューでカテゴリごとにフィルタリング出来ます。
検索バーに文字を入力することで、アイコン名にその文字が含まれてるアイコンのみが表示されます。

### アイコンの大きさ調整

![IconBrowserIconSize](https://user-images.githubusercontent.com/50489494/208280288-9aed45fa-5bdf-424d-86f3-3276558e1236.png)

右下にあるスライダーとプラス、マイナスボタン、数値入力ボックスを変更する事でアイコンの大きさを変更できます。<br>
デフォルトは64pxで16px～64pxの範囲で変更できます。

### ビューモードの変更

<img src="https://user-images.githubusercontent.com/50489494/208280329-c41863f8-8c6c-4d3e-8e3d-913dc0cabbfa.png" width=49.5%> <img src="https://user-images.githubusercontent.com/50489494/208280334-9bbde091-b7c1-41c1-aadb-49496f75563d.png" width=49.5%>
右下にあるボタンでリストモードとアイコンモードの変更が出来ます。
