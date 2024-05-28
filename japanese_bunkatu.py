import MeCab

class BunsetsuWakachi:
    def __init__(self):
        self.m = MeCab.Tagger('')

    def bunsetsu_wakachi(self, text):
        m_result = self.m.parse(text).splitlines()
        m_result = m_result[:-1] # 最後の1行は不要な行なので除く
        break_pos = ['名詞','動詞','接頭詞','副詞','感動詞','形容詞','形容動詞','連体詞'] # 文節の切れ目を検出するための品詞リスト
        wakachi = [''] # 分かち書きのリスト
        after_prepos = False # 接頭詞の直後かどうかのフラグ
        after_sahen_noun = False # サ変接続名詞の直後かどうかのフラグ

        for v in m_result:
            if '\t' not in v:
                continue
            surface = v.split('\t')[0] # 表層系
            pos = v.split('\t')[1].split(',') # 品詞など
            pos_detail = ','.join(pos[1:4]) # 品詞細分類（各要素の内部がさらに'/'で区切られていることがあるので、','でjoinして、inで判定する)

            # この単語が文節の切れ目とならないかどうかの判定
            no_break = pos[0] not in break_pos
            no_break = no_break or '接尾' in pos_detail
            no_break = no_break or (pos[0] == '動詞' and 'サ変接続' in pos_detail)
            no_break = no_break or '非自立' in pos_detail # 非自立な名詞、動詞を文節の切れ目としたい場合はこの行をコメントアウトする
            no_break = no_break or after_prepos
            no_break = no_break or (after_sahen_noun and pos[0] == '動詞' and pos[4] == 'サ変・スル')

            if no_break == False:
                wakachi.append("")
            wakachi[-1] += surface
            after_prepos = pos[0] == '接頭詞'
            after_sahen_noun = 'サ変接続' in pos_detail

        if wakachi[0] == '':
            wakachi = wakachi[1:] # 最初が空文字のとき削除する

        return wakachi