function neutron_classifier_configure_common {
    _neutron_service_plugin_class_add $NEUTRON_CLASSIFIER_PLUGIN
}

if [[ "$1" == "stack" && "$2" == "install" ]]; then
    setup_develop $NEUTRON_CLASSIFIER_DIR

elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
    echo_summary "Configuring neutron-classifier"
    neutron_classifier_configure_common
fi
