from dataclasses import dataclass
from typing import Optional
import re

from lr2irscraper.helper.fetch import fetch
from lr2irscraper.types import BmsMd5, Lr2Id
from lr2irscraper.helper.exceptions import ParseError


@dataclass()
class BmsInfo:
    lr2_id: Lr2Id
    title: str

    @classmethod
    def from_source(cls, source: str) -> "Optional[BmsInfo]":
        """ LR2IRのランキングページをスクレイピングし、譜面情報を返す。
        http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=ranking&bmsmd5={}

        :param source: ランキングページ (html)
        :return: 譜面情報
        """
        if "この曲は登録されていません。<br>" in source.splitlines():
            return None

        bmsid_match = re.search(r"<a href=\"search\.cgi\?mode=editlogList&bmsid=(\d+)\">", source)
        courseid_match = re.search(r"<a href =\"search\.cgi\?mode=downloadcourse&courseid=(\d+)\">", source)
        if bmsid_match:
            lr2_id = Lr2Id("bms", int(bmsid_match.group(1)))
        elif courseid_match:
            lr2_id = Lr2Id("course", int(courseid_match.group(1)))
        else:
            raise ParseError("failed to detect lr2 id")

        title_match = re.search(r"<h1>(.*?)</h1>", source)
        if title_match is None:
            ParseError("parse error: failed to detect title")

        return BmsInfo(lr2_id, title_match.group(1))

    @classmethod
    def from_bmsmd5(cls, bmsmd5: BmsMd5) -> "Optional[BmsInfo]":
        """ BmsMd5を指定し、LR2IR から譜面情報を取得する。

        :param bmsmd5: BmsMd5
        :return: 譜面情報
        """
        """
        ランキングページの上部に書いてある譜面の情報さえ取れればよいので (ランキングそのものを見たいわけではないので)、
        ページ数に大きな値を指定しておいて、ランキングそのものは1件も表示されないようにする。以下のような意図。
        [1] 通信量削減 (LR2IRへの負荷対策)
        [2] 飛んでくる html のバリエーションを減らして安定性を高める
            [2-1] ランキングが100件以下かどうかでページ構成が微妙に変わったりする (ページめくり周り)
            [2-2] ランキングを表示するとプレイヤ名に変な文字が入っていたりする可能性がある
        """
        very_large_number = 4294967295
        url = "http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=ranking&bmsmd5={}&page={}" \
            .format(bmsmd5.hash, very_large_number)
        source = fetch(url).decode("cp932")
        return cls.from_source(source)