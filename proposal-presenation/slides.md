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


# How is it done currently and What are the limitations?

## Current approach focus on player, team, lines that are either forward or defensemen
- For focus on a player there's shot type [1], position and posture [2,3]
## Limitations are that it doesn't focus on the entire player on ice unit as a whole
- Team comparison corsi rating [4]
- Analysis of players together using play by play models and markov chains [5]

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

## - Journalists
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

- scope might be to large, might have to pare it down.
- our comparison model might have some unknown biases/uncertainties since different teams have different strategies[6]


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

---

# References
<ul class="text-sm">
    <li>[1] Barinberg, E. (2023). Evaluating how NHL player shot selection impacts even-strength goal output over the course of a full season (Master's thesis). Ramapo College of New Jersey.</li>
    <li>[2] Becker, Devan G., Douglas G. Woolford, and Charmaine B. Dean. "Algorithmically deconstructing shot locations as a method for shot quality in hockey." Journal of Quantitative Analysis in Sports 17.2 (2021): 107-115.</li>
    <li>[3] Hamzah, Adi Padli, et al. "Study of Body Attitude Criteria of Indoor Hockey Players Based on Body Height to Obtain Accurate Passing Techniques." International Journal of Multidisciplinary Research and Analysis 4.02 (2021): 137-141.</li>
    <li>[4] Goldfarb, Daniel. "An application of topological data analysis to hockey analytics." arXiv preprint arXiv:1409.7635 (2014)</li>
    <li>[5] Ljung, D., Carlsson, N., & Lambrix, P. (2019). Player pairs valuation in ice hockey. In Machine Learning and Data Mining for Sports Analytics: 5th International Workshop, MLSA 2018, Co-located with ECML/PKDD 2018, Dublin, Ireland, September 10, 2018, Proceedings 5 (pp. 82-92). Springer International Publishing</li>
    <li>[6] Snow, Kevin. The Science of Hockey: The Math, Technology, and Data Behind the Sport. Simon and Schuster, 2023.</li>
</ul>
