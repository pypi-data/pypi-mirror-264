from setuptools import setup, find_packages

# README.mdを読み込む
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='funcs_for_pfs',  # パッケージ名: 他と衝突しないユニークな名前を選択
    version='0.1.0',  # パッケージのバージョン
    packages=find_packages(),  # このパッケージで定義されるすべてのパッケージを自動的に見つける
    install_requires=[
        'toolz',  # 必要な外部パッケージがあればここに列挙
    ],
    long_description=long_description,  # 長い説明としてREADMEの内容を設定
    long_description_content_type='text/markdown',  # マークダウン形式を指定
    # 最低限のメタデータ
    author='kcode',
    author_email='kscreamsun@gmail.com',
    description='This is a collection of handy functions for performing functional pipeline processing (Point-Free Style) in Python.',
    license='CC0',  # ライセンス
)
