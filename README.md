## wuvt-site
This is the next-generation website for [WUVT-FM](https://www.wuvt.vt.edu), 
Virginia Tech's student radio station.

It has several main components:
- A Content Management System (CMS) to store both blog-style *articles* and 
  static *pages*. These can be managed at the `/admin` endpoint. One *admin*
  user capable of administrative access exists; all other users have full 
  control of articles and pages and may upload files. 
- **Trackman**, a track logger with a UI and an API compatible with both 
  WinAmp's POST plugin and [mpd-automation](https://github.com/wuvt/mpd-automation). 
  Upon track changes, metadata is sent to Icecast, TuneIn, and Last.fm. Logged 
  playlists are publicly available on the main website. 
- HTML5 stream player capable of smooth chained OGG playback in Webkit

### Development Environment Setup
Install redis and start the daemon. You'll need redis running whenever you want
to run the site, but it is not necessary to start it on boot.

It is recommended that you use a virtualenv for this so that you can better
separate dependencies:

```
mkdir -p ~/.local/share/virtualenv
virtualenv ~/.local/share/virtualenv/wuvt-site
source ~/.local/share/virtualenv/wuvt-site/bin/activate
```

Now, within this virtualenv, install the dependencies:

```
pip install -r requirements.txt
```

You'll also want to get gunicorn, which is used as a local web server:

```
pip install gunicorn
```

Next, clone the repo and make a copy of the config:

```
git clone https://github.com/wuvt/wuvt-site.git
cd wuvt-site
cp wuvt/config.py.example wuvt/config.py
```

Edit wuvt/config.py to match your desired config, then go ahead and create the
database and fill it with some sample content:

```
python2 create.py
python2 articles.py
```

Finally, start the celery worker and development web server:

```
./run_celery.sh &
./run_dev_server.sh
```

You can now access the site at http://127.0.0.1:8080/

### Production Environment Setup
Here are some example instructions to get you started. These are not complete,
so it's recommended to just use the Ansible playbook for this. 
- Install redis, start the daemon, and configure it to start at boot
- Run `sudo pip install -r requirements.txt` to install requirements
- Copy `wuvt/config.py.example` to `wuvt/config.py` and edit it to match your desired config
- Run `python2 create.py` to setup the website
- Run `python2 articles.py` to create some sample articles

(TODO: uwsgi setup)

Check-out [our ansible playbooks](https://github.com/wuvt/wuvt-ansible) for
example setup with Nginx.

Once set-up, you can visit:
- `/admin` to manage website content
- `/trackman` to enter tracks

### API
TODO

Look at submit_track.sh for an example of sending metadata to Trackman.


### License

Besides the exceptions noted below, the entirety of this software is available
under the GNU Affero General Public License:

```
Copyright 2012-2015 James Schwinabart, Calvin Winkowski, Matt Hazinski.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```

The following files are JavaScript libraries, freely available under the MIT
license as noted in their headers:
* wuvt/static/js/jquery.js
* wuvt/static/js/jquery-ui.min.js
* wuvt/static/js/moment.min.js

The following font file was designed by Humberto Gregorio and is in the public
domain:
* wuvt/static/fonts/sohoma_extrabold.woff

Other included fonts (in wuvt/static/fonts) are not covered under this license.
