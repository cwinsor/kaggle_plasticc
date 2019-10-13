
# create an empty virtualenv and activate
python -m pip install virtualenv
python -m virtualenv pymote_env --no-site-packages
.\pymote_env\Scripts\activate

# get the packages
pip install --find-links=pymote_wheelhouse -r requirements.txt
