# QMK_te96_kt
狭ピッチ

te96（[e3w2q/te96-keyboard](https://github.com/e3w2q/te96-keyboard)）をオリジナル配列で組んだ分割キーボード用の、VIA/Remap対応ファームウェア一式。

- 基板構成: `rev1_inverted`（Pro Micro 向かい合わせ・左右分割、片側 6行×8列）
- ベース: e3w2q の QMK フォーク（`e3w2q` ブランチ, commit `228a26b`, 2021-12）
- VIA protocol 9 のため、Remap は旧版 **[Remap for QMK 0.18](https://qmk018.remap-keys.app/)** を使う

## 構成

| パス | 内容 |
|---|---|
| `keymaps/via/` | VIA対応キーマップ（VID `0x1209` / PID `0x4651`：Remap登録済みの te96 定義が使われる） |
| `keymaps/via_custom/` | 上記と同じで PID のみ `0x7E96` に変更。Remap に未登録扱いさせ、自作の定義JSONを読み込ませる用 |
| `keymaps/mapcheck/` | 配列調査用。どのキーも自分のマトリクス位置を `行,列 ` として入力する |
| `firmware/*.hex` | 上記のビルド済みファームウェア |
| `remap/te96_rev1_inverted_grid.json` | 格子状（6×8×左右）の仮定義。PID `0x4651` 用 |
| `scripts/build.sh` | フォークの取得からビルドまで |

## キーマップ（via / via_custom）

- 4レイヤー。レイヤー0は te96 標準 `default` キーマップの配置
- レイヤー1: `RESET`（書き込みモード）、`EEP_RST`（設定初期化）、RGB操作を配置。Remap で上書きすると次回書き込み時に GND–RST の短絡が必要になる
- VIA は保存領域の有効性をビルド日付で判定するため、別日にビルドした hex を書き込むと Remap での変更は初期化される

## 書き込み

1. [QMK Toolbox](https://github.com/qmk/qmk_toolbox/releases) で hex を開く（Auto-Flash）
2. 左側（USB接続側）だけをつなぎ、Pro Micro の GND と RST を短絡
3. キー入力処理はUSB接続側で行うので、キーマップだけの変更なら左側のみの書き込みで足りる

## ビルド

```
scripts/build.sh              # via / via_custom / mapcheck すべて
scripts/build.sh via_custom   # 個別
```

必要なもの: `avr-gcc`・`avr-libc`（macOS なら `brew install qmk/qmk/qmk` で入る）、python3、git、make。
古い QMK CLI の依存（milc 1.4 など）は `.venv/` に隔離して入れる。
