# -*- coding: utf-8 -*-
"""
@Author   : QH
@Time     :2024/3/25
@File     :ClassInAPI.py
@IDE      :PyCharm
"""

import time
import hashlib
import requests
import json

"""
如果你有任何疑问，可以通过eeoapisupport@eeoa.com联系我们

If you have any questions you can contact us at eeoapisupport@eeoa.com

ClassIn APIDoc：https://docs.eeo.cn/api/  
"""


# 请求域名
domain = 'https://api.eeo.cn'


class Path:
    def __init__(self):
        # 用户相关接口
        self.register = domain + '/partner/api/course.api.php?action=register'
        self.registerMultiple = domain + '/partner/api/course.api.php?action=registerMultiple'
        self.modifyPassword = domain + '/partner/api/course.api.php?action=modifyPassword'
        self.addSchoolStudent = domain + '/partner/api/course.api.php?action=addSchoolStudent'
        self.editSchoolStudent = domain + '/partner/api/course.api.php?action=editSchoolStudent'
        self.addTeacher = domain + '/partner/api/course.api.php?action=addTeacher'
        self.editTeacher = domain + '/partner/api/course.api.php?action=editTeacher'
        self.stopUsingTeacher = domain + '/partner/api/course.api.php?action=stopUsingTeacher'
        self.restartUsingTeacher = domain + '/partner/api/course.api.php?action=restartUsingTeacher'

        # 课程相关接口
        self.addCourse = domain + '/partner/api/course.api.php?action=addCourse'
        self.editCourse = domain + '/partner/api/course.api.php?action=editCourse'
        self.endCourse = domain + '/partner/api/course.api.php?action=endCourse'
        self.modifyCourseTeacher = domain + '/partner/api/course.api.php?action=modifyCourseTeacher'
        self.removeCourseTeacher = domain + '/partner/api/course.api.php?action=removeCourseTeacher'

        # 课节相关接口
        self.addCourseClass = domain + '/partner/api/course.api.php?action=addCourseClass'
        self.addCourseClassMultiple = domain + '/partner/api/course.api.php?action=addCourseClassMultiple'
        self.editCourseClass = domain + '/partner/api/course.api.php?action=editCourseClass'
        self.delCourseClass = domain + '/partner/api/course.api.php?action=delCourseClass'
        self.modifyClassSeatNum = domain + '/partner/api/course.api.php?action=modifyClassSeatNum'

        # 操作课程或课节学生
        self.addCourseStudent = domain + '/partner/api/course.api.php?action=addCourseStudent'
        self.delCourseStudent = domain + '/partner/api/course.api.php?action=delCourseStudent'
        self.addCourseStudentMultiple = domain + '/partner/api/course.api.php?action=addCourseStudentMultiple'
        self.delCourseStudentMultiple = domain + '/partner/api/course.api.php?action=delCourseStudentMultiple'
        self.addClassStudentMultiple = domain + '/partner/api/course.api.php?action=addClassStudentMultiple'
        self.delClassStudentMultiple = domain + '/partner/api/course.api.php?action=delClassStudentMultiple'
        self.addCourseClassStudent = domain + '/partner/api/course.api.php?action=addCourseClassStudent'

        # 机构标签
        self.addSchoolLabel = domain + '/partner/api/course.api.php?action=addSchoolLabel'
        self.updateSchoolLabel = domain + '/partner/api/course.api.php?action=updateSchoolLabel'
        self.deleteSchoolLabel = domain + '/partner/api/course.api.php?action=deleteSchoolLabel'

        # 课程课节标签相关
        self.addCourseLabels = domain + '/partner/api/course.api.php?action=addCourseLabels'
        self.addClassLabels = domain + '/partner/api/course.api.php?action=addClassLabels'

        # 同步班级昵称
        self.modifyGroupMemberNickname = domain + '/partner/api/course.api.php?action=modifyGroupMemberNickname'

        # 云盘相关
        self.getFolderList = domain + '/partner/api/cloud.api.php?action=getFolderList'
        self.getCloudList = domain + '/partner/api/cloud.api.php?action=getCloudList'
        self.getTopFolderId = domain + '/partner/api/cloud.api.php?action=getTopFolderId'
        self.uploadFile = domain + '/partner/api/cloud.api.php?action=uploadFile'
        self.renameFile = domain + '/partner/api/cloud.api.php?action=renameFile'
        self.delFile = domain + '/partner/api/cloud.api.php?action=delFile'
        self.createFolder = domain + '/partner/api/cloud.api.php?action=createFolder'
        self.renameFolder = domain + '/partner/api/cloud.api.php?action=renameFolder'
        self.delFolder = domain + '/partner/api/cloud.api.php?action=delFolder'

        # 直播相关接口
        self.setClassVideoMultiple = domain + '/partner/api/course.api.php?action=setClassVideoMultiple'
        self.deleteClassVideo = domain + '/partner/api/course.api.php?action=deleteClassVideo'
        self.updateClassLockStatus = domain + '/partner/api/course.api.php?action=updateClassLockStatus'
        self.getWebcastUrl = domain + '/partner/api/course.api.php?action=getWebcastUrl'

        # 唤醒客户端进入教室
        self.getLoginLinked = domain + '/partner/api/course.api.php?action=getLoginLinked'


class API:
    def __init__(self, school_uid, school_secret):
        """
        初始化eeo api对象，需传输eeo的SID和SECRET
        :param school_uid: eeo 学校账号UID
        :param school_secret: 密钥
        """

        self.SID = school_uid
        self.SECRET = school_secret
        # 创建请求url的对象
        self.action = Path()

    def get_safe_key(self):
        time_stamp = int(time.time())
        secret = self.SECRET
        safe_key = hashlib.md5((secret + str(time_stamp)).encode()).hexdigest()
        return time_stamp, safe_key

    def register(self, email, nickname, password, addToSchoolMember):
        """
        注册用户  https://docs.eeo.cn/api/zh-hans/user/register.html
        @param email: string 必填-用户邮箱
        @param nickname: string 非必填-eeo.cn姓名，如用户是首次注册，将同步姓名信息至客户端昵称，非首次注册则不修改用户当前昵称
        @param password:string 必填-密码
        @param addToSchoolMember:int 非必填-1学生 2老师
        @return:
        """
        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'email': email,
            'password': password,
            'nickname': nickname,
            'addToSchoolMember': addToSchoolMember
        }

        response = json.loads((requests.post(url=self.action.register, data=data)).text)
        if 'data' in response.keys():
            return response['data']
        else:
            return ''

    def register_multiple(self, userJson):
        """
        批量注册用户  https://docs.eeo.cn/api/zh-hans/user/registerMultiple.html
        @param userJson:
        telephone和email 2选1
        [
        {"telephone":"xxxx","nickname":"xxxx","password":"xxxx"},
        {"email":"xxxx","nickname":"xxxx","password":"xxxx"}
        ]
        @return:
        """
        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'userJson': json.dumps(userJson)
        }

        response = json.loads((requests.post(url=self.action.registerMultiple, data=data)).text)

        return response

    def add_teacher(self, teacherAccount, teacherName):
        """
        添加学校老师  https://docs.eeo.cn/api/zh-hans/user/addTeacher.html
        :param teacherAccount:string 老师账号
        :param teacherName:string 老师姓名
        :return:
        """
        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'teacherAccount': teacherAccount,
            'teacherName': teacherName
        }

        response = json.loads((requests.post(url=self.action.addTeacher, data=data)).text)
        return response

    def edit_teacher(self, teacherUid, teacherName):
        """
        编辑老师信息  https://docs.eeo.cn/api/zh-hans/user/editTeacher.html
        :param teacherUid:string 用户UID
        :param teacherName:string 老师姓名
        :return:
        """
        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'teacherUid': teacherUid,
            'teacherName': teacherName
        }

        response = json.loads((requests.post(url=self.action.editTeacher, data=data)).text)
        return response

    def add_school_student(self, studentAccount, studentName):
        """
        添加学校学生  https://docs.eeo.cn/api/zh-hans/user/addSchoolStudent.html
        :param studentAccount:string 学生账号
        :param studentName:string 学生姓名
        :return:
        """
        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'studentAccount': studentAccount,
            'studentName': studentName
        }

        response = (requests.post(url=self.action.addSchoolStudent, data=data)).text

        return json.loads(response)

    def edit_school_student(self, studentUid, studentName):
        """
        添加学校学生  https://docs.eeo.cn/api/zh-hans/user/editSchoolStudent.html
        :param studentUid:string 用户UID
        :param studentName:string 学生姓名
        :return:
        """
        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'studentUid': studentUid,
            'studentName': studentName
        }

        response = (requests.post(url=self.action.editSchoolStudent, data=data)).text

        return json.loads(response)

    def add_course(self, courseName, folderId=None, expiryTime=None, mainTeacherUid=None, allowAddFriend=None,
                   allowStudentModifyNickname=None, courseUniqueIdentity=None):
        """
        创建课程  https://docs.eeo.cn/api/zh-hans/classroom/addCourse.html
        :param courseName: string 必填，课程名
        :param folderId: int 非必填，授权云盘文件夹ID
        :param expiryTime: int时间戳, 非必填，课程有效期，默认空永久有效，
        :param mainTeacherUid: int非必填，班主任uid，默认空
        :param allowAddFriend: int非必填，是否允许班级成员在群里互相添加好友，0=不允许，1=允许，传非0或非1报参数错误
        :param allowStudentModifyNickname:int非必填，是否允许学生在群里修改其班级昵称，0=不允许，1=允许，传非0或非1报参数错误，不传默认0
        :param courseUniqueIdentity: string非必填，机构可传唯一标识，传入此值后，我们会检验已创建课程中是否有该唯一标识
        :return:
        """
        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'courseName': courseName,
            'folderId': folderId,
            'expiryTime': expiryTime,
            'mainTeacherUid': mainTeacherUid,
            'allowAddFriend': allowAddFriend,
            'allowStudentModifyNickname': allowStudentModifyNickname,
            'courseUniqueIdentity': courseUniqueIdentity,
        }

        response = json.loads((requests.post(url=self.action.addCourse, data=data)).text)
        if 'data' in response.keys():

            return response['data']
        else:
            return ''

    def end_course(self, courseId):
        """
        https://docs.eeo.cn/api/zh-hans/classroom/endCourse.html
        结束课程   注意：课程下没有正在上的课节，即可结束课程。
        如果课程下有尚未开始的课节，会删除未开始的课节之后结束课程，请谨慎使用此功能
        :param courseId:int 课程ID
        :return:
        """
        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'courseId': courseId,
        }
        response = json.loads((requests.post(url=self.action.endCourse, data=data)).text)
        # end_result = response['error_info']['error']
        # result = '结课状态：{}'.format(end_result)
        return response

    def add_course_class(self, courseId, className, beginTime, endTime, teacherUid, assistantUid='', seatNum=6,
                         record=0, live=0, replay=0):
        """
        创建课节  具体可参考 https://docs.eeo.cn/api/zh-hans/classroom/addCourseClass.html
        :param courseId: int 课程ID
        :param className: string 课节名称
        :param beginTime: int 时间戳，课节开始时间
        :param endTime: int 时间戳，课节结束时间
        :param teacherUid: int 教师UID
        :param assistantUid: int 助教UID
        :param seatNum: int 1VX 上台人数
        :param record: 录课状态，默认0  0关 1开
        :param live: 直播状态，默认0  0关 1开
        :param replay: 回放状态，默认0  0关 1开
        :return:
        """

        time_stamp, safe_key = self.get_safe_key()
        if assistantUid == '':
            data = {
                'SID': self.SID,
                'timeStamp': time_stamp,
                'safeKey': safe_key,
                'courseId': courseId,
                'className': className,
                'beginTime': beginTime,
                'endTime': endTime,
                'teacherUid': teacherUid,
                'seatNum': seatNum,
                'record': record,
                'live': live,
                'replay': replay
            }
        else:
            data = {
                'SID': self.SID,
                'timeStamp': time_stamp,
                'safeKey': safe_key,
                'courseId': courseId,
                'className': className,
                'beginTime': beginTime,
                'endTime': endTime,
                'teacherUid': teacherUid,
                'assistantUid': assistantUid,
                'seatNum': seatNum,
                'record': record,
                'live': live,
                'replay': replay
            }

        response = json.loads(requests.post(url=self.action.addCourseClass, data=data).text)
        if 'data' in response.keys():
            return response['data']
        else:
            return ''

    def edit_course_class(self, courseId, classId, record, live, replay):
        """
        编辑课节  https://docs.eeo.cn/api/zh-hans/classroom/editCourseClass.html
        @param courseId:int 课程ID
        @param classId:int 课节ID
        @param record:
        @param live:
        @param replay:
        @return:
        """

        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'courseId': courseId,
            'classId': classId,
            'record': record,
            'live': live,
            'replay': replay

        }

        response = json.loads(requests.post(url=self.action.editCourseClass, data=data).text)

        return response

    def del_course_class(self, courseId, classId):
        """
        删除课节  https://docs.eeo.cn/api/zh-hans/classroom/delCourseClass.html
        @param courseId:int 课程ID
        @param classId:int 课节ID
        @return:
        """

        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'courseId': courseId,
            'classId': classId,
        }

        response = json.loads(requests.post(url=self.action.delCourseClass, data=data).text)

        return response

    def add_course_student(self, courseId, studentUid, identity=1):
        """
        添加课程学生  https://docs.eeo.cn/api/zh-hans/classroom/addCourseStudent.html
        :param courseId: int 课程ID
        :param studentUid: int 用户UID
        :param identity:int 默认为课程学生，学生和旁听的识别(1 为学生,2 为旁听)
        :return:
        """
        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'courseId': courseId,
            'studentUid': studentUid,
            'identity': identity
        }

        response = json.loads(requests.post(url=self.action.addCourseStudent, data=data).text)

        return response

    def add_course_student_multiple(self, courseId, user_list, identity=1):
        """
        批量添加课程学生 https://docs.eeo.cn/api/zh-hans/classroom/addCourseStudentMultiple.html
        :param courseId:int 课程ID
        :param user_list:[{'uid':123},{'uid':456}]
        :param identity:int 默认为课程学生，学生和旁听的识别(1 为学生,2 为旁听)
        :return:
        """

        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'courseId': courseId,
            'identity': identity,
            'studentJson': json.dumps(user_list)
        }

        response = json.loads(requests.post(url=self.action.addCourseStudentMultiple, data=data).text)

        return response

    def del_course_student(self, courseId, studentUid, identity=1):
        """
        删除课程学生    https://docs.eeo.cn/api/zh-hans/classroom/delCourseStudent.html
        :param courseId: int 课程ID
        :param studentUid:int 用户UID
        :param identity:int 默认为课程学生，学生和旁听的识别(1 为学生,2 为旁听)
        :return:
        """

        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'courseId': courseId,
            'identity': identity,
            'studentUid': studentUid
        }

        response = json.loads(requests.post(url=self.action.delCourseStudent, data=data).text)

        return response

    def del_course_student_multiple(self, courseId, user_list, identity):
        """
        批量删除课程学生    https://docs.eeo.cn/api/zh-hans/classroom/delCourseStudentMultiple.html
        :param courseId: int 课程ID
        :param user_list:['123', ..., '456']
        :param identity:int 默认为课程学生，学生和旁听的识别(1 为学生,2 为旁听)
        :return:
        """

        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'courseId': courseId,
            'identity': identity,
            'studentUidJson': json.dumps(user_list)
        }

        response = json.loads(requests.post(url=self.action.delCourseStudentMultiple, data=data).text)

        return response

    def modify_class_seatNum(self, courseId, classId, seatNum, isHd):
        """
        修改课节上台人数及清晰度  https://docs.eeo.cn/api/zh-hans/classroom/modifyClassSeatNum.html
        :param courseId: int 课程ID
        :param classId: int 课节ID
        :param seatNum: int 上台人数
        :param isHd: 是否高清(0=非高清，1=高清，2=全高清，非1的数字都会当做0来处理)
        :return:
        """
        time_stamp, safe_key = self.get_safe_key()
        data = {
            'SID': self.SID,
            'timeStamp': time_stamp,
            'safeKey': safe_key,
            'courseId': courseId,
            'classId': classId,
            'seatNum': seatNum,
            'isHd': isHd
        }

        response = json.loads(requests.post(url=self.action.modifyClassSeatNum, data=data).text)

        return response
