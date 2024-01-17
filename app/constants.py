TRANSITIONS = [
    {
        "trigger": "say_info_about_center",
        "source": "start",
        "dest": "info_center",
        "before": "get_info_about_center",
        "after": "_save_state",
    },
    {
        "trigger": "say_info_about_center_personal",
        "source": "start",
        "dest": "start",
        "before": "get_info_about_center_personal",
        "after": "_save_state",
    },
    {
        "trigger": "say_info",
        "source": "info_center",
        "dest": "start",
        "before": "get_info",
        "after": "_save_state",
    },
    {
        "trigger": "say_help",
        "source": "*",
        "dest": "help",
        "before": "get_help",
    },
    {
        "trigger": "say_help_phrase",
        "source": "help",
        "dest": "help",
        "before": "get_help_phrase",
    },
    {
        "trigger": "say_help_navigation",
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
