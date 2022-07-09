# daily-report
make to daily report.

# usage
```bash
git clone git@github.com:mochi256/daily-report.git $HOME/.daily-report
mkdir -p ~/.local/bin
export PATH=$PATH:$HOME/.local/bin
mv $HOME/.daily-report/report.py $HOME/.local/bin/report

mkdir $HOME/report
export REPORT_DIR=$HOME/report

report
```
