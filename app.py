from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'pc_expert_system_secret_key'

# Simple Knowledge Base for Diagnosis Questions & Results
DIAGNOSTIC_DATA = {
    'cat_power': {
        'label': 'Computer won\'t turn on',
        'questions': [
            {
                'step': 1,
                'question': 'Are any LEDs or fan lights turning on when you press the power button?',
                'subtext': 'Check the front panel power indicator light or internal fans.'
            },
            {
                'step': 2,
                'question': 'Is the power cable securely plugged into a working wall outlet?',
                'subtext': 'Try plugging another device into the outlet to verify power delivery.'
            },
            {
                'step': 3,
                'question': 'Does the system emit a sequence of beeping sounds upon startup?',
                'subtext': 'Listen for POST motherboard beep codes during boot attempts.'
            }
        ],
        'outcomes': {
            'no_power': {
                'title': 'Power Supply Unit (PSU) or Cable Fault',
                'description': 'The motherboard is receiving no electrical power, indicating an interrupted circuit or hardware component failure.',
                'action': 'Inspect wall outlets, replace the power cable, or test the system with a known working Power Supply Unit (PSU).'
            },
            'beep_fault': {
                'title': 'RAM or Motherboard POST Failure',
                'description': 'Power is reaching the components, but the system fails the initial hardware self-test (POST).',
                'action': 'Reseat the RAM modules into their slots, test individual RAM sticks, or check GPU connectivity.'
            }
        }
    },
    'cat_heat': {
        'label': 'Computer is overheating',
        'questions': [
            {
                'step': 1,
                'question': 'Are the cooling fans making loud grinding noises or completely stationary?',
                'subtext': 'Visually inspect CPU or chassis fans while the system is powered.'
            },
            {
                'step': 2,
                'question': 'Has the computer shut down abruptly during heavy usage?',
                'subtext': 'Unexpected shutdowns under load often trigger thermal protection.'
            },
            {
                'step': 3,
                'question': 'Is the ventilation grill or internal heatsink blocked by dust build-up?',
                'subtext': 'Check air intakes and exhaust vents for dust accumulation.'
            }
        ],
        'outcomes': {
            'thermal_thrust': {
                'title': 'Thermal Throttling & Airflow Blockage',
                'description': 'Excess heat accumulation is causing thermal protection protocols to throttle performance or force system shutdown.',
                'action': 'Clean dust vents using compressed air, replace CPU thermal paste, and ensure cooling fans are operational.'
            }
        }
    },
    'cat_net': {
        'label': 'No internet connection',
        'questions': [
            {
                'step': 1,
                'question': 'Are other devices able to connect to the same Wi-Fi network?',
                'subtext': 'Test connectivity on a mobile phone or secondary laptop.'
            },
            {
                'step': 2,
                'question': 'Is your network adapter enabled in system settings?',
                'subtext': 'Verify status in Device Manager or Network Settings.'
            },
            {
                'step': 3,
                'question': 'Does restarting your router/modem restore connection?',
                'subtext': 'Power cycle network equipment by unplugging for 30 seconds.'
            }
        ],
        'outcomes': {
            'net_adapter': {
                'title': 'Network Driver or Adapter Misconfiguration',
                'description': 'The issue is localized to this PC rather than the external internet gateway.',
                'action': 'Reinstall Wi-Fi/Ethernet drivers, flush local DNS settings using `ipconfig /flushdns`, or reset TCP/IP stack.'
            }
        }
    },
    'cat_slow': {
        'label': 'Computer is running slowly',
        'questions': [
            {
                'step': 1,
                'question': 'Is Task Manager showing high CPU or Memory usage (near 100%)?',
                'subtext': 'Press Ctrl+Shift+Esc to open Task Manager and check resource metrics.'
            },
            {
                'step': 2,
                'question': 'Is your primary storage drive nearly full (less than 10% free space)?',
                'subtext': 'Check space availability on the system drive (usually C:).'
            },
            {
                'step': 3,
                'question': 'Does the slowdown persist after a complete system restart?',
                'subtext': 'Select Restart rather than Shut Down to clear temporary cached memory.'
            }
        ],
        'outcomes': {
            'resource_exhaustion': {
                'title': 'System Memory or Drive Bottleneck',
                'description': 'Insufficient RAM or storage space is causing excessive virtual memory paging.',
                'action': 'Disable unnecessary startup programs, uninstall heavy background applications, and free up disk space or upgrade to an SSD.'
            }
        }
    },
    'cat_audio': {
        'label': 'No sound output',
        'questions': [
            {
                'step': 1,
                'question': 'Is the correct playback device selected in the audio settings?',
                'subtext': 'Check the volume icon in the taskbar for the active output device.'
            },
            {
                'step': 2,
                'question': 'Are external speakers or headphones plugged into the correct audio jack?',
                'subtext': 'Verify physical connection to the green 3.5mm jack or USB port.'
            },
            {
                'step': 3,
                'question': 'Does the Windows Audio troubleshooting tool detect driver errors?',
                'subtext': 'Run audio troubleshooter from system settings.'
            }
        ],
        'outcomes': {
            'audio_driver': {
                'title': 'Audio Device Configuration or Driver Failure',
                'description': 'The sound card driver is unresponsive or routed to an inactive audio output device.',
                'action': 'Set default playback device, update Realtek/Audio drivers via Device Manager, or restart Windows Audio Service (`services.msc`).'
            }
        }
    }
}


# --- NAVIGATION ROUTES ---
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('navigation', page_name='SignIn'))
        
    return render_template('index.html', page='Home', user=session.get('user'))

@app.route('/nav/<page_name>')
def navigation(page_name):
    # Protect all pages except 'SignIn' for logged-out users
    if 'user' not in session and page_name != 'SignIn':
        return redirect(url_for('navigation', page_name='SignIn'))
        
    return render_template('index.html', page=page_name, user=session.get('user'))


# --- AUTHENTICATION ROUTES ---
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if email and password:
        session['user'] = email.split('@')[0]
        return redirect(url_for('navigation', page_name='Home'))

    return render_template('index.html', page='SignIn', login_error="Invalid email or password credentials.")

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if name and email and password:
        session['user'] = name
        return redirect(url_for('navigation', page_name='Home'))

    return render_template('index.html', page='SignIn', register_error="Please fill in all registration fields.")

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.form.get('email', '').strip()

    forgot_message = f"If {email} is registered, a password reset link has been sent to your inbox."

    return render_template(
        'index.html',
        page='SignIn',
        forgot_message=forgot_message
    )

@app.route('/guest')
def guest():
    session['user'] = 'Guest User'
    return redirect(url_for('navigation', page_name='Diagnose'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('navigation', page_name='SignIn'))


# --- DIAGNOSTIC ENGINE ROUTES ---
@app.route('/select_category/<cat_id>')
def select_category(cat_id):
    if 'user' not in session:
        return redirect(url_for('navigation', page_name='SignIn'))

    if cat_id in DIAGNOSTIC_DATA:
        session['selected_category'] = cat_id
        session['step_number'] = 1
        session['answers'] = []
        session['completed'] = False
    return redirect(url_for('navigation', page_name='Diagnose'))

@app.route('/answer/<user_choice>')
def process_answer(user_choice):
    if 'user' not in session:
        return redirect(url_for('navigation', page_name='SignIn'))

    cat_id = session.get('selected_category')
    step = session.get('step_number', 1)

    if cat_id and cat_id in DIAGNOSTIC_DATA:
        answers = session.get('answers', [])
        answers.append(user_choice)
        session['answers'] = answers

        if step < len(DIAGNOSTIC_DATA[cat_id]['questions']):
            session['step_number'] = step + 1
        else:
            session['completed'] = True

    return redirect(url_for('navigation', page_name='Diagnose'))

@app.route('/back')
def previous_step():
    if 'user' not in session:
        return redirect(url_for('navigation', page_name='SignIn'))

    step = session.get('step_number', 1)
    answers = session.get('answers', [])

    if step > 1:
        session['step_number'] = step - 1
        if answers:
            answers.pop()
            session['answers'] = answers
        session['completed'] = False
    else:
        session.pop('selected_category', None)
        session.pop('step_number', None)
        session.pop('answers', None)
        session.pop('completed', None)

    return redirect(url_for('navigation', page_name='Diagnose'))

@app.route('/reset')
def reset_diagnosis():
    if 'user' not in session:
        return redirect(url_for('navigation', page_name='SignIn'))

    session.pop('selected_category', None)
    session.pop('step_number', None)
    session.pop('answers', None)
    session.pop('completed', None)
    return redirect(url_for('navigation', page_name='Diagnose'))


# Inject Jinja Context for Diagnosis Engine State
@app.context_processor
def inject_diagnostic_state():
    cat_id = session.get('selected_category')
    step = session.get('step_number', 1)
    completed = session.get('completed', False)

    category_data = DIAGNOSTIC_DATA.get(cat_id) if cat_id else None
    current_question = None
    current_diagnosis = None

    if category_data:
        if not completed and step <= len(category_data['questions']):
            current_question = category_data['questions'][step - 1]
        elif completed:
            outcomes = category_data.get('outcomes', {})
            current_diagnosis = list(outcomes.values())[0] if outcomes else None

    return dict(
        selected_category=cat_id,
        category_label=category_data['label'] if category_data else None,
        step_number=step,
        current_question=current_question,
        current_diagnosis=current_diagnosis,
        diagnostic_data=DIAGNOSTIC_DATA
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)