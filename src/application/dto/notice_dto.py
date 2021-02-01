from dataclasses import dataclass


@dataclass
class NoticeInputDto:
    uid: str
    email_notice: bool
    push_notice: bool
    notice_token: str

@dataclass
class NoticeOutPutDto:
    email_notice: bool
    push_notice: bool
    notice_token: str = None

@dataclass
class NoticeListInputDto:
    uid: str

@dataclass
class NoticeListOutputDto:
    notice_list: dict