#!/usr/bin/env python3
"""Merge busy intervals into free time slots within a daily work window.

Input: path to a JSON file (see SKILL.md for the schema).
Output: JSON printed to stdout with per-date free slots and a
ready-to-paste Japanese bullet list.
"""
import json
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

WEEKDAY_JP = ["月", "火", "水", "木", "金", "土", "日"]


def main():
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)

    tz = ZoneInfo(data.get("timezone", "Asia/Tokyo"))
    start_date = date.fromisoformat(data["start_date"])
    end_date = date.fromisoformat(data["end_date"])
    work_start_hour = data.get("work_start_hour", 9)
    work_end_hour = data.get("work_end_hour", 18)
    weekdays_only = data.get("weekdays_only", True)
    min_slot = timedelta(minutes=data.get("min_slot_minutes", 60))
    lunch_break_start_hour = data.get("lunch_break_start_hour", 12)
    lunch_break_end_hour = data.get("lunch_break_end_hour", 13)

    # 対面の予定には移動時間としてのバッファが必要。「対面の予定の直後」「対面の予定の
    # 直前」どちらの隙間にも同じ発想のバッファを適用しうるが、同じ隙間に両方の理由が
    # 重なっても合計を60分にはせず、常に片側だけ・最大でもこのバッファ分までしか
    # 削らない（詳しくはcompute_free_slotsのコメントを参照）。
    in_person_buffer = timedelta(minutes=data.get("in_person_travel_buffer_minutes", 30))

    # 新しく調整しようとしている予定自体が対面の場合、その予定はその日のどこかの
    # 空き枠に入る想定なので、直前の予定との間にも移動時間を確保する。
    # オンラインの場合はこのバッファは不要。
    new_meeting_is_in_person = data.get("new_meeting_is_in_person", False)
    pre_meeting_buffer = timedelta(minutes=data.get("travel_buffer_before_minutes", 30))

    raw_events = []
    for b in data.get("busy_intervals", []):
        bstart = datetime.fromisoformat(b["start"]).astimezone(tz)
        bend = datetime.fromisoformat(b["end"]).astimezone(tz)
        if bend > bstart:
            raw_events.append((bstart, bend, bool(b.get("is_in_person"))))
    raw_events.sort()

    results = []
    lines = []
    d = start_date
    while d <= end_date:
        weekday_idx = d.weekday()  # 0=Mon ... 6=Sun
        if weekdays_only and weekday_idx >= 5:
            d += timedelta(days=1)
            continue

        day_start = datetime(d.year, d.month, d.day, work_start_hour, 0, tzinfo=tz)
        day_end = datetime(d.year, d.month, d.day, work_end_hour, 0, tzinfo=tz)

        day_busy = []
        for bstart, bend, is_in_person in raw_events:
            cs, ce = max(bstart, day_start), min(bend, day_end)
            if ce > cs:
                day_busy.append((cs, ce, is_in_person))

        if lunch_break_start_hour is not None and lunch_break_end_hour is not None:
            lunch_start = datetime(d.year, d.month, d.day, lunch_break_start_hour, 0, tzinfo=tz)
            lunch_end = datetime(d.year, d.month, d.day, lunch_break_end_hour, 0, tzinfo=tz)
            cs, ce = max(lunch_start, day_start), min(lunch_end, day_end)
            if ce > cs:
                day_busy.append((cs, ce, False))

        day_busy.sort()

        # 予定を時系列にマージしつつ、各ブロックの「開始側」「終了側」がそれぞれ
        # 対面の予定によるものかを別々に記録する。重なり合う予定の一方だけが対面でも
        # 該当する側は対面扱いにする（OR）。
        merged = []
        for cs, ce, is_in_person in day_busy:
            if merged and cs <= merged[-1]["end"]:
                cur = merged[-1]
                if cs == cur["start"]:
                    cur["start_in_person"] = cur["start_in_person"] or is_in_person
                if ce > cur["end"]:
                    cur["end"] = ce
                    cur["end_in_person"] = is_in_person
                elif ce == cur["end"]:
                    cur["end_in_person"] = cur["end_in_person"] or is_in_person
            else:
                merged.append({
                    "start": cs, "end": ce,
                    "start_in_person": is_in_person,
                    "end_in_person": is_in_person,
                })

        # 隙間（空き候補）ごとに、前の予定を出た後の移動時間（開始側トリム）と
        # 次の予定に入る前の移動時間（終了側トリム）のどちらが必要かを判定する。
        # 同じ隙間で両方の理由が発生しても、実際に必要な移動は1回分なので
        # 合計せず、次の予定側（より動かせない制約）を優先して片側だけを削る。
        def trimmed_gap(gap_start, gap_end, prev_end_in_person, next_start_in_person, has_prev):
            if next_start_in_person:
                new_end = max(gap_start, gap_end - in_person_buffer)
                return gap_start, new_end
            start_side_buffer = timedelta(0)
            if prev_end_in_person:
                start_side_buffer = max(start_side_buffer, in_person_buffer)
            if new_meeting_is_in_person and has_prev:
                start_side_buffer = max(start_side_buffer, pre_meeting_buffer)
            if start_side_buffer:
                new_start = min(gap_end, gap_start + start_side_buffer)
                return new_start, gap_end
            return gap_start, gap_end

        free = []
        cursor = day_start
        for i, blk in enumerate(merged):
            bs, be = blk["start"], blk["end"]
            if bs > cursor:
                prev_end_in_person = merged[i - 1]["end_in_person"] if i > 0 else False
                gap_start, gap_end = trimmed_gap(
                    cursor, bs, prev_end_in_person, blk["start_in_person"], cursor > day_start
                )
                if gap_end > gap_start:
                    free.append((gap_start, gap_end))
            cursor = max(cursor, be)
        if cursor < day_end:
            prev_end_in_person = merged[-1]["end_in_person"] if merged else False
            gap_start, gap_end = trimmed_gap(cursor, day_end, prev_end_in_person, False, cursor > day_start)
            if gap_end > gap_start:
                free.append((gap_start, gap_end))

        free = [(s, e) for s, e in free if (e - s) >= min_slot]

        if free:
            slot_strs = [f"{s.strftime('%H:%M')}-{e.strftime('%H:%M')}" for s, e in free]
            date_label = f"{d.month}/{d.day}({WEEKDAY_JP[weekday_idx]})"
            lines.append(f"・{date_label} " + "、".join(slot_strs))
            results.append({
                "date": d.isoformat(),
                "weekday": WEEKDAY_JP[weekday_idx],
                "slots": [{"start": s.strftime("%H:%M"), "end": e.strftime("%H:%M")} for s, e in free],
            })

        d += timedelta(days=1)

    output = {
        "free_slots_by_date": results,
        "bullet_list_text": "\n".join(lines) if lines else "(指定期間内に条件を満たす空き時間はありませんでした)",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
