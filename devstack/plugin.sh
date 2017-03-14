function neutron_classifier_configure_common {
    _neutron_service_plugin_class_add $NEUTRON_CLASSIFIER_PLUGIN
    iniset /$Q_PLUGIN_CONF_FILE agent extensions "neutron-classifier"
    iniset $NEUTRON_CONF DEFAULT service_plugins $Q_SERVICE_PLUGIN_CLASSES
}

if [[ "$1" == "stack" && "$2" == "install" ]]; then
    setup_develop $NEUTRON_CLASSIFIER_DIR

elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
    echo_summary "Configuring neutron-classifier"
    neutron_classifier_configure_common
fi
