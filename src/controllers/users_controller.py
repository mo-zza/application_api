from flask import request

from src.application.services.sign_in_application_service import SignApplicationService
from src.application.services.sign_up_application_service import SignUpApplicationService
from src.application.services.password_applicatioin_service import PasswordApplicationService
from src.application.services.user_asset_application_service import UserAssetApplicationService
from src.application.services.user_history_application_service import UserHistoryApplicationService
from src.application.services.user_chart_application_service import UserChartApplicationChart
from src.application.services.notice_application_service import NoticeApplicationService
from src.application.services.user_nick_name_application_service import NickNameApplicationService
from src.application.services.profile_upload_application import ProfileUploadApplication
from src.application.dto.users_dto import SignInInputDto, PasswordInputDto, SignUpInputDto, SimpleInputDto, NickNameInputDto, ProfileInputDto
from src.application.dto.notice_dto import NoticeInputDto, NoticeListInputDto
from src.adapter.response import success_response
from src.adapter.user_athentication import EmailAuth
from src.controllers import users_bp as bp
from src.domain.value.controller_data import userEmailArg, simplePwArg, emailNoticeArg, pushNoticeArg, noticeTokenArg, nickNameArg


@bp.route('login', methods=['GET'])
@EmailAuth
def login(uid):
    request.args.get(userEmailArg)
    simple_pw = request.args.get(simplePwArg)
    input_dto = SignInInputDto(uid=uid, simple_pw=simple_pw)
    token     = SignApplicationService(input_dto).sign_in()
    return success_response(token, 200)

@bp.route('', methods=['POST'])
@EmailAuth
def create_user(uid):
    user_email   = request.form[userEmailArg]
    simple_pw    = request.form[simplePwArg]
    email_notice = request.form[emailNoticeArg]
    push_notice  = request.form[pushNoticeArg]
    notice_token = request.form[noticeTokenArg]
    
    input_dto  = SignUpInputDto(uid, user_email, simple_pw, email_notice, push_notice, notice_token)
    user_info  = SignUpApplicationService(input_dto).create_user()
    return success_response(user_info, 200)

@bp.route('password', methods=['PUT'])
@EmailAuth
def change_password(uid):
    user_email    = request.form[userEmailArg]
    new_simple_pw = request.form[simplePwArg]
    input_dto     = PasswordInputDto(uid, user_email, new_simple_pw)
    new_simple_pw = PasswordApplicationService(input_dto).change_password()
    return success_response(new_simple_pw, 200)

@bp.route('password', methods=['GET'])
@EmailAuth
def get_password(uid):
    user_email = request.args.get(userEmailArg)
    input_dto  = PasswordInputDto(uid, user_email)
    simple_pw  = PasswordApplicationService(input_dto).get_password()
    return success_response(simple_pw, 200)

@bp.route('assets', methods=['GET'])
@EmailAuth
def get_user_asset(uid):
    user_email = request.args.get(userEmailArg)
    input_dto  = SimpleInputDto(user_email, uid)
    user_asset = UserAssetApplicationService(input_dto).user_asset()
    return success_response(user_asset, 200)

@bp.route('history', methods=['GET'])
@EmailAuth
def get_user_history(uid):
    user_email   = request.args.get(userEmailArg)
    input_dto    = SimpleInputDto(user_email, uid)
    user_history = UserHistoryApplicationService(input_dto).user_history()
    return success_response(user_history, 200)

@bp.route('chart', methods=['GET'])
@EmailAuth
def get_user_chart(uid):
    user_email = request.args.get(userEmailArg)
    input_dto  = SimpleInputDto(user_email, uid)
    user_chart = UserChartApplicationChart(input_dto).user_chart()
    return success_response(user_chart, 200)

@bp.route('notice', methods=['PUT'])
@EmailAuth
def update_notice_settinf(uid):
    request.form[userEmailArg]
    email_notice = request.form[emailNoticeArg]
    push_notice  = request.form[pushNoticeArg]
    notice_token = request.form[noticeTokenArg]

    input_dto     = NoticeInputDto(uid, email_notice, push_notice, notice_token)
    update_result = NoticeApplicationService(input_dto).change_notice_status()
    return success_response(update_result, 200)

@bp.route('notice/list', methods=['GET'])
@EmailAuth
def get_notice_list(uid):
    request.args.get(userEmailArg)
    input_dto   = NoticeListInputDto(uid)
    notice_list = NoticeApplicationService(input_dto).notice_list()
    return success_response(notice_list, 200)

@bp.route('nickName', methods=['PUT'])
@EmailAuth
def update_nick_name(uid):
    request.form[userEmailArg]
    new_nick_name   = request.form[nickNameArg]
    input_dto       = NickNameInputDto(uid, new_nick_name)
    update_response = NickNameApplicationService(input_dto).update_nick_name()
    return success_response(update_response, 200)

@bp.route('profile', methods=['PUT'])
@EmailAuth
def update_profile(uid):
    request.form['user_email']
    profile         = request.form['profile_url']
    input_dto       = ProfileInputDto(uid, profile)
    new_profile_url = ProfileUploadApplication(input_dto).upload_profile()
    return success_response(new_profile_url, 200)