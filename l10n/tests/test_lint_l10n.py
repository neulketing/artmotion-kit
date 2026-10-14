"""python3 -m unittest discover -s l10n/tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import lint  # noqa: E402

KO = """화풍: 고흐 풍 두꺼운 붓결
팔레트: paper
캐릭터: 손과 뒷모습만

| 시간 | 사물 | 동작 | 카메라 | 화면 글자 | 방법 |
|---|---|---|---|---|---|
| 0–3 | 밀밭 위 사이프러스 | 바람에 휘어진다 | 정지 | | scenes/09_postimp.js |
| 3–6 | 소용돌이 하늘 | 별빛이 빙글빙글 돈다 | 천천히 밀기 | 별이 빛나는 밤 | scenes/09_postimp.js |
| 6–9 | 사이프러스 | 붓결이 흔들린다 | 빼기 | | scenes/09_postimp.js |
"""
EN = KO.replace('화풍', 'Style').replace('팔레트', 'Palette').replace('캐릭터: 손과 뒷모습만', 'Character: hands and back view only') \
    .replace('| 시간 | 사물 | 동작 | 카메라 | 화면 글자 | 방법 |', '| Time | Object | Action | Camera | On-screen text | Method |') \
    .replace('정지', 'hold').replace('천천히 밀기', 'slow push').replace('빼기', 'pull out')


class LintL10n(unittest.TestCase):
    def verdict(self, text):
        return lint.SL.lint(lint.translate(text))

    def test_korean_and_english_tables_pass(self):
        for text in (KO, EN):
            res = self.verdict(text)
            self.assertNotIn('error', res)
            self.assertEqual(res['verdict'], lint.SL.GREEN, lint.SL.report(res))

    def test_korean_text_card_ending_is_red(self):
        bad = KO.replace('| 6–9 | 사이프러스 | 붓결이 흔들린다 | 빼기 | |',
                         '| 6–9 | 제목 | 나타난다 | 빼기 | 고흐가 그린 하늘은 왜 이렇게 소용돌이칠까요 정말 궁금하네요 |')
        res = self.verdict(bad)
        tags = {i[1] for r in res['rows'] for i in r['issues']}
        self.assertEqual(res['verdict'], lint.SL.RED)
        self.assertTrue({'①物', '②做什么', '③屏上字'} <= tags, tags)


if __name__ == '__main__':
    unittest.main()
