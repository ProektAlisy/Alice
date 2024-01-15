TRANSITIONS = [
    {
        "trigger": "trigger_info_about_center",
        "source": "start",
        "dest": "start",
        "before": "get_info_about_center",
        "after": "_save_state",
    },
    {
        "trigger": "trigger_info_about_center_personal",
        "source": "start",
        "dest": "start",
        "before": "get_info_about_center_personal",
        "after": "_save_state",
    },
    {
        "trigger": "trigger_help",
        "source": "*",
        "dest": "help",
        "before": "get_help",
    },
    {
        "trigger": "trigger_help_phrase",
        "source": "help",
        "dest": "help",
        "before": "get_help_phrase",
    },
    {
        "trigger": "trigger_help_navigation",
        "source": "help",
        "dest": "help",
        "before": "get_help_navigation",
    },
    {
        "trigger": "from_help",
        "source": "help",
        "dest": "=",
        "before": "get_help_exit",
        "after": "_return_to_original_state",
    },
    {
        "trigger": "trigger_services_for_blind",
        "source": "start",
        "dest": "services_for_blind",
        "before": "get_services_for_blind",
        "after": "_save_state",
    },
]
