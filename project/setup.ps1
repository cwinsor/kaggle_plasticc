################################################
# activate the virtual environment
# if the venv does not exist - create it

if (-NOT (Test-Path '.\venv\Scripts\activate' -PathType Leaf)) {

    " "
    "did not find venv\Scripts\activate - creating now..."

    # confirm at least we have python with pip
    python --version
    python -m pip --version

    # add venv to global libraries
    # python -m pip install venv

    # create an empty virtualenv
    python -m venv venv
    }

# activate the venv
.\venv\Scripts\activate

# get the libraries specified in requirements.txt
pip install -r requirements.txt



################################################
# add current directory to PATH (so libraries can be found)

$Env:PYTHONPATH=$ENV:PYTHONPATH + $PSScriptRoot
$Env:PYTHONPATH=$ENV:PYTHONPATH + ';'

$Env:PYTHONPATH=$ENV:PYTHONPATH + $PSScriptRoot
$Env:PYTHONPATH=$ENV:PYTHONPATH + '/lib;'


#################################################
# start vs-code
" "
"to start visual studio code:"
"code -n ."

#################################################
# start vs-code
" "
"to start jupyter notebook:"
"jupyter notebook"
