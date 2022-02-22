# PI Car Shakedown script

## To install

first clone the repository
```
git clone https://github.com/aradford123/pi-shakedown.git
```

Next change directory.
```
cd pi-shakedown/
```

Now run the install script.  This will setup a virtual environment, install some requirements and copy the sample webex_config.py file

```
./install.sh 
```

Next you need to activate the virtual environement (as instructed)
```
source env3/bin/activate
```

And finally, edit the webex_config.py file to include token and the roomID

Once you have done this, you can run the script in two ways:

The first will just test the script and capture the images, without posting to the webex teams space.
```
./shakedown.py 
```

The second is with the --post option.  This will post the images and video to webex teams
```
./shakedown.py --post
```
