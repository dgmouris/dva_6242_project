---
layout: cover
theme: seriph
background: /images/hockey_shot.jpg

title: Evaluating the Effectiveness of a Player and Unit of Players on the Ice and Finding Unit Comparables Based on Various NHL Shot Metrics

class: text-center
transition: slide-left
configs:
  footer: "Team 117: Daniel Mouris, Dylan Riggs, Kaiyu Chen, Toshan Doodnauth, & Tyler Stephenson"
---

# Evaluating the Effectiveness of a Player and Unit of Players on the Ice and Finding Unit Comparables Based on Various NHL Shot Metrics

Built with my project team at Georgia Tech.

---

# Overview

### - Demo
### - What we tried to do
### - Why are you doing this?
### - How is it done and What are the limits?
### - Whats our new Approach?
### - What's the stack?
### - Where and how was it Deployed?
### - What was the process in building it?
### - What would I do with more time?
### - Conclusions

---
layout: intro
---

# Demo
<br/>

## Go check it out here: https://dva-6242-project.vercel.app/
- Note: doesn't look great on mobile.
- Please wait until after the talk to do so, for speed sake.

<br/>

## Repo and questions
- Repo: https://github.com/dgmouris/dva_6242_project/
  - Note: a few shortcuts were taken in the interest of speed and this was more of a proof of concept.
- if you have any questions please @dgmouris me on the slack.

---

# What we tried to do

1. Web app to search players and NHL Player On Ice Units (POIU)
   - Retrieves most common POIU for that player.
2. Compares POIU as a whole to
   - The player searched for
   - Comparable/Similar POIUs across the league to the POIU searched for.
3. Create Visualization to Display
   - similar poius as a network
   - offensive shots are taken
   - defensive shots are conceded
   - offensive shot volume

---

# Why are you doing this?

1. I wanted to learn more about d3.js and data visualization as a whole
2. I wanted build an end to end visualization project performing all steps required to build an analytics site.
   1. Data ingestion
   2. Backend REST API
   3. Frontend App
   4. Using AI (not llms) to get similarities between things
   5. D3.js
   6. Deployment
3. My 12 year old self loves hockey stats, I understand the domain, and I didn't want to build a project on boring stats I didn't care about.

---
layout: intro
---

# How is it done currently and What are the limitations?
<br/>

## Current approach focus on player, team, lines that are either forward or defensemen

<br/>

## Limatations are that it doesn't focus on the entire player on ice unit as a whole.


---
layout: intro
---

# Whats new in our Approach?
<br/>

## Visualizing the data for an entire POIU.
<br/>

## Creating a similarity Metric for POIUs and finding comparables across the league
---

# What's the Stack?

## Backend
1. Flask for the API
2. SQLAlchemy (with Postgres) for the backend
3. Pandas, Scikit-learn and jupyter for the similarity algo

## Frontend
1. D3.js
2. React with Next.js, and shadcn for ui components
3. React Query for all of the data fetching
---

# Where and how was it Deployed?

## Backend
1. VPS (Droplet) Ubuntu 24.10
   1. Nginx and Gunicorn.
2. Managed Database
   1. Postgres 15

Note: this was all deployed on DigitalOcean

## Frontend
1. Vercel

<br>
<br>
<br>
<br>
PS. if you're a student use your sweet free digital ocean credits.
---

# What was the process in building it?

1. Come up with a static UI that looks janky (excalidraw for those who have seen my art).
2. Find sources for all the data needed (moneypuck.com, unofficial NHL api)
3. Come up with a schema for the database and build the first pass of the SQLAlchemy models needed.
4. Begin the process of ingesting data.
   1. Ingest all of the shots first.
   2. all of the player shifts reconcile shot and shift data to each POIU.
5. Create a CSV for scikit learn to analyze data and cluster the POIUs for similarity.
   1. Do the analysis with Precision@K, PCA, Silhouette scores, K Nearest Neighbours (KNN) and KMeans export to csv and then load that csv data in a similarity table.
6. Create the API to search and the frontend part to visualize the data side by side.
7. iterate on the following for each chart
   1. mock up a visualization you'd like to see.
   2. Create the backend api endpoint you're going to need (create tables if needed)
   3. Create the component (poiu id as a prop) that fetches the data and creates the d3.js visualization.

---

# What would we do with more time?

1. Fix and refactor general Jank in the codebase, we only had two months so is was rushed.
2. Make it so that we could replace a player and find comparable lines on the fly.
   1. This was one of the first original idea so that we could evaluate how a potential line would work
   2. Make the AI piece work on the fly.
3. Injest and process since 2008 (so there's more POIUs) and you can compare it historically.
   1. we currently only have the data for the year 2023-24.
4. Make the frontend more mobile friendly and a bit clearer, fix up general bugs that I didn't have time to fix.

---
# Conclusions

- I think this was pretty cool and passes the interesting test (for myself at least).
- Is valuable or useful?
  - I'm not sure yet but I think the data is more useful for powerplay and penalty kill.
- Will I build more of this?
  - I'm not sure but it would have been more fun if I wasn't trying to do so many things at once during the semester.
- I learned a ton, which is great.
- If you want to read the report if you're interested (or if you want to go to sleep) send me a message on the slack.
- If you know someone at puckpedia let me know as I think some of this could be a cool visualization on their site.
