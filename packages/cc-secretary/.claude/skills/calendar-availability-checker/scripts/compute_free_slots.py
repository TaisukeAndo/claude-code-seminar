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
    work_start_hour = data.get("work_start_hour", 8)
    work_end_hour = data.get("work_end_hour", 18)
    weekdays_only = data.get("weekdays_only", True)
    min_slot = timedelta(minutes=data.get("min_slot_minutes", 60))

    busy = []
    for b in data.get("busy_intervals", []):
        bstart = datetime.fromisoformat(b["start"]).astimezone(tz)
        bend = datetime.fromisoformat(b["end"]).astimezone(tz)
        if bend > bstart:
            busy.append((bstart, bend))
    busy.sort()

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
        for bstart, bend in busy:
            cs, ce = max(bstart, day_start), min(bend, day_end)
            if ce > cs:
                day_busy.append((cs, ce))
        day_busy.sort()

        merged = []
        for cs, ce in day_busy:
            if merged and cs <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], ce))
            else:
                merged.append((cs, ce))

        free = []
        cursor = day_start
        for bs, be in merged:
            if bs > cursor:
                free.append((cursor, bs))
            cursor = max(cursor, be)
        if cursor < day_end:
            free.append((cursor, day_end))

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
