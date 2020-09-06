# (WIP) API Portugal Cinema

📽️ API for Portuguese Cinemas with the current movies in exhibition (even tho it's just a JSON file).

Contains information of the current week's movies in Portugal theaters. The cinema timetable is updated on thursday, so the file only contains information until the next wednesday (or until today, if the current day is wednesday).

---

## Content from:
- [x] Cinemas NOS
- [ ] UCI
- [ ] Castello Lopes
- [ ] Cinema City
- [ ] Other Cinemas
- [ ] Sapo Mag Timetables

## Work plan:
- [x] Scrape Cinemas NOS website
- [ ] Scrape other cinemas websites
- [ ] Automatically rerun script to scrape the information
  - [ ] Rerun every Thursday (day of new content and timetables update in Portugal)
  - [ ] Rerun on commit
  - [ ] Manually trigger reruns
- [ ] Scraping error detection
- [ ] Github Pages to present project and access "api" (JSON file)


---

### Execute scripts:
#### Requirements:
- [Python 3.8](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)

    - Install/Upgrade Windows: 
  
      `py -m pip install --upgrade pip`

    - Install/Upgrade Linux and macOS: 
  
      `python3 -m pip install --user --upgrade pip`

#### Setup virtualenv and install required python packages:
- Windows:
  
  ```
  py -m pip install --user virtualenv
  py -m venv env
  .\env\Scripts\activate
  pip install -r requirements.txt
  deactivate
  ```

- Linux and macOS:
  
  ```
  python3 -m pip install --user virtualenv
  python3 -m venv env
  source env/bin/activate
  pip install -r requirements.txt
  deactivate
  ```

#### Running:

- Windows:
  
  ```
  .\env\Scripts\activate
  py movies_scraper.py
  deactivate
  ```

- Linux and macOS:
  
  ```
  source env/bin/activate
  python3 movies_scraper.py
  deactivate
  ```
