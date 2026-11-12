#!/usr/bin/env python3
"""A tiny command-line to-do manager that stores tasks in a JSON file."""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def store_path() -> Path:
    return Path(os.environ.get("TASKS_FILE", Path.home() / ".tasks.json"))


def load() -> list:
    p = store_path()
    if not p.exists():
        return []
    return json.loads(p.read_text())


def save(tasks: list) -> None:
    store_path().write_text(json.dumps(tasks, indent=2))


def add(text: str) -> dict:
    tasks = load()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": new_id, "text": text, "done": False,
            "created": datetime.now().isoformat(timespec="seconds")}
    tasks.append(task)
    save(tasks)
    return task


def mark_done(task_id: int) -> bool:
    tasks = load()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save(tasks)
            return True
    return False


def delete(task_id: int) -> bool:
    tasks = load()
    remaining = [t for t in tasks if t["id"] != task_id]
    if len(remaining) == len(tasks):
        return False
    save(remaining)
    return True


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="tasks", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("text", nargs="+")
    p_list = sub.add_parser("list", help="list tasks")
    p_list.add_argument("--all", action="store_true", help="include completed")
    sub.add_parser("done", help="complete a task").add_argument("id", type=int)
    sub.add_parser("rm", help="delete a task").add_argument("id", type=int)
    args = parser.parse_args(argv)

    if args.cmd == "add":
        t = add(" ".join(args.text))
        print(f"Added #{t['id']}: {t['text']}")
    elif args.cmd == "list":
        for t in load():
            if t["done"] and not args.all:
                continue
            print(f"[{'x' if t['done'] else ' '}] {t['id']:>3}  {t['text']}")
    elif args.cmd == "done":
        ok = mark_done(args.id)
        print("Done!" if ok else f"No task #{args.id}")
        return 0 if ok else 1
    elif args.cmd == "rm":
        ok = delete(args.id)
        print("Deleted." if ok else f"No task #{args.id}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
