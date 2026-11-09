# 既存GitHubリポジトリを frevised 原稿に合わせて更新する手順

対象：`hideok3460/New-Supplementary-Materials`。
比較元：添付 `New-Supplementary-Materials-main (2).zip`。
合わせる先：添付 `applsci-4605095frevised.zip`。
本手順・更新用ZIPはローカルで作成しました。GitHubへの変更・アップロードは未実施です。
公開サイトの現在の内容はこの環境から取得できなかったため、添付されたダウンロード版を比較基準にしています。

## 1. 今回合わせる論文タイトル

**Ideal Fixed-Code Channel Equivalence and Single-Session Hardware Diagnostics of a Five-Qubit Coherent State-Transfer Circuit**

`manuscript/template3revised.tex` と `manuscript/Manuscriptrevised2.pdf` が一致し、本文は17ページ、改訂日は2026年11月9日です。
以前の「Exact Logical-Channel Equivalence ... Encoded-Qubit Transfer Circuit」へ戻す作業ではありません。
本文ファイルはこの更新では書き換えません。

補足2文書は2ページ・11ページのままです。全17個の表行ファイル、保存済み数値、実機ZIPは変わりません。
主な変更はタイトル・日付、現行監査、17ページ版の参照位置、READMEと引用情報です。
現行の主論文ビルドに残る Overfull hbox 1件（4.98134 pt）はそのまま監査に明記します。

## 2. 新しいリポジトリを作らず、既存リポジトリを準備

GitHub Desktopを `hideok3460` で開き、Current repositoryを
`New-Supplementary-Materials`、Current branchを更新対象（通常は`main`）にします。
既にClone済みなら、Cloneし直したり別のリポジトリを作ったりしません。

まだPCにCloneしていない場合だけ、File → Clone repository → URLから
`https://github.com/hideok3460/New-Supplementary-Materials` を指定します。
保存先の例：

```text
C:\Users\hideok34\Documents\GitHub\New-Supplementary-Materials
```

**ブラウザのDownload ZIPで展開したフォルダには通常 `.git` がありません。**
それは閲覧用スナップショットで、Cloneされた作業フォルダとは別です。
GitHub Desktopの Repository → Show in Explorer で、今回使う実際のClone先を確認します。
解析を行った `Documents\Revision_fixed5` を今回の公開更新先と取り違えないでください。

まず未コミットの変更があるか確認します。心当たりのある変更を退避・コミットするなどして保全し、
Fetch originを押し、Pull originが出た場合は取り込みます。競合があれば先に解決します。
他の更新があるのに強制的に上書きしたり、Force pushしたりしません。
Cloneフォルダ全体のローカルバックアップも別フォルダへ保存してください。

共同編集や保護ブランチでは、更新用ブランチを作成し、Push後にPull Requestでmainへ反映します。
ブランチだけにPushした段階では、論文が指す通常のmainの画面は更新されません。

## 3. 差分ZIPを作業用フォルダへ展開

通常は小さい方の `New-Supplementary-Materials_frevised_update.zip` を使用します。
例として次へ展開します（Clone先の外）：

```text
C:\Users\hideok34\Downloads\frevised_repository_update\
  START_HERE_JA.md
  check_before_update.py
  update_plan.json
  MOVE_OLD_LOGS_AFTER_COPY.txt
  copy_to_repository\
    README.md
    CITATION.cff
    audit\
    supplement\
    ...
```

更新用ZIPには、変更・追加するファイルと、同じ内容で再配置する小容量の表・監査ファイルが入っています。
同一内容の再配置は、Windowsの自動改行変換があった場合も投稿原本と同じバイト列にそろえるためです。
数値や計算式は変更しません。約27.64 MiBの実機ZIPは含めず、既存リポジトリの同一ファイルを残して使います。
ファイル全体を確認・保存する場合は `New-Supplementary-Materials_frevised_ready.zip` に完成形があります。
**差分フォルダだけを新しい空のリポジトリとして使用しないでください。**

## 4. コピー前に読み取り専用チェック

既にお使いのJupyterLabのPythonコードセルで、次を1行で実行します。
保存場所が異なる場合だけ2つのパスを直してください。

```python
%run "C:/Users/hideok34/Downloads/frevised_repository_update/check_before_update.py" --repository "C:/Users/hideok34/Documents/GitHub/New-Supplementary-Materials"
```

`UPDATE_COMPATIBILITY_CHECK_PASSED` と出れば、今回の更新を適用できるファイル状態です。改行だけの違いは通知されますが、本文変更とは区別します。
このチェックは読み取りだけで、コピー・削除・Git操作・IBM接続・解析をしません。

`CONFLICT` や `MISSING` が出たら、コピーを始めず対象ファイルを確認します。
GitHub側に今回の添付ZIP以降の変更がある可能性があります。検査を無効化して上書きしません。
`.git`がないという警告が出たら、Download ZIPの展開先ではなくClone先か確認してください。
知らない追加ファイルは自動削除しません。公開前に中身を確認してください。

## 5. copy_to_repository の「中身」をClone先へコピー

`copy_to_repository` を開き、その中にあるファイル・フォルダをすべて、
GitHub Desktopの Repository → Show in Explorer で開いたClone先へコピーします。
同名の対象ファイルについては置き換え、フォルダは中身を統合します。
手順4で差分を確認したファイルだけを置き換えます。

正しい配置：

```text
New-Supplementary-Materials\README.md
New-Supplementary-Materials\audit\current_build_logs\build_template3revised.log
New-Supplementary-Materials\supplement\Supplementary_Run02_Tables.pdf
```

間違い：

```text
New-Supplementary-Materials\copy_to_repository\README.md
New-Supplementary-Materials\New-Supplementary-Materials\README.md
```

`.git`や、既存の`audit`/`supplement`フォルダ全体を削除してからコピーしないでください。
実機ZIPは既存のものを残し、展開・再圧縮しません。
`applsci-4605095frevised.zip`全体を公開フォルダへコピーする作業でもありません。
査読回答書・許諾書・投稿原稿そのもの・著者用チェックリストは今回の公開範囲から外しています。

## 6. 古いログの重複を3ファイルだけ取り除く

コピー後、以下の**新しい置き場所**に旧ログが保存されたことを先に確認します。

```text
audit\previous_build_logs\build_template.log
audit\previous_build_logs\build_Supplementary_Derivations.log
audit\previous_build_logs\build_Supplementary_Run02_Tables.log
```

その後、`audit`直下に残る次の3ファイルだけを、ローカルバックアップへ移すか削除します。

```text
audit\build_template.log
audit\build_Supplementary_Derivations.log
audit\build_Supplementary_Run02_Tables.log
```

旧ログは新しい`previous_build_logs`側とGitの過去履歴に残ります。
`current_build_logs`や実機ZIPは削除しません。
`BUILD_VALIDATION.json`は現行版へ置換し、旧版は
`previous_build_logs/BUILD_VALIDATION_previous_round.json`に保存されています。

## 7. 完成形を読み取り専用で検証

JupyterLabのPythonセルで、Clone先の検証プログラムを実行します。

```python
%run "C:/Users/hideok34/Documents/GitHub/New-Supplementary-Materials/verify_repository.py"
```

主な合格表示：

```text
FREVISED_SOURCE_FILES_VERIFIED: 40/40
CURRENT_TITLE_AND_LINKS_VERIFIED; supplied 17-page build warning retained
HARDWARE_MANIFEST_VERIFIED: 3373/3373; ZIP CRC passed
SAVED_COUNTS_VERIFIED: 1746 circuits; 7151616 shots; 6 stored job IDs
FREVISED_REPOSITORY_ALIGNMENT_VERIFIED_OFFLINE
```

必要なのはPython標準ライブラリだけです。新しいQiskit、Julia、CVXPY、APIキーは不要です。
これは整合性検査で、ソルバー再実行や実機取得、許諾判定ではありません。
エラーが出たらそのメッセージを確認し、チェック用ハッシュを手で書き換えて通しません。
Windowsでテキストの改行が勝手に変わるのを避けるため、`.gitattributes`を同梱しています。
文字エディターで保存し直した原本がハッシュ不一致になった場合は配布原本を再コピーします。

## 8. GitHub Desktopで変更を確認してCommit・Push

Changesで `README.md`、`CITATION.cff`、補足4ファイル、監査メタデータとログ、追加説明等を確認します。
GitHub Desktopは旧ログの処理を移動（rename）または削除＋追加として表示する場合があります。
`update_plan.json`と一致する範囲か確認してください。

次は変更されないはずです：

```text
supplement/ibm_phoenix_run02_reproducible.zip
supplement/tables/（17ファイル）
audit/data_audit.json
audit/recheck_saved_results.py
audit/*_state_values.csv
audit/calibration_qubits.csv
```

これらが意図せず変更として表示された場合は、進まずに確認します。
新しいAPIキー、.venv、.qiskit、私的なメール等は選択しません。

Summaryの例：

```text
Align supplementary materials with the 9 November 2026 frevised manuscript
```

Descriptionの例：

```text
Update title/date and 17-page build/locator records; retain earlier logs as history.
Preserve run02 hardware archive and numerical tables unchanged.
Restore missing repository guidance and read-only verification files.
```

`Commit to main`（更新用ブランチならそのブランチ）を押し、その後 `Push origin`を押します。
**CommitだけではGitHub側へ送信されません。** Force push、リポジトリ削除、新規作成は不要です。
保護ブランチの場合はPull Requestを作り、レビュー後にmainへマージします。

## 9. ブラウザで公開内容を確認

`https://github.com/hideok3460/New-Supplementary-Materials` を再読み込みします。
Current branchではなく、ブラウザで表示中のブランチも確認してください。

- READMEの論文タイトルが新しいものになったか。
- 補足2PDFの1ページ目が9 November 2026か。
- `audit/BUILD_VALIDATION.json`が17ページ版で、1件の警告が残っていると記録されているか。
- `current_build_logs`と`previous_build_logs`が区別されているか。
- READMEの検証プログラム・ライセンス確認案内へのリンクが開くか。
- `supplement/ibm_phoenix_run02_reproducible.zip`を引き続きダウンロードできるか。

旧GitHub Releaseの資産はmainをPushしただけでは更新されません。
公開資料として案内する前に、ログアウトした画面/プライベートブラウズでも確認してください。
このローカル作業が自動的に公開を完了したわけではありません。

## 10. 論文対応版の新しいReleaseを作る

既存の公開済み版を黙って差し替えず、新しい未使用タグを使用します。
例：`applsci-4605095-frevised-20261109`（既に存在する場合は別の未使用名）。
Releases → Draft a new release → Choose a tag → Create new tag → Targetに更新後のmainを指定。
タイトルと説明には `RELEASE_NOTES_frevised.md` の文案を使えます。
Publish releaseを押すまでは公開版ではありません。

同じ実機ZIPをReleaseにも直接添付するかは任意です。旧版とバイト一致のままにします。
新しいtag/commitと実際のアクセス日を、原稿・README・CITATIONへ必要に応じて記録します。
過去の日付や未取得DOIを新たに作らないでください。

## 原稿側に残る確認事項

frevised原稿のData Availabilityには依然として
“The companion repository associated with the preceding work ...” とあります。
今回の新しい補足資料リポジトリを指す説明としては、著者が整合を確認すべき箇所です。
別添の `Optional_Manuscript_Repository_Statements_frevised.tex` は公開確認後に使う文案です。
今回、原稿そのものや投稿日・アクセス日を自動変更していません。

主原稿のOverfull警告1件、図の再利用クレジット/許諾条件の確認は別の著者作業です。
今回は許諾書や査読者との通信を公開しません。Public化はライセンス付与と同じではありません。
同梱の`LICENSE_NOTICE.md`は許諾の代わりではありません。

## 公式操作資料

- 同期・Push: https://docs.github.com/en/desktop/making-changes-in-a-branch/pushing-changes-to-github-from-github-desktop
- Commitと差分確認: https://docs.github.com/en/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop
- Release: https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository
- ファイル追加/上限: https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository

画面名はGitHubの言語設定・バージョンにより多少異なる場合があります。
