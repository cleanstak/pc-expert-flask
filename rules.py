# rules.py

CATEGORIES = [
    {"id": "cat_power", "label": "Computer won't turn on", "icon": "⚡"},
    {"id": "cat_heat", "label": "Computer is overheating", "icon": "♨️"},
    {"id": "cat_net", "label": "No internet connection", "icon": "🌐"},
    {"id": "cat_slow", "label": "Computer is running slowly", "icon": "⏱️"},
    {"id": "cat_audio", "label": "No sound", "icon": "🔊"}
]

DIAGNOSTIC_TREES = {
    # 1. Power & Booting Issues
    "cat_power": {
        "start_node": "q_power_1",
        "nodes": {
            "q_power_1": {
                "question": "Does the power light turn on when you press the power button?",
                "subtext": "Check for any LED activity or fan spin inside the computer case.",
                "yes": "q_power_2",
                "no": "diag_psu_failure"
            },
            "q_power_2": {
                "question": "Do the cooling fans spin continuously without turning off?",
                "subtext": "Listen closely to the air vents or look through the casing grid.",
                "yes": "diag_ram_fault",
                "no": "diag_motherboard_rail"
            }
        }
    },

    # 2. Thermal & Overheating Issues
    "cat_heat": {
        "start_node": "q_heat_1",
        "nodes": {
            "q_heat_1": {
                "question": "Does the computer shut down abruptly during heavy usage?",
                "subtext": "Notice if shutdowns happen during gaming, rendering, or multitasking.",
                "yes": "q_heat_2",
                "no": "diag_ambient_heat"
            },
            "q_heat_2": {
                "question": "Are the cooling fans making unusual loud grinding or buzzing noises?",
                "subtext": "Listen for mechanical fan friction or blocked air vents.",
                "yes": "diag_fan_failure",
                "no": "diag_thermal_paste"
            }
        }
    },

    # 3. Network & Connectivity Issues
    "cat_net": {
        "start_node": "q_net_1",
        "nodes": {
            "q_net_1": {
                "question": "Do other devices (like your phone) successfully connect to the same Wi-Fi?",
                "subtext": "Check if the router itself has an active internet connection.",
                "yes": "q_net_2",
                "no": "diag_router_isp"
            },
            "q_net_2": {
                "question": "Is your network adapter visible and enabled in System Settings / Device Manager?",
                "subtext": "Look for warning icons next to Network Adapters.",
                "yes": "diag_ip_dns_conflict",
                "no": "diag_corrupt_net_driver"
            }
        }
    },

    # 4. Performance & System Speed
    "cat_slow": {
        "start_node": "q_slow_1",
        "nodes": {
            "q_slow_1": {
                "question": "Is Task Manager showing CPU or Memory usage continuously near 100%?",
                "subtext": "Press Ctrl + Shift + Esc to check performance graphs.",
                "yes": "q_slow_2",
                "no": "diag_storage_fragmented"
            },
            "q_slow_2": {
                "question": "Does the computer take more than 3 minutes to load up to the desktop?",
                "subtext": "Observe startup programs launching automatically after login.",
                "yes": "diag_startup_apps",
                "no": "diag_malware_process"
            }
        }
    },

    # 5. Audio & Sound Output Issues
    "cat_audio": {
        "start_node": "q_audio_1",
        "nodes": {
            "q_audio_1": {
                "question": "Is the correct playback device selected in the system volume menu?",
                "subtext": "Click the sound icon on the taskbar to review active output endpoints.",
                "yes": "q_audio_2",
                "no": "diag_audio_routing"
            },
            "q_audio_2": {
                "question": "Does sound play properly when you plug in external headphones?",
                "subtext": "Test secondary audio jacks or Bluetooth audio devices.",
                "yes": "diag_internal_speaker",
                "no": "diag_audio_driver"
            }
        }
    }
}

DIAGNOSES = {
    "diag_psu_failure": {
        "title": "Faulty Power Supply Unit (PSU) or Charger",
        "description": "The system receives no electrical current, indicating a dead power adapter, defective PSU, or tripped wall breaker.",
        "action": "Verify wall outlet power, inspect charger cables for damage, and test with a known functional PSU."
    },
    "diag_ram_fault": {
        "title": "RAM / Memory Contact Fault",
        "description": "The system powers on but fails to POST or output video display. This points to loose or oxidized RAM pins.",
        "action": "Unplug power, open case, remove RAM modules, clean gold contacts with a rubber eraser, and re-seat them firmly."
    },
    "diag_motherboard_rail": {
        "title": "Motherboard Power Rail / VRM Short",
        "description": "Fans spin momentarily and cut off, indicating VRM short-circuits or damaged motherboard capacitors.",
        "action": "Perform a CMOS battery reset, disconnect external peripherals, and check for blown motherboard components."
    },
    "diag_ambient_heat": {
        "title": "Dust Accumulation & Restricted Airflow",
        "description": "System runs warmer than average due to clogged dust filters and thermal throttling.",
        "action": "Clear air intake vents and internal heatsink fins using compressed air."
    },
    "diag_fan_failure": {
        "title": "Mechanical Cooling Fan Failure",
        "description": "Cooling fans have failed or operate below required RPM thresholds, driving temperatures past safe limits.",
        "action": "Replace defective CPU cooler or chassis exhaust fans."
    },
    "diag_thermal_paste": {
        "title": "Degraded CPU Thermal Interface Material",
        "description": "Thermal paste between CPU heat spreader and heatsink has dried out, preventing efficient thermal transfer.",
        "action": "Clean off old thermal compound with isopropyl alcohol and apply fresh thermal paste."
    },
    "diag_router_isp": {
        "title": "Router / Internet Service Provider Outage",
        "description": "Local access point has lost upstream WAN connection.",
        "action": "Power cycle your modem/router. Contact your ISP if internet lights remain off or red."
    },
    "diag_ip_dns_conflict": {
        "title": "IP Address or DNS Resolver Conflict",
        "description": "Network interface is active but cannot resolve domain names or route packets.",
        "action": "Open Command Prompt as administrator and run: netsh winsock reset && ipconfig /flushdns"
    },
    "diag_corrupt_net_driver": {
        "title": "Missing or Corrupted Network Driver",
        "description": "The operating system cannot communicate with the Wi-Fi card or Ethernet adapter.",
        "action": "Reinstall official network drivers from the manufacturer site using Device Manager."
    },
    "diag_storage_fragmented": {
        "title": "Storage Bottleneck / Drive Degradation",
        "description": "Slow response times caused by fragmented mechanical drives or low system disk space.",
        "action": "Free up at least 15% drive space or upgrade your primary OS drive to a Solid State Drive (SSD)."
    },
    "diag_startup_apps": {
        "title": "Excessive Background Startup Services",
        "description": "Multiple background services auto-launching on boot, clogging CPU/RAM memory allocations.",
        "action": "Open Task Manager, go to Startup Apps, and disable unnecessary background software."
    },
    "diag_malware_process": {
        "title": "Unwanted Background Activity / Malware",
        "description": "Unidentified background processes consuming high CPU/Memory clock cycles.",
        "action": "Run an offline system scan using Windows Defender or Malwarebytes."
    },
    "diag_audio_routing": {
        "title": "Incorrect Audio Playback Target",
        "description": "Audio output is being routed to an inactive display or disconnected audio endpoint.",
        "action": "Click the sound tray icon and change default playback device to Speakers/Headphones."
    },
    "diag_audio_driver": {
        "title": "Corrupted Audio Service / Driver",
        "description": "Windows Audio endpoint service or High Definition Audio Controller driver crashed.",
        "action": "Restart Windows Audio service via services.msc or reinstall Realtek High Definition Audio drivers."
    },
    "diag_internal_speaker": {
        "title": "Internal Speaker Hardware Fault",
        "description": "Audio signal processes normally, but internal laptop speakers or wiring harness are damaged.",
        "action": "Inspect internal speaker connections or use external speakers/Bluetooth audio."
    }
}