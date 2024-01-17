TRANSITIONS = [
    {
        "trigger": "trigger_training_center",
        "source": "start",
        "dest": "=",
        "before": "get_training_center",
    },
    {
        "trigger": "trigger_staff",
        "source": "start",
        "dest": "=",
        "before": "get_staff",
    },
    {
        "trigger": "trigger_services_for_blind",
        "source": "start",
        "dest": "services_for_blind",
        "before": "get_services_for_blind",
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
]
