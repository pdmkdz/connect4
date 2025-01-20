# Connect 4 in PyQt5 by Michele Del Zoppo

Got as an assignment for a job interview, and trying to have some fun with the tools and skills I know, this project was completed in **~8h** of work.  
Using **PyQt5** and a full python application, 1 single BATCH file to run **[pyinstaller](https://pyinstaller.org/en/stable/index.html)**.  
Managing enviroment thru **conda**, all libraries are from open source channels [conda-forge]  
**[Miniforge3](https://conda-forge.org/miniforge/)** is recommended, but not essential for building this application.  
Icons where downloaded from the free tier of 

## How to setup environment:

1)  Create Enviroment:

`conda env create --file .\connect_env.yml`

2) Activate it

`conda activate connect_env`

3) Install package

`pip install -e .`

3) Run it

`python __main__.py` or un debug in VsCode as setup in .vscode folder

## DEBUG:

* For Debug this app could setup a debug mode in VsCode like I did, check the `.vscode` folder for the setup (should work on all machines [not tested on LINUX OS]).

## Packaging and usage:

* Pack it by running `installer.bat`, or simply copy paste the command stored in it in any terminal with working directory set for main repo folder.

* PLAY IT! The `.exe` from pyinstaller contains all needed pieces to play this game as is.

### Contacts:
If you want to contact me for questions or simply commenting or using this code for your own feel free to reach out thru [GIT](https://github.com/pdmkdz)

### GIT integration:
To be able to use Git on your local check the [tutorial](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup).

## Idea for future development:

* Create a real AI player where moves are not simply random (this was enough to let my 2 years old play it and enjoy it)

* Improve GUI to be looking more like a real Connect 4 board

* Improve the error handling after longer testing, I was not really pushing to have something perfect, just needed to complete the assignment and have fun with it showcasing some of my coding skills.