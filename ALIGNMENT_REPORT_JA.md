# 添付2ZIPの比較と公開用適合方針

## 比較した現物
- 公開側の基準：`New-Supplementary-Materials-main (2).zip`（ファイル39件）。
- 投稿側の基準：`applsci-4605095frevised.zip`（ファイル102件、自己マニフェストを除く101件を照合して全件一致）。
- 各ZIP・主原稿のSHA-256は`FREVISED_ALIGNMENT.json`に記録。
- オンラインの現在のGitHub内容はこの環境から取得できず、添付ZIPを比較基準にした。更新前にFetch/Pullを実施すること。

## 確認できた相違

| 対象 | 添付リポジトリ側 | frevised側 / 更新方針 |
|---|---|---|
| 現行論文タイトル | Exact Logical-Channel Equivalence and Code-Space-Leakage-Aware Tomography of a Five-Qubit Encoded-Qubit Transfer Circuit | Ideal Fixed-Code Channel Equivalence and Single-Session Hardware Diagnostics of a Five-Qubit Coherent State-Transfer Circuit |
| 本文と監査の基準 | 15ページの旧ビルド記録 | 17ページの現行原稿を参照 |
| 補足表紙 | 26 October 2026 | 9 November 2026、現行タイトル |
| 補足表の説明 | 以前の2資源実験を置換との説明 | 1セッション・6分割ジョブであることを明示 |
| 主図表の参照 | チャネルFigure 5、方法Table 7 | 基準比較Figure 5、チャネルFigure 6、判定Table 7、方法Table 8 |
| ビルド警告 | Overfullなしと記録 | 現行監査は主原稿に4.98134 ptのOverfull 1件。消さない |
| ログの配置 | audit直下に旧ログ3件 | current_build_logsとprevious_build_logsを区別 |
| READMEリンク | 6種類の参照先ファイルが欠けていた（LICENSE_NOTICEへの重複参照を含め7リンク） | 今回存在する案内・検証ファイルへ更新 |

## 数値と原本の保全

実機ZIPは両方の入力で同一SHA-256：
`d9a3ec3a5ef620e13216f9e4719508ea5148e4633ec26868e1f83cd1c382baab`。
17個の`supplement/tables`、`audit/data_audit.json`、4個の監査CSV、監査Pythonとrequirementsも同一。
これらを再計算した別値へ交換していない。古い保存アーカイブ内部のタイトル・ソフト版・日時も履歴として保持。

今回の公開用フォルダは、投稿ZIPから40ファイルをバイト単位で一致したままコピー。
`audit/README.md`とルートの案内は公開リポジトリ向けに新規作成/編集した。
`SOURCE_FILES_SHA256.json`はその40件の元ファイルとの対応を記録し、昔の37件用マニフェストを偽って再利用しない。

## コピーしなかったもの

`manuscript/`、`responses/`、著者確認事項、許諾/請求情報は自動公開しない。
`audit/REVIEWER_REVISION_ACTIONS.json`、`audit/REVIEWER_REVISION_LOG_JA.md`、
`audit/original_template2.tex`、`audit/template2_review_changes.diff`、
`audit/template2_to_template3revised.diff`も、査読・原稿編集の履歴なので投稿用ZIPに残す。
これらは保存数値の検証には不要。公開側のREADMEでこの範囲を明示した。

## この更新が行っていないこと

新規実機測定、IBM認証付き照会、最適化全再実行、本文の編集・再コンパイル、
新規許諾取得、著者承認の代行、オンラインリポジトリ更新、Release発行はしていない。
現行`BUILD_VALIDATION.json`は著者提供の記録としてコピーし、この作業の新規ビルド証明と混同しない。
