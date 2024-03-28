from typing import List, Optional
from bs4 import BeautifulSoup


class Tag:
    """A Tree node class on Bs4 Soup"""
    __starting_point__min_contentful_sentence_length = 100
    __gap__min_contentful_sentence_length = 10
    __ending_point__min_contentful_sentence_length = 30
    __min_contentful_sentences = 3

    def __init__(self, soup: BeautifulSoup):
        self.__child: List[Tag] = []
        # text of self and all child
        all_text: Optional[str] = soup.get_text(strip=True)
        # text of self only
        self_text: Optional[str] = soup.find(text=True)
        self.__soup: BeautifulSoup = soup
        self.__self_text: Optional[str] = self_text.strip(" \n\t") if self_text is not None else None
        self.__no_space_self_text: Optional[str] = self.__self_text.replace(" ", "").replace("\n", "").replace("\t",
                                                                                                               "") if self.__self_text is not None else None
        self.__all_text: Optional[str] = all_text

    def add_child(self, tag):
        self.__child.append(tag)

    def get_is_sentence(self, min_contentful_sentence_length: int):
        """Determine is this tag a sentence tag, base on length"""
        return len(
            self.__no_space_self_text) > min_contentful_sentence_length if self.__no_space_self_text is not None else False

    def get_num_good_direct_child(self, min_contentful_sentence_length: int) -> int:
        """How many direct child is good, non-recursively"""
        cumulative = 0
        for c in self.__child:
            if c.get_is_sentence(min_contentful_sentence_length=min_contentful_sentence_length) or c.get_num_good_direct_child(min_contentful_sentence_length=min_contentful_sentence_length) > 0:
                cumulative += 1
        return cumulative

    def get_quality(self, min_contentful_sentence_length: int):
        """Determine the contentful quality of this tag"""
        # GOOD, BAD
        if self.get_is_sentence(min_contentful_sentence_length):
            return "GOOD"
        elif self.get_num_good_direct_child(min_contentful_sentence_length=min_contentful_sentence_length) >= self.__min_contentful_sentences:
            # although self is not good, but it has sufficient good child
            return "GOOD"
        return "BAD"

    def get_contentful_tag(self):
        """Get contentful tag recursively"""
        min_contentful_sentence_length = self.__starting_point__min_contentful_sentence_length
        max_attempts = 100
        attempts = 0
        while True:
            attempts += 1
            contentful_tag = self.__get_contentful_tag(min_contentful_sentence_length=min_contentful_sentence_length)
            if contentful_tag is not None:
                return contentful_tag
            else:
                min_contentful_sentence_length = min_contentful_sentence_length - self.__gap__min_contentful_sentence_length
                if min_contentful_sentence_length < self.__ending_point__min_contentful_sentence_length:
                    raise ValueError(
                        f"Failed to find contentful tag from this soup base on the given content length. No single HTML tag contains sentence length within {self.__ending_point__min_contentful_sentence_length}~{self.__starting_point__min_contentful_sentence_length} range")
            if attempts > max_attempts:
                raise ValueError("Maximum attempts reached. Failed to find contentful tag from this soup")

    def __get_contentful_tag(self, *, min_contentful_sentence_length: int, _depth: int = 0, ):
        num_good_child = self.get_num_good_direct_child(min_contentful_sentence_length=min_contentful_sentence_length)
        if num_good_child == 1:
            # you should return that good child
            candidates = [(c, c.get_num_good_direct_child(min_contentful_sentence_length=min_contentful_sentence_length)) for c in self.__child if c.get_is_sentence(
                min_contentful_sentence_length=min_contentful_sentence_length) or c.get_num_good_direct_child(min_contentful_sentence_length=min_contentful_sentence_length) > 0]
            assert len(candidates) >= 1, f"Found {len(candidates)} good child, looks like you have a bug"
            sorted(candidates, key=lambda x: x[1], reverse=True)
            # export_html(self.__soup, _depth, "Condition 1")
            return candidates[0][0].__get_contentful_tag(_depth=_depth + 1,
                                                         min_contentful_sentence_length=min_contentful_sentence_length)
        elif num_good_child == 0:
            # no good child
            if self.get_quality(min_contentful_sentence_length=min_contentful_sentence_length) == "GOOD":
                # export_html(self.__soup, _depth, "Condition 2")
                # text = self.get_contentful_tag_texts()
                # export_txt(text, _depth, "Condition 2 export")
                return self
            return None
        else:
            # multiple good child
            # text = self.get_contentful_tag_texts()
            # export_txt(text, _depth, f"Condition 3, with {num_good_child} good child")
            # export_html(self.__soup, _depth, f"Condition 3, with {num_good_child} good child")
            return self

    def get_contentful_tag_texts(self):
        return self.__all_text if self.__all_text is not None else ""
        # texts = [self.self_text] if self.self_text is not None else []
        # for c in self.child:
        #     good_child = c.get_num_good_direct_child()
        #     if good_child > 0:
        #         texts.append(c.all_text)
        #     elif c.self_text is not None: # todo, bug
        #         texts.append(c.self_text)
        # return "\n".join(texts)

    @classmethod
    def from_soup(cls, soup):
        # this tag
        t = Tag(soup)
        # child
        child_list = soup.find_all(recursive=False)
        for child in child_list:
            child_tag = cls.from_soup(child)
            t.add_child(child_tag)

        return t
