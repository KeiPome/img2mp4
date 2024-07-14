import streamlit as st
from img2mp4 import Img2MP4  # Img2MP4クラスを別ファイルからインポート

# Streamlitアプリのタイトル
st.title('画像からMP4への変換ツール')

# ユーザー入力
img_folder = st.text_input('画像フォルダのパスを入力してください:', '/path/to/your/image/folder')
output_folder = st.text_input('出力フォルダのパスを入力してください:', '/path/to/your/output/folder')
fps = st.number_input('フレームレート(FPS):', min_value=1, max_value=60, value=30)
batch_size = st.number_input('バッチサイズ:', min_value=1, value=100)
concatenate = st.checkbox('バッチ動画を結合しますか?', value=True)

# 変換ボタン
if st.button('画像をMP4に変換'):
    # Img2MP4クラスのインスタンスを作成
    img2mp4 = Img2MP4(img_folder, output_folder, fps, batch_size, concatenate)
    # 変換処理を実行
    img2mp4.run()
    st.success('変換が完了しました！')