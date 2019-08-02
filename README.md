### **Seele One Button Mining**

Seele One Button Mining is a utility that helps with setting up Seele mining process.  It provides a GUI for the Seele command line based tools. 

### How to Build

Building the executable is pretty straight forward.  The current released version is build with Python 3.7 and PyInstaller.  Please read the documentation on how to generate a Windows executable from a python script using PyInstaller.

Here's the command that's use to build the Seele One Button Mining on Windows:

pyinstaller --onefile -wF --clean --name smc --icon=seele.ico main.py 

The executable is in the dist directory.  The tool must be run in Administrator mode for it to interact the mining services. 

### Contribution

Thank you for considering helping out with our source code. We appreciate any contributions, even the smallest fixes.

* Pull requests need to be based on and opened against the `master` branch.
* We use reviewable.io as our review tool for any pull request. Please submit and follow up on your comments in this tool. After you submit a PR, there will be a `Reviewable` button in your PR. Click this button, it will take you to the review page (it may ask you to login).
* If you have any questions, feel free to join [chat room](https://gitter.im/seeleteamchat/dev) to communicate with our core team.

### License

[go-seele/LICENSE](https://github.com/seeleteam/go-seele/blob/master/LICENSE)