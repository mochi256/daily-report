#!/usr/bin/env python3
import os
import sys
import re
import subprocess
from datetime import datetime, timedelta

REPORT_DIR = os.environ['REPORT_DIR']
CURRENT_DATE = datetime.now()
CURRENT_DATE_STR = CURRENT_DATE.strftime("%Y-%m-%d")


if __name__ == "__main__":
    if not os.path.exists(REPORT_DIR):
        raise Exception("environ 'REPORT_DIR' is not found.")
    
    # 作成済みの日報の振り分け
    made_files = os.listdir(REPORT_DIR)
    for f in made_files:
        m = re.match(r'(\d{4})-(\d{2})-(\d{2})', f)
        if m is None:
            continue

        if f == "{0}.md".format(CURRENT_DATE_STR):
            continue
        
        target_dir = "{0}/{1}-{2}".format(
            REPORT_DIR, m.groups()[0], m.groups()[1]
        )
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        subprocess.run(["mv", "{0}/{1}".format(REPORT_DIR, f), target_dir])
    
    today_report = "{0}/{1}.md".format(REPORT_DIR, CURRENT_DATE_STR)
    if os.path.exists(today_report):
        subprocess.run(["open", today_report])
        sys.exit(0)

    # 過去の日報のコピー
    history = list(set([
        (CURRENT_DATE - timedelta(weeks=m)).strftime("%Y-%m") for m in range(12)
    ]))
    history.sort()
    for hist in history[::-1]:
        target_dir = "{0}/{1}".format(REPORT_DIR, hist)
        if not os.path.exists(target_dir):
            continue

        history_files = os.listdir(target_dir)
        mds = [
            f for f in history_files if re.match(r'\d{4}-\d{2}-\d{2}\.md', f)
        ]
        if len(mds) == 0:
            continue
        mds.sort()
        mds.reverse()
        target_file = "{0}/{1}".format(target_dir, mds[0])
        with open(target_file, "r") as fp:
            target_data = fp.read()
        
        schedule = re.findall(r'(?<=##\sNext\sSchedule\s\s).+', target_data, flags=re.DOTALL)[0]
        tasks = re.findall(r'(?<=##\sTasks\s\s).+?(?=\s{0,4}##)', target_data, flags=re.DOTALL)[0]

        template_path = "{0}/.template/template.md".format(REPORT_DIR)
        if not os.path.exists(template_path):
            raise Exception("file '{0}' is not found.".format(template_path))
        with open(template_path, "r") as fp:
            temp_data = fp.read()
        
        today_report = "{0}/{1}.md".format(REPORT_DIR, CURRENT_DATE_STR)
        with open(today_report, "w") as fq:
            fq.write(temp_data.format(CURRENT_DATE_STR, schedule, tasks))

        subprocess.run(["open", today_report])
        sys.exit(0)

    # 以前の日報が作成されていない場合
    basemd_path = "{0}/.template/base.md".format(REPORT_DIR)
    if not os.path.exists(basemd_path):
        raise Exception("file '{0}' is not found.".format(basemd_path))

    with open(basemd_path, "r") as fp:
        read_data = fp.read()

    today_report = "{0}/{1}.md".format(REPORT_DIR, CURRENT_DATE_STR)
    with open(today_report, "w") as fq:
        fq.write(read_data.format(CURRENT_DATE_STR))

    subprocess.run(["open", today_report])
