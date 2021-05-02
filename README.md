# vaxget
Automatically fills in the RegionH leftover vaccine form questionnaire (SurveyXact) using python and selenium webdriver. For an arbitrary amount of people.

---

Requires:
---

Selenium server with chrome running. This code is meant for use with the containerized version from dockerhub.

Setup:
---

Put vaxget.py and vaxlist.yaml in the same folder.
Edit absolute paths in vaxget.py.
add something like the following to your crontab: ```30 9 * * * /home/pi/covid19-autofill/vaxget.py >> ~/covid19-autofill/cron.log 2>&1```
