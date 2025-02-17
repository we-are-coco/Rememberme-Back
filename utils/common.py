from datetime import datetime, timezone


def get_time_description(notification: datetime):
    """ 알림 시간에 따른 설명 반환 """
    now = datetime.now()
    diff = notification - now

    if diff.days > 0:
        return f"{diff.days}일 후"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600}시간 후"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60}분 후"
    else:
        return "시간이 지났어요"