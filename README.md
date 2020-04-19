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

### Develop Using Docker

Make sure docker installed on your machine. Follow [this steps](https://docs.docker.com/install/) 
for docker installation
   
  ```shell
   # Reset migration for new Device, skip this if you've run this app before
   find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
   find . -path "*/migrations/*.pyc"  -delete
   docker-compose run web python manage.py makemigrations
   docker-compose run web python manage.py migrate
   
   # Create superuser account
   # You can user this superuser account to open django admin after you've start the app
   # django admin url is 'localhost:8000/superuser'
   docker-compose run web python manage.py createsuperuser
   
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