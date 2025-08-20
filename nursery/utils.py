from datetime import datetime, timedelta
from urllib.parse import quote


def create_google_calendar_url(schedule):
    """
    見学スケジュールからGoogleカレンダー追加用URLを生成
    """
    # イベントタイトル
    title = f"【保育園見学】{schedule.nursery.name}"
    
    # 日時の設定
    if schedule.visit_time:
        # 時間が指定されている場合
        start_datetime = datetime.combine(schedule.visit_date, schedule.visit_time)
        # 見学時間を1時間と仮定
        end_datetime = start_datetime + timedelta(hours=1)
        
        # GoogleカレンダーのフォーマットはYYYYMMDDTHHMMSS
        dates = f"{start_datetime.strftime('%Y%m%dT%H%M%S')}/{end_datetime.strftime('%Y%m%dT%H%M%S')}"
    else:
        # 時間が未定の場合は終日イベントとして登録
        dates = f"{schedule.visit_date.strftime('%Y%m%d')}/{(schedule.visit_date + timedelta(days=1)).strftime('%Y%m%d')}"
    
    # 詳細説明
    details_parts = [
        f"保育園名: {schedule.nursery.name}",
        f"施設タイプ: {schedule.nursery.nursery_type}",
        f"電話番号: {schedule.nursery.phone_number}",
    ]
    
    if schedule.contact_person:
        details_parts.append(f"担当者: {schedule.contact_person}")
    
    if schedule.notes:
        details_parts.append(f"\\nメモ: {schedule.notes}")
    
    details = "\\n".join(details_parts)
    
    # 場所
    location = schedule.nursery.address
    
    # GoogleカレンダーURLの構築
    base_url = "https://calendar.google.com/calendar/render"
    params = {
        'action': 'TEMPLATE',
        'text': title,
        'dates': dates,
        'details': details,
        'location': location,
    }
    
    # URLパラメータの組み立て
    param_strings = []
    for key, value in params.items():
        param_strings.append(f"{key}={quote(str(value))}")
    
    return f"{base_url}?{'&'.join(param_strings)}"


def create_ics_content(schedule):
    """
    見学スケジュールからICSファイルの内容を生成
    """
    from datetime import datetime
    import uuid
    
    # イベントタイトル
    summary = f"【保育園見学】{schedule.nursery.name}"
    
    # 日時の設定
    if schedule.visit_time:
        start_datetime = datetime.combine(schedule.visit_date, schedule.visit_time)
        end_datetime = start_datetime + timedelta(hours=1)
        dtstart = start_datetime.strftime('%Y%m%dT%H%M%S')
        dtend = end_datetime.strftime('%Y%m%dT%H%M%S')
    else:
        # 終日イベント
        dtstart = schedule.visit_date.strftime('%Y%m%d')
        dtend = (schedule.visit_date + timedelta(days=1)).strftime('%Y%m%d')
    
    # 説明
    description = f"保育園名: {schedule.nursery.name}\\n"
    description += f"施設タイプ: {schedule.nursery.nursery_type}\\n"
    description += f"電話番号: {schedule.nursery.phone_number}\\n"
    if schedule.contact_person:
        description += f"担当者: {schedule.contact_person}\\n"
    if schedule.notes:
        description += f"\\nメモ: {schedule.notes}"
    
    # UIDの生成
    uid = str(uuid.uuid4())
    
    # ICSファイルの内容
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//HoikuNavi//見学スケジュール//JP
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:{summary}
DESCRIPTION:{description}
LOCATION:{schedule.nursery.address}
END:VEVENT
END:VCALENDAR"""
    
    return ics_content