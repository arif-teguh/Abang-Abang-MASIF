<div align="center">
	<h1>MASIF</h1>
	<p>Masif is an aplication to search and apply internship for Diskominfo Depok</p>
</div>

<div align="center">
![coverage](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2020/ppl-c/diskominfo-depok---masif/abang-abang-masif/badges/staging/coverage.svg?job=Test)
![build](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2020/ppl-c/diskominfo-depok---masif/abang-abang-masif/badges/staging/pipeline.svg)
![python](https://img.shields.io/pypi/pyversions/Django)
</div>

## Setup Development

1. **Install and Setup the Pyenv**

    For MacOs & Debian/Ubuntu users:
    
   ```shell
   # Install 
   $ brew install pyenv     # MacOS
   $ apt-get install pyenv  # Debian/Ubuntu
   
   # Setup Pyenv requirement
   # Depends on your system, you can change .zshrc to .bashrc or .bash_profile
   $ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc    
   $ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
   $ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc
   $ exec "$SHELL"
   
   # Install and Using Python 3.7.6
   $ pyenv install 3.7.6
   $ pyenv global 3.7.6
   
   ```
   
   For Windows users: Follow [this](https://github.com/pyenv-win/pyenv-win) steps
   
   If you found any problem, you can visit [pyenv](https://github.com/pyenv/pyenv) repo.

2. **Setup Pipenv**

   Setup Pipenv for easier virtual environment (venv) and package manager 

   ```shell
   # Install Pipenv
   $ pip install pipenv
   
   # Install all packages and creating virtual environment
   $ pipenv install
   
   ```

3. **Use the Virtual Environment**

   Start the virtual environment (venv):

   ```shell
   $ pipenv shell
   ```
   
   If you want to exit the virtual environment, use:
   
   ```shell
   $ deactivate
   ```
   
4. **Happy Developing!**
 
### Optional: Develop Using Docker

Make sure docker installed on your machine. Follow [this steps](https://docs.docker.com/install/) 
for docker installation
   
  ```shell
   # Start the application
   $ docker-compose up
   
   #Stop the aplication
   $ docker-compose down
   ```

For any troubleshoot you can visit [docker documentation](https://docs.docker.com/)


## Team Members
* 1706040012 - Arif Teguh Wangi
* 1706075041 - Kevin Raikhan Zain
* 1706074865 - Muhammad Azhar Rais Zulkarnain
* 1706075054 - Muhammad Feril Bagus Perkasa
* 1706074921 - Stefanus Khrisna Aji Hardiyanto