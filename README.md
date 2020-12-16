<div class="head">
  <h3 align="center">
    <a href="https://github.com/Cloud11665/sabat.dev#----------------">
      <img src="https://raw.githubusercontent.com/Cloud11665/sabat.dev/master/images/head.png" height="120px" alt="SABAT.DEV >>">
    <p>&nbsp;</p>
   </h3>
  <p align="center">
    <a href="https://sabat.dev" target="_blank">
      <img src="https://img.shields.io/website?down_color=critical&down_message=offline&logo=icloud&logoColor=ffffff&up_color=45966e&up_message=online&url=https%3A%2F%2Fsabat.dev" alt="website status">
    </a>
    <a href="https://github.com/Cloud11665/sabat.dev/actions?query=workflow%3Abuild">
      <img src="https://img.shields.io/github/workflow/status/Cloud11665/sabat.dev/build?color=%2345966e&label=build&logo=python&logoColor=ffffff" alt="build status">
    </a>
    <a href="https://github.com/Cloud11665/sabat.dev/actions?query=workflow%3AAPI">
      <img src="https://img.shields.io/github/workflow/status/Cloud11665/sabat.dev/test?color=%2345966e&label=API&logo=flask" alt="api status">
    </a>
  </p>
  <h2></h2>
    <h3>
      <p align="center">
        <a href="https://github.com/Cloud11665/sabat.dev#installation">[Installation]</a>
        &nbsp;
        <a href="https://github.com/Cloud11665/sabat.dev#deployment">[Deployment]</a>
        &nbsp;
        <a href="https://github.com/Cloud11665/sabat.dev#testing">[Testing]</a>
        &nbsp;
        <a href="https://github.com/Cloud11665/sabat.dev/blob/master/api/README.md">[API documentation]</a>
        &nbsp;
        <a href="https://github.com/Cloud11665/sabat.dev/blob/master/LICENSE">[License]</a>
        &nbsp;
        <a href="https://github.com/Cloud11665/sabat.dev#contributing">[Contributing]</a>
      </p>
    </h3>
  <h2></h2>
  <p>&nbsp;</p>
  <p align="center">
    <strong>
      My personal website for hosting my projects <i>(mostly API's)</i> and messing with front-end
    </strong>
  </p>
  <p>&nbsp;</p>
</div>
<!--Markdown only from now on ((`with some exceptions`))-->
<!--
<p align="center">
  <a href="https://github.com/Cloud11665/sabat.dev/tree/master/api">
    <img src="https://img.shields.io/badge/API%20version-1.1-informational">
  </a>
  <a href="https://github.com/Cloud11665/sabat.dev/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Cloud11665/sabat.dev">
  </a>
  <a href="https://www.codefactor.io/repository/github/cloud11665/sabat.dev">
    <img src="https://img.shields.io/codefactor/grade/github/Cloud11665/sabat.dev">
  </a>
  <a href="https://github.com/Cloud11665/sabat.dev/blob/master/Pipfile.lock">
    <img src="https://img.shields.io/github/pipenv/locked/python-version/Cloud11665/sabat.dev">
  </a>
</p>
## Installation
Standard python
```
git clone https://github.com/Cloud11665/sabat.dev
cd ./sabat.dev
python -m pip install -r ./requirements.txt
```
Pipenv
```
git clone https://github.com/Cloud11665/sabat.dev
cd ./sabat.dev
pipenv install
```
&nbsp;  
&nbsp;   
## Deployment
I use nginx, listening to port 5000 and gunicorn to serve the app.  
&nbsp;  
When running on something like [GNU screen](https://www.gnu.org/software/screen) or [tmux](https://github.com/tmux/tmux).
```
python -m gunicorn --bind 127.0.0.1:5000 wsgi:app
```
When running in the background.
```
nohup python -m gunicorn --bind 127.0.0.1:5000 wsgi:app </dev/null >/dev/null 2>&1&
```
&nbsp;  
&nbsp;  
## Testing
Run the whole API test suite. *(Requires the http server to be running on localhost)*
```
pytest ./tests/*.py
```
&nbsp;  
&nbsp;  
## Contributing
-->
