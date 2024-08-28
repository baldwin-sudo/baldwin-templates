
install_env (){
    conda deactivate ;              # exist current/default environement  (base) !
    
    conda create --name rag_env     # the conda environement is called rag_env .you may change it if yo u want !
    
    conda activate rag_env
    conda install pip python==3.9   #python 3.9 is required for this version of code and dependencies .

    conda install pip 
    pip install -r requirements.txt # install python dependencies

    echo "************************"
    echo "***env setup finished***"
    echo "************************" 
    }


conda --version ;

if [[ $? == 0 ]]; then
    install_env
else 
    echo " You need to install conda first ... "
    echo " check the README.md  for more info !"
    fi