from typing import List, Tuple, Any, Optional
from langchain_core.documents import Document
import json
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, ValidationInfo, computed_field
from keble_helpers import PydanticModelConfig
from enum import Enum
from datetime import datetime
import pytz
class WxMessageType(str, Enum):
    TEXT = "TEXT"
    VOICE = "VOICE"
    VIDEO = "VIDEO"
    IMAGE = "IMAGE"
    EMOJI = "EMOJI"
    OTHER = "OTHER"


class WxMessage(BaseModel):
    model_config = PydanticModelConfig.default()

    compress_content: Optional[Any] = Field(None, alias="CompressContent")
    con_blob: Optional[str] = Field(None, alias="ConBlob")
    int_res1: Optional[int] = Field(None, alias="IntRes1")
    int_res2: Optional[int] = Field(None, alias="IntRes2")
    str_res1: Optional[str] = Field(None, alias="StrRes1")
    str_res2: Optional[str] = Field(None, alias="StrRes2")
    mes_des: Optional[int] = Field(None, alias="mesDes")
    mes_local_id: Optional[int] = Field(None, alias="mesLocalID")
    mes_svr_id: Optional[int] = Field(None, alias="mesSvrID")

    msg_content: Optional[str] = Field(None, alias="msgContent")
    msg_create_time: Optional[datetime] = Field(None, alias="msgCreateTime")
    msg_img_status: Optional[int] = Field(None, alias="msgImgStatus")
    msg_seq: Optional[int] = Field(None, alias="msgSeq")

    msg_source: Optional[str] = Field(None, alias="msgSource")
    msg_status: Optional[int] = Field(None, alias="msgStatus")
    msg_voice_text: Optional[str] = Field(None, alias="msgVoiceText")

    original_message_type: Optional[int] = Field(None, alias="messageType")

    @field_validator("msg_create_time", mode="before")
    def create_time_validate(cls, dt: int):
        return datetime.fromtimestamp(dt, tz=pytz.timezone("Asia/Shanghai"))

    @computed_field
    @property
    def message_type(self) -> WxMessageType:
        if self.original_message_type is None: return WxMessageType.OTHER
        original = str(self.original_message_type)
        if original == "1": return WxMessageType.TEXT
        if original == "3": return WxMessageType.IMAGE
        if original == "34": return WxMessageType.VOICE
        if original == "43": return WxMessageType.VIDEO
        if original == "47": return WxMessageType.EMOJI
        return WxMessageType.OTHER

    def get_message_content_placeholder(self):
        placeholders = {
            '1': '文字',
            '3': '图片',
            '43': '视频',
            '-1879048185': '微信运动排行榜',
            '5': 'unknown',
            '47': '表情包',
            '268445456': '撤回的消息',
            '34': '语音',
            '419430449': '转账',
            '50': '语音电话',
            '10000': '系统消息',  # 例如红包等，或者拒收
            '822083633': '回复消息',
            '922746929': '拍一拍',
            '1090519089': '发送文件',
            '318767153': '付款成功',
            '436207665': '发红包',
        }
        if self.original_message_type is not None and str(
                self.original_message_type) in placeholders: return f"[{placeholders[str(self.original_message_type)]}]"
        return f"[unknown]"

    def get_wxid_and_content(self) -> Tuple[Optional[str], Optional[str]]:
        if self.msg_content is None: return None, None
        wxid = self.msg_content.split("\n")[0]
        content = self.msg_content[len(wxid):]
        wxid = wxid.strip(": \n\t")
        content = content.strip("\n\t")
        if self.message_type.TEXT: return wxid, content
        if self.message_type.VOICE or self.message_type.VIDEO:
            if self.msg_voice_text is not None: return wxid, self.msg_voice_text
            return wxid, self.get_message_content_placeholder()
        return wxid, self.get_message_content_placeholder()

    def to_document(self) -> Optional[Document]:
        wxid, content = self.get_wxid_and_content()
        if wxid is None or content is None: return None
        return Document(page_content=f"{wxid}: {content}")


class KebleWechatHistoryLoader:

    def __init__(self, json_filepath: str | Path):
        self.__json_filepath = json_filepath

    def load_messages(self) -> List[WxMessage]:
        docs: List[WxMessage] = []
        with open(self.__json_filepath, "r") as file:
            messages = json.load(file)
            for message in messages:
                parsed_message = WxMessage(**message)
                docs.append(parsed_message)
        return docs

    def load(self) -> List[Document]:
        """parse wechat history
        format explains:
        [{"CompressContent": null, # 转账金额信息，有+与-表示：收到与转出，默认为空
        "ConBlob": "chN3eGlkX2dnNWpibzcyZGkyaTEyehN3eGlkX3BlMXMzenh6OThsajIykgF05paw5qKF5Zut57Sg6aOffumhv+m4vyA6IOaLm+eUn+S/oeaBrwrmrKLov47ovazlj5HvvIzlip/lvrfml6Dph4/vvIEK5pS26I635Y6o6Im677yM5pm65oWn5Lq655Sf77yBCiAg44CK5rOo5oSPIDouLi6AAQCYAQCgAQC4AQDIAQDQAQDwAQD4AQA=", #
        "IntRes1": 0,
        "IntRes2": 0,
        "StrRes1": null,
        "StrRes2": null,
        "mesDes": 1, # 是否为自己发送的消息
        "mesLocalID": 2,
        "mesSvrID": 1920754171758050414, # 服务端的消息ID
        "messageType": 1, # 消息类型，1为文本，3为图片，34为语音，37为好友添加，43为视频，48为位置，49为xml格式消息，10000为系统消息
                here is a dictionary for it {
                    '1':'文字',
                    '3':'图片',
                    '43':'视频',
                    '-1879048185':'微信运动排行榜',
                    '5':'',
                    '47':'表情包',
                    '268445456':'撤回的消息',
                    '34':'语音',
                    '419430449':'转账',
                    '50':'语音电话',
                    '10000':'领取红包',
                    '10000':'消息已发出，但被对方拒收了。',
                    '822083633':'回复消息',
                    '922746929':'拍一拍',
                    '1090519089':'发送文件',
                    '318767153':'付款成功',
                    '436207665':'发红包',
                }
        "msgContent": "招生信息\n欢迎转发，功德无量！", # 消息内容
        "msgCreateTime": 1626161450, # 创建时间（Unix时间戳）
        "msgImgStatus": 1, # 图片的状态
        "msgSeq": 711260330,
        "msgSource": "",
        "msgStatus": 4, # 消息状态，比如发送失败，成功，正在发送
        "msgVoiceText": null}, ...]
        """
        docs: List[Document] = []
        with open(self.__json_filepath, "r") as file:
            messages = json.load(file)
            for message in messages:
                parsed_message = WxMessage(**message)
                docs.append(parsed_message.to_document())
        return [doc for doc in docs if doc is not None]
