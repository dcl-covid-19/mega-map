# Start Here If You're New!

Hello and welcome! In this folder, we'll establish some general practices and tips for making new projects in this repository. We'll assume that we have a little knowledge of how to use Git and Terminal/Command Line (but it's okay if that's not the case -- we can visit the resources at the end of the README). When (not if) you have questions, please message the #bac-data-engineering Slack channel! 


## Philosophies
* We want to design and document our project so that anyone with some technical familiarity should understand what our project does and how to run or even pick up our project.
    * There's a saying in software that code we wrote six months ago basically looks completely new to us -- that means we want to write good notes!
* We ought to store ways to reproduce data, not the actual data. Data files tend to be large, and their contents get outdated more often than code does! (Imagine if we're scraping information daily.)


## General Workflow 
A way we design a project might be:
* Get an idea (genius, weird, half-formed, or otherwise)
* Make sure we've `git pull`ed recently, then checkout a new branch
* Make a new directory/folder locally, from the repository root directory (`mega-map`), with a README file
    * The contents of the README are displayed on Github whenever we're inside the directory i.e. we're inside a README file right now! Trippy. More details on this later.
* Write our code or notebook, making sure to `git commit` often, until we reach a good stopping point
* Clean, reformat, and comment our work, and update the README file accordingly
* `git push` our branch, so our changes are reflected in a branch remotely (i.e. in Github, not just our computer!)
* Make a pull request and possibly ask others to review our changes!
* Merge our changes! We've done good. We can always update our project later by making a new local branch, writing more changes, and then pushing again.


## README
The README is the first file that someone looks at in a repository or project, so in it, we want to orient the reader. That means we want to include the following information:

### Summary
What's the purpose of our project? Are we trying to scrape Google Maps? Or are we analyzing USDA food insecurity data? Or are we mining Bitcoin? (Let's not do that.) This can be reasonably high level.

### Requirements
We generally need to have external tools or software libraries to make our code work! The idea of this section is "how would I tell someone to setup if they just bought their computer?". Are we using Python (2 or 3?), R, HTML/CSS, or something else? 

If we're using Python, for instance, we want to say how to install all the libraries we need, say:
```
pip install numpy pandas matplotlib jupyter plotly
```
or, if we're feeling fancy, we can make a `requirements.txt` file and instead instruct the reader to run:
```
pip install -r requirements.txt
```

If we're using R, should we be using RStudio? Do we need any external plugins, such as for OSRM for transportation info?


### Setup and Running the Project
This flows from the Requirements section, and here, we should think "how would someone run our project given they have the right environment?". Let's be precise and list out all the steps here! We might say:
* Navigate to this directory:
```
cd tutorial
```
* Then run
```
python driver.py --output-file data.json
```
which should output a JSON file.
* Inspect `data.json` for any obvious mistakes, then upload `data.json` to the shared Google Drive at `UnBox/Scraping/Outputs`.

Maybe if we had an R notebook instead, we'd say:
* Open the notebook in RStudio
* Run all the cells in a row, then look at the visualizations of online SNAP coverage

### Other Notes
We might explain how we've designed this project. For instance, we could explain that `driver.py` is just a driver file, and it first calls the Google Maps scraping code in `web_scrapers.py`, then calls the data processing code in `etl.py`, then translates the information into Spanish by default by calling `translators.py`.


## Technical Resources
* Terminal/Command Line/Linux
    * Here's a common command [cheatsheet](https://www.hostinger.com/tutorials/linux-commands)
    * We might find an interactive course, such as from [Codecademy](https://www.codecademy.com/learn/learn-the-command-line), helpful if we're less familiar with this tool.
* Git
    * Here's a good [summary](https://rogerdudler.github.io/git-guide/) of using Git in Terminal/Command Line
    * Again, if this is our first time using Git, we could consider a more interactive course, such as from [Codecademy](https://www.codecademy.com/learn/learn-git)
* Markdown (good for writing `README.md` files)
    * Here's a [Markdown cheatsheet](https://www.markdownguide.org/cheat-sheet/)
* R 
    * The top of [Berkeley's D-Lab repository](https://github.com/dlab-berkeley/R-Fundamentals) has instructions for setting up an R environment (downloading R and RStudio)
    * Stanford's [Data Challenge Lab](https://dcl-docs.stanford.edu/home/) has some resources on project workflow and good practices through an R lens
    * Here are some example [coding practices](https://jadebc.github.io/lab-manual/coding-practices.html) in R that reflect the philosophies described below.
    * Here are some [statistical method examples](https://cehs-research.github.io/eBook_multilevel/gee-continuous-outcome-beat-the-blues.html) through an R lens



## TODOs and Personal Musings
* Decide whether non-main branches + PRs is the best approach, or if forking should be best practice
* Construct an extra README for the actual example project (maybe also a subdir)
* Possibly split off sections from the main README since it's getting kinda large
* Find a good Jupyter notebook tutorial
* Make a pretty diagram for explaining the general workflow
* add an example notebook with comments
* PR etiquette -- attach an example PR to this README (woah, inception)

