



# browser_automation
  
Module to perform web actions using the browser extension  

*Read this in other languages: [English](Manual_browser_automation.md), [Português](Manual_browser_automation.pr.md), [Español](Manual_browser_automation.es.md)*
  
![banner](imgs/Banner_browser_automation.png o jpg)
## How to install this module
  
To install the module in Rocketbot Studio, it can be done in two ways:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The folder name must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh your browser to be able to use the new module.
2. Automatic: When entering Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, search for the desired module and press install.  


## Description of the commands

### Open Browser
  
Open a selected browser
|Parameters|Description|example|
| --- | --- | --- |
|Browser |Browser you want to use.||
|URL|URL where to go.|https://rocketbot.com/en|
|Select a Folder|Profile forlder (leave empty to use default rocketbot folder for testing).|Path to folder|
|Port (Optional)|Port to open Chrome debugger|5002|
|Search free port (Optional)||checkbox|

### Close Browser
  
Close a selected browser
|Parameters|Description|example|
| --- | --- | --- |
