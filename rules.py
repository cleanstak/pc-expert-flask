CATEGORIES = [
    {"id": "cat_power", "label": "Power & Booting Issues", "icon": "🔌"},
    {"id": "cat_display", "label": "Display & Screen Issues", "icon": "🖥️"},
    {"id": "cat_performance", "label": "Performance & Slowdown", "icon": "⚡"},
    {"id": "cat_network", "label": "Network & Internet Connection", "icon": "🌐"},
    {"id": "cat_storage", "label": "Storage & Hard Drive Errors", "icon": "💾"}
]

DIAGNOSTIC_TREES = {
    "cat_power": {
        "start_node": "q1_power",
        "nodes": {
            "q1_power": {
                "question": "Does the power light turn on when you press the power button?",
                "subtext": "Check for any LED activity or fan spin inside the computer case.",
                "yes": "q2_fans",
                "no": "diag_psu_failure"
            },
            "q2_fans": {
                "question": "Do the cooling fans spin continuously without turning off?",
                "subtext": "Listen closely to the air vents or look through the casing grid.",
                "yes": "diag_ram_issue",
                "no": "diag_motherboard_short"
            }
        }
    },
    "cat_display": {
        "start_node": "q1_display",
        "nodes": {
            "q1_display": {
                "question": "Is the screen completely black with no backlight?",
                "subtext": "Check if the power indicator on the monitor is lit.",
                "yes": "diag_monitor_cable",
                "no": "q2_glitch"
            },
            "q2_glitch": {
                "question": "Are there lines, flickering, or distorted colors on display?",
                "subtext": "Look for horizontal/vertical lines or rainbow patterns.",
                "yes": "diag_gpu_fault",
                "no": "diag_resolution_setting"
            }
        }
    }
}

DIAGNOSES = {
    "diag_psu_failure": {
        "title": "Power Supply Unit (PSU) or Adapter Failure",
        "description": "The system receives zero electrical power. This indicates an unplugged cable, faulty power adapter, or blown power supply unit.",
        "action": "Check the wall outlet, test with another power adapter, or replace the internal Power Supply Unit (PSU)."
    },
    "diag_ram_issue": {
        "title": "RAM / Memory Contact Fault",
        "description": "The system powers on but fails to post or display video output. This typically indicates loose or oxidized RAM contact pins.",
        "action": "Unplug power, open the computer case, remove the RAM sticks, clean the gold contacts with an eraser, and re-seat them firmly."
    },
    "diag_motherboard_short": {
        "title": "Motherboard or Internal Short Circuit",
        "description": "The system starts briefly and immediately shuts down or cuts power.",
        "action": "Disconnect external peripherals and test with bare-minimum components (1 stick of RAM, CPU, power supply)."
    },
    "diag_monitor_cable": {
        "title": "Loose Video Cable or Monitor Power Disconnected",
        "description": "The PC turns on normally, but no image reaches the display monitor.",
        "action": "Ensure the HDMI/DisplayPort cable is plugged firmly into the dedicated GPU output (not the motherboard port)."
    },
    "diag_gpu_fault": {
        "title": "Graphics Processing Unit (GPU) Driver / Hardware Issue",
        "description": "Visual artifacts, flickering, or distorted colors indicate video memory or driver corruption.",
        "action": "Boot into Safe Mode, reinstall display drivers using DDU, or test with another graphics card."
    },
    "diag_resolution_setting": {
        "title": "Unsupported Display Resolution / Refresh Rate",
        "description": "The monitor goes out of range due to misconfigured operating system settings.",
        "action": "Restart in Low-Resolution Video Mode and set the display resolution to native defaults."
    }
}