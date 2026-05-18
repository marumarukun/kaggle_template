"""Kaggle提出監視スクリプト: PENDING→COMPLETE/ERRORの所要時間を計測する."""

import argparse
import json
import re
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi


def log(msg: str) -> None:
    """タイムスタンプ付きでメッセージを出力する."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def parse_time_limit(value: str) -> float | None:
    """時間制限文字列をパースして秒数を返す. 例: '9h', '30m', '2h30m'."""
    if not value:
        return None
    total = 0.0
    pattern = re.findall(r"(\d+(?:\.\d+)?)\s*([hHmMsS])", value)
    if not pattern:
        try:
            return float(value)
        except ValueError:
            print(f"警告: 時間制限 '{value}' をパースできません。無視します。", flush=True)
            return None
    for num, unit in pattern:
        unit = unit.lower()
        if unit == "h":
            total += float(num) * 3600
        elif unit == "m":
            total += float(num) * 60
        elif unit == "s":
            total += float(num)
    return total


def format_duration(seconds: float) -> str:
    """秒数を人間が読みやすい形式にフォーマットする."""
    if seconds < 60:
        return f"{seconds:.0f}秒"
    elif seconds < 3600:
        m, s = divmod(int(seconds), 60)
        return f"{m}分{s}秒"
    else:
        h, rem = divmod(int(seconds), 3600)
        m, s = divmod(rem, 60)
        return f"{h}時間{m}分{s}秒"


def get_competition_from_metadata() -> str | None:
    """sub/kernel-metadata.json からコンペスラッグを取得する."""
    metadata_path = Path("sub/kernel-metadata.json")
    if not metadata_path.exists():
        return None
    try:
        data = json.loads(metadata_path.read_text())
        sources = data.get("competition_sources", [])
        return sources[0] if sources else None
    except (json.JSONDecodeError, IndexError):
        return None


def get_submissions(api: KaggleApi, competition: str) -> list[dict]:
    """提出一覧を取得して辞書のリストとして返す. date は UTC aware datetime."""
    subs = api.competition_submissions(competition)
    result = []
    for s in subs:
        # Kaggle API は naive datetime を UTC として返す
        date_obj = s.date
        if date_obj is not None and date_obj.tzinfo is None:
            date_obj = date_obj.replace(tzinfo=timezone.utc)
        result.append({
            "ref": s.ref,
            "date": date_obj,
            "description": s.description or "",
            "status": str(s.status),
            "public_score": s.public_score or "",
            "error_description": s.error_description or "",
        })
    return result


def format_local(dt: datetime) -> str:
    """UTC datetime をローカル時刻文字列にフォーマットする."""
    if dt is None:
        return "(不明)"
    return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S")


def main():
    parser = argparse.ArgumentParser(description="Kaggle提出の所要時間を計測する")
    parser.add_argument("--competition", "-c", type=str, default=None,
                        help="コンペティションスラッグ (例: birdclef-2026)")
    parser.add_argument("--interval", "-i", type=int, default=60,
                        help="ポーリング間隔（秒）(デフォルト: 60)")
    parser.add_argument("--time-limit", "-t", type=str, default=None,
                        help="コンペの実行時間制限 (例: 9h, 30m)")
    args = parser.parse_args()

    # コンペスラッグの解決
    competition = args.competition or get_competition_from_metadata()
    if not competition:
        print("エラー: --competition を指定するか、sub/kernel-metadata.json を配置してください。",
              flush=True)
        sys.exit(1)

    time_limit_sec = parse_time_limit(args.time_limit)

    # API初期化
    api = KaggleApi()
    api.authenticate()

    log(f"コンペ: {competition}")
    if time_limit_sec:
        log(f"制限時間: {format_duration(time_limit_sec)}")
    log(f"ポーリング間隔: {args.interval}秒")
    print(flush=True)

    # Step 1: スナップショット取得
    initial_subs = get_submissions(api, competition)
    initial_refs = {s["ref"] for s in initial_subs}
    log(f"スナップショット取得: 提出{len(initial_subs)}件")

    # 既にPENDINGのものがあれば追跡対象にする (起点は API の date = 実提出時刻 UTC)
    tracking: dict[int, datetime] = {}  # ref -> 提出時刻 (UTC)
    for s in initial_subs:
        if "PENDING" in s["status"]:
            tracking[s["ref"]] = s["date"]
            log(f"既存のPENDING提出を検知: {s['description']} (ref={s['ref']}, 提出時刻={format_local(s['date'])})")

    if not tracking:
        log("新しい提出を待機中...")

    # Ctrl+C ハンドリング
    def handle_sigint(signum, frame):
        print(flush=True)
        if tracking:
            now = datetime.now(timezone.utc)
            elapsed = (now - min(tracking.values())).total_seconds()
            log(f"中断: 現在の経過時間 {format_duration(elapsed)}")
        else:
            log("中断: まだ提出は検知されていません")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)

    # Step 2-4: ポーリングループ
    consecutive_errors = 0

    while True:
        time.sleep(args.interval)

        try:
            current_subs = get_submissions(api, competition)
            consecutive_errors = 0
        except Exception as e:
            consecutive_errors += 1
            if consecutive_errors >= 3:
                log(f"警告: API呼び出しが3回連続失敗 ({e})")
            continue

        # 新しい提出の検知
        for s in current_subs:
            if s["ref"] not in initial_refs and s["ref"] not in tracking:
                tracking[s["ref"]] = s["date"]
                initial_refs.add(s["ref"])
                log(f"新しい提出を検知! {s['description']} (ref={s['ref']}, 提出時刻={format_local(s['date'])})")

        # 追跡中の提出のステータスチェック
        now_utc = datetime.now(timezone.utc)
        completed = []
        for ref, submit_time in tracking.items():
            sub = next((s for s in current_subs if s["ref"] == ref), None)
            if sub is None:
                continue

            status = sub["status"]
            elapsed = (now_utc - submit_time).total_seconds()

            if "COMPLETE" in status:
                completed.append(ref)
                print(flush=True)
                print("=" * 50, flush=True)
                print(f"  COMPLETE!", flush=True)
                print(f"  提出: {sub['description']}", flush=True)
                print(f"  提出時刻: {format_local(submit_time)}", flush=True)
                print(f"  完了時刻: {format_local(now_utc)}", flush=True)
                print(f"  経過時間: {format_duration(elapsed)}", flush=True)
                if sub["public_score"]:
                    print(f"  スコア: {sub['public_score']}", flush=True)
                if time_limit_sec:
                    pct = (elapsed / time_limit_sec) * 100
                    print(f"  制限時間に対する使用率: {pct:.1f}% ({format_duration(elapsed)} / {format_duration(time_limit_sec)})", flush=True)
                print("=" * 50, flush=True)
                print(flush=True)

            elif "ERROR" in status:
                completed.append(ref)
                print(flush=True)
                print("=" * 50, flush=True)
                print(f"  ERROR!", flush=True)
                print(f"  提出: {sub['description']}", flush=True)
                print(f"  提出時刻: {format_local(submit_time)}", flush=True)
                print(f"  完了時刻: {format_local(now_utc)}", flush=True)
                print(f"  経過時間: {format_duration(elapsed)}", flush=True)
                if sub["error_description"]:
                    print(f"  エラー: {sub['error_description']}", flush=True)
                print("=" * 50, flush=True)
                print(flush=True)

            else:
                log(f"PENDING... {sub['description']} (経過: {format_duration(elapsed)})")

        for ref in completed:
            del tracking[ref]

        # 全ての追跡が完了し、かつ最初から追跡していたものがあった場合は終了
        if not tracking and completed:
            log("全ての提出が完了しました。終了します。")
            break


if __name__ == "__main__":
    main()
