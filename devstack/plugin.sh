if [[ "$1" == "stack" && "$2" == "install" ]]; then
    setup_develop $NEUTRON_CLASSIFIER_DIR

elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
    echo_summary "Configuring neutron-classifier"
fi
