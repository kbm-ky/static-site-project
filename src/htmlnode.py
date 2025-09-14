from typing import Self, Any, Optional

class HtmlNode:
    def __init__(self, 
                tag: Optional[str] = None,
                value: Optional[str] = None,
                children: Optional[list[Self]] = None,
                props: Optional[dict[str, Any]] = None
                ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None:
            return ''

        s = ''
        for k,v in self.props.items():
            s += f' {k}="{v}"'
        return s

    def __repr__(self) -> str:
        return f'HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'