from typing import Self, Any, Optional
import io

class HtmlNode:
    def __init__(self, 
                tag: Optional[str] = None,
                value: Optional[str] = None,
                children: Optional[list[Self]] = None,
                props: Optional[dict[str, str]] = None
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


class LeafNode(HtmlNode):
    def __init__(self, tag: Optional[str], value: str, props: Optional[dict[str, str]]=None):
        super().__init__(tag, value, None, props)


    def to_html(self) -> str:
        if self.value is None:
            raise ValueError('value is None')
        
#        if self.value.strip() == '':
#            raise ValueError('value is empty')

        # raw text
        if self.tag == None:
            return self.value

        #img
        if self.tag == 'img':
            return f'<img{self.props_to_html()}>'
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HtmlNode):
    def __init__(self, tag: str, children: list[HtmlNode], props: Optional[dict[str,str]]=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError('missing tag!')
        
        if self.children is None:
            raise ValueError('missing children!')
        
        builder = io.StringIO()
        builder.write(f'<{self.tag}{self.props_to_html()}>')

        for child in self.children:
            builder.write(child.to_html())

        builder.write(f'</{self.tag}>')
        return builder.getvalue()