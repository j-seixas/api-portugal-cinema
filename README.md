# api-portugal-cinema

📽️ API for Portuguese Cinemas with the current movies in exhibition (even tho it's just a JSON file).

Contains information of the current week's movies in Portugal theaters. The cinema timetable is updated on thursday, so the file only contains information until the next wednesday (or until today, if the current day is wednesday).

### Content from:
- [x] Cinemas NOS
- [ ] UCI
- [ ] Castello Lopes
- [ ] Cinema City
- [ ] Other Cinemas

### Work plan:
- [x] Scrape Cinemas NOS website
- [ ] Scrape other cinemas websites
- [ ] Automatically rerun script to scrape the information
  - [ ] Rerun every Thursday (day of new content and timetables update in Portugal)
  - [ ] Rerun on commit
  - [ ] Manually trigger reruns
- [ ] Scraping error detection
- [ ] Github Pages to present project and access "api" (JSON file)

