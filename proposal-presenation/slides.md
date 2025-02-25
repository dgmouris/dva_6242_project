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

Team 117: Daniel Mouris, Dylan Riggs, Kaiyu Chen, Toshan Doodnauth, & Tyler Stephenson


---

# Overview of Proposal

### - What are we trying to do?
### - How is it done and What are the limits?
### - Whats our new Approach, and if successful what are the innovations?
### - Who Cares about this application?
### - What are the Risks, Payoffs and Potential Impact?
### - What is the Cost, Time and how will be checking for success?

<!-- Add to bottom of all slides -->
<div class="absolute bottom-4 right-4 text-sm opacity-70">
  Team 117: Daniel Mouris, Dylan Riggs, Kaiyu Chen, Toshan Doodnauth, & Tyler Stephenson
</div>
---

# What are we trying to do

1. Web app to search players and NHL Player On Ice Units (POIU)
   - Retrieves most common POIU for that player.
2. Compares POIU as a whole to
   - The player searched for
   - Comparable/Similar POIUs across the league
3. Create Visulation to Display
   - offensive shots are taken
   - defensive shots are conceded
   - Shot metrics: SAT for and against, shot distance, type of shot
<!-- Add to bottom of all slides -->
<div class="absolute bottom-4 right-4 text-sm opacity-70">
  Team 117: Daniel Mouris, Dylan Riggs, Kaiyu Chen, Toshan Doodnauth, & Tyler Stephenson
</div>
---
layout: intro
---

# How is it done currently and What are the limitations?
<br/>

## Current approach focus on player, team, lines that are either forward or defensemen

<br/>

## Limatations are that it doesn't focus on the entire player on ice unit as a whole.

<!-- Add to bottom of all slides -->
<div class="absolute bottom-4 right-4 text-sm opacity-70">
  Team 117: Daniel Mouris, Dylan Riggs, Kaiyu Chen, Toshan Doodnauth, & Tyler Stephenson
</div>
---
layout: intro
---

# Whats new in our Approach?
<br/>

## Visualizing the data for an entire POIU.
<br/>

## Creating a similarity Metric for POIUs and finding comparables across the league

<br/>

## Injecting a player from a different team on a POIU and predicting how the line would perform (time permitting)

<!-- Add to bottom of all slides -->
<div class="absolute bottom-4 right-4 text-sm opacity-70">
  Team 117: Daniel Mouris, Dylan Riggs, Kaiyu Chen, Toshan Doodnauth, & Tyler Stephenson
</div>
---
layout: intro
---

# Who Cares?
<br/>

## - Fans
<br/>

## - NHL Team Staff
<br/>

## - Analytics Organizations
<br/>

## - NHL Team Staff
<br/>
<!-- Add to bottom of all slides -->
<div class="absolute bottom-4 right-4 text-sm opacity-70">
  Team 117: Daniel Mouris, Dylan Riggs, Kaiyu Chen, Toshan Doodnauth, & Tyler Stephenson
</div>

---
layout: two-cols-header
---
# What are the Payoffs and Risks?

::left::
# Payoffs

- Novel Visualizations to compare POIUs
- Get a way to visualize the effect of players on shots who play well together.

::right::
# Risks

- scope might be to large, might have to pair it down.
- our comparison model might have some unknown biases/uncertainties since different teams have different strategies


<!-- https://www.vectorstock.com/royalty-free-vector/ice-hockey-rink-isolated-vector-27143243 -->
<!-- Add to bottom of all slides -->
<div class="absolute bottom-4 right-4 text-sm opacity-70">
  Team 117: Daniel Mouris, Dylan Riggs, Kaiyu Chen, Toshan Doodnauth, & Tyler Stephenson
</div>
---

<h1>Cost,  Time and Checks for Success</h1>
<div class="flex space-x-6 h100">
  <div class="w-1/4">
    Cost
    <ul>
        <li>Free until we run of resources for AWS or a cloud provider</li>
    </ul>
    <br/>
    Time and Check points
    <ul>
        <li>Mid checkpoint (1 month): model to find comparable POIU</li>
        <li>Final checkpoint (2 month total): Fully searchable web app that visualizes and compares</li>
    </ul>

  </div>
  <div class="w-3/4 bg-cover bg-center" style="background-image: url('/images/gantt-chart.png');">

  </div>
</div>
<!-- Add to bottom of all slides -->
<div class="absolute bottom-4 right-4 text-sm opacity-70">
  Team 117: Daniel Mouris, Dylan Riggs, Kaiyu Chen, Toshan Doodnauth, & Tyler Stephenson
</div>