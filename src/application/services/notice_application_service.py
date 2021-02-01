from dataclasses import asdict

from src.application.dto.notice_dto import NoticeInputDto, NoticeOutPutDto, NoticeListOutputDto, NoticeListInputDto
from src.application.dto.users_dto import NoticeDto
from src.application.repository.notice_repository import NoticeRepo
from src.domain.services.notice_domain_serivce import NoticeListDomainService


class NoticeApplicationService:
    def __init__(self, input_dto: NoticeInputDto or NoticeListInputDto):
        self._input_dto = input_dto

    def change_notice_status(self) -> NoticeOutPutDto:
        uid          = self._input_dto.uid
        email_notice = self._input_dto.email_notice
        push_notice  = self._input_dto.push_notice
        notice_token = self._input_dto.notice_token

        notice_param = NoticeDto(email_notice, push_notice, notice_token)
        NoticeRepo().update_notice(uid, asdict(notice_param))
        return NoticeOutPutDto(email_notice, push_notice, notice_token)

    def notice_list(self) -> NoticeListOutputDto:
        uid         = self._input_dto.uid
        notice_docs = NoticeRepo().find_notice_list(uid)
        notice_list = NoticeListDomainService(notice_docs).sorting_notice_list()
        return NoticeListOutputDto(notice_list)