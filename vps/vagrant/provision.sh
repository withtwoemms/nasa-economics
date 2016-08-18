#echo 'deb http://ftp.debian.org/debian sid main' | sudo tee -a /etc/apt/sources.list

#sudo touch /etc/apt/preferences.d/pinning
#cat << EOF | sudo tee -a /etc/apt/preferences.d/pinning
#Package: *
#Pin: release a=stable
#Pin-Priority: 700
 
#Package: *
#Pin: release a=testing
#Pin-Priority: 650
 
#Package: *
#Pin: release a=unstable
#Pin-Priority: 600
#EOF

#cd opt
#wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
#tar xzf Python-3.4.3.tgz

#cd Python-3.4.3
#./configure
#make
#sudo make install

#sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get -y update

#Flask Setup
sudo apt-get -y install python3.4-dev python-virtualenv git libevent-dev
pip install --upgrade distribute
mkdir /var/www
mkdir /var/www/nasanomics

/bin/bash -c "rsync -av \
    --exclude='/vagrant/nasanomics/vps/packer' \
    --exclude='/vagrant/nasanomics/vps/vagrant' \
    /vagrant/nasanomics/ /var/www/nasanomics"

# Setup dependencies
cd /var/www/nasanomics
make venv
source /var/www/nasanomics/venv/bin/activate
make install

# UWSGI Setup
sudo apt-get -y install uwsgi uwsgi-plugin-python
mkdir /var/www/run
chown www-data:www-data /var/www/run
touch /var/log/uwsgi/emperor.log
chown www-data:www-data /var/log/uwsgi/emperor.log
touch /var/log/uwsgi/app/nasanomics.log
chown www-data:www-data /var/log/uwsgi/app/nasanomics.log
cp /vagrant/nasanomics/vps/vagrant/uwsgi.conf /etc/init
cp /vagrant/nasanomics/vps/vagrant/uwsgi_config.ini /etc/uwsgi/apps-available/
ln -s /etc/uwsgi/apps-available/uwsgi_config.ini /etc/uwsgi/apps-enabled

# NGINX Setup
sudo apt-get -y install nginx
rm /etc/nginx/sites-enabled/default
cp /vagrant/nginx_config /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/nginx_config /etc/nginx/sites-enabled

# Start UWSGI and NGINX
service nginx restart
service uwsgi restart
