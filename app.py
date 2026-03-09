from flask import Flask, render_template, jsonify, request, session, send_file

import json
import io
import zipfile
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = 'citoyens_community_2025'

# ── DUMMY DATA ──────────────────────────────────────────────────────────────

AMBASSADORS = [
    {"id":1,"name":"Salih El Mehdi","avatar":"AB","photo_url":"/static/members/member1/img.jpg", "region":"Rabat-Sale-Kenitra","city":"Rabat","skills":["Dev","Ai Solutions","Social Media"],"role":"IT Ambassador","bio":"Passionnée par le développement communautaire et l'engagement citoyen depuis 2019.","email":"mehdi.salih@lescitoyens.org","phone":"+212 6 12 34 56 78","joined":"2025-03","events":12,"color":"#8B5CF6"},
    {"id":2,"name":"Mohamed EL AMRANI","avatar":"MA","photo_url":"/static/members/member2/img.jpg", "region":"Beni Mellal - Khenifra","city":"Beni Mellal","skills":["Debat","Facilitation","Training"],"role":"Ambassador","bio":"Facilitateur et formateur engagé, spécialisé dans l’animation de débats et le renforcement des capacités des jeunes à travers des espaces de dialogue et d’apprentissage.","email":"m.elamrani@lescitoyens.org","phone":"+212 6 30 80 92 22","joined":"2025-01","events":8,"color":"#06B6D4"},
    {"id":3,"name":"BOUCHAMAR MERYAM","avatar":"BM","photo_url":"/static/members/member3/img.jpg", "region":"CASABLANCA-SETTAT","city":"Settat","skills":["COMMUNICATION","ART","CREATIVITY"],"role":"Ambassador","bio":"Passionnée par la communication créative et l’expression artistique, je m’engage à utiliser l’art et la créativité comme leviers pour sensibiliser et renforcer la participation citoyenne.","email":"m.bouchamar@lescitoyens.org","phone":"+212 6 34 56 78 90","joined":"2025-01","events":6,"color":"#F59E0B"},
    {"id":4,"name":"Hamza Bouksim","avatar":"MB","photo_url":"/static/members/member4/img.jpg", "region":"Souss Massa","city":"Tiznit","skills":["Facilitation","Training","Youth empowerment"],"role":"Mentor Ambassador","bio":"Projects Coordinator for an International NGO.","email":"hamzabouksim1@gmail.com","phone":"+212620928858","joined":"2021-06","events":25,"color":"#06B6D4"},
    {"id":5,"name":"Chaimae CHAATET","avatar":"CC","photo_url":"/static/members/member5/img.jpg", "region":"Tanger-Tetouan-Elhoucima","city":"Tanger","skills":["Translation","Reporting"," CREATIVITY"],"role":"Ambassador","bio":"Passionnée par la traduction, le reporting et la communication créative, je contribue à valoriser les initiatives citoyennes à travers la rédaction, la documentation et le partage d’histoires inspirantes.","email":"c.chaatet@lescitoyens.org","phone":"+212 6 45 67 89 01","joined":"2020-03","events":20,"color":"#EF4444"},
    {"id":6,"name":"Ait El Mouden Khaoula","avatar":"AB","photo_url":"/static/members/member6/img.jpg", "region":"Daraa Tafilalt","city":"Ouarzazate","skills":["Dev","Ai Solutions","Social Media"],"role":"IT Ambassador","bio":"Passionnée par le développement communautaire et l'engagement citoyen depuis 2019.","email":"khaoula.mouden@lescitoyens.org","phone":"+212 6 12 34 56 78","joined":"2025-03","events":12,"color":"#8B5CF6"},
    {"id":7,"name":"bachir abou yassine","avatar":"ZM","photo_url":"/static/members/member7/img.jpg", "region":"rabat sale kenitra","city":"Sale","skills":["politics","Community Building"],"role":"Ambassador","bio":"studiant , je crois en l'art de  la politic comme vecteur de changement.","email":"bachirabouyassine@lescitoyens.org","phone":"+212 6 78 90 12 34","joined":"2022-07","events":5,"color":"#F59E0B"},
    {"id":8,"name":"Nour El Houda Elfadl","avatar":"MB","photo_url":"/static/members/member8/img.jpg", "region":"rabat sale kenitra","city":"Sidi Slimane","skills":["project managemnt","Training","Youth engagement"],"role":"Ambassador","bio":"etudiante en digital sport entrepreneurship .","email":"nourelhouda.elfadl@lescitoyens.org","phone":"+212720261025","joined":"2024-11","events":7,"color":"#06B6D4"},
     {"id":9,"name":"Mohamed Boussif","avatar":"MB","photo_url":"/static/members/member9/img.jpg", "region":"Guelmim-Oued Noun","city":"Tan-Tan","skills":["Debat","Facilitation","Training"],"role":"Ambassador","bio":"Facilitateur et formateur engagé, spécialisé dans l’animation de débats et le renforcement des capacités des jeunes à travers des espaces de dialogue et d’apprentissage.","email":"mohamed.boussif@lescitoyens.org","phone":"+212720261025","joined":"2024-11","events":7,"color":"#EF4444"},
]

EVENTS = [
    {
    "id": 1,
    "title": "مقهى المواطنة | مدينة سلا – جهة الرباط سلا القنيطرة",
    "type": "past",
    "date": "2026-02-07",
    "location": "Sale",
    "region": "Rabat-Sale-Kenitra",
    "description": "كيفاش كيشوفو شباب مدينة سلا انتخابات 2026؟ فضاء حواري مفتوح جمع شباب المدينة ف نقاش صريح حول انتخابات 2026 ودورهم فالمشاركة وصنع القرار. شكر خاص لجميع الشركاء اللي ساهمو فنجاح هاد اللقاء ودعموا خلق فضاءات حوار حقيقية مع الشباب.",
    "image": "forum",
    "image_url": "/static/event1/img.jpeg",
    "organizer": "Nour El Houda Elfadl",
    "attendees": 210,
    "tags": ["Forum", "Civic", "Youth"],
    "report": "Le forum a réuni des acteurs clés de la société civile...",
    "driveLink": "https://drive.google.com/drive/folders/example1",
    "category": "org"
    },
    {
    "id": 2,
    "title": "مقهى المواطنة | مدينة مكناس – جهة فاس مكناس",
    "type": "past",
    "date": "2026-01-14",
    "location": "Meknes",
    "region": "Fès-Meknès",
    "description": "كيفاش كيشوفو شباب مدينة سلا انتخابات 2026؟ فضاء حواري مفتوح جمع شباب المدينة ف نقاش صريح حول انتخابات 2026 ودورهم فالمشاركة وصنع القرار. شكر خاص لجميع الشركاء اللي ساهمو فنجاح هاد اللقاء ودعموا خلق فضاءات حوار حقيقية مع الشباب.",
    "image": "atelier",
    "image_url": "/static/event2/img.jpeg",
    "organizer": "Amina Benali",
    "attendees": 210,
    "tags": ["Forum", "Civic", "Youth"],
    "report": "Le forum a réuni des acteurs clés de la société civile...",
    "driveLink": "https://drive.google.com/drive/folders/example1",
    "category": "org"
    },
   {
    "id": 3,
    "title": "مقهى المواطنة مع جمعية  @tahadathfoundation ",
    "type": "past",
    "date": "2024-08-09",
    "location": "Tiznit",
    "region": "Souss-Massa",
    "description": " كان عندنا لقاء مع مجموعة من الشباب والشابات فإطار الويكاند المواطن لي وصل عندنا لجهة سوس ماسة، ولي كان لينا الشرف نستاضفو وحدة من محطاتو فمدينة تيزنيت ، ولي كانت عبارة عن مقهى المواطنة حول موضوع كيفاش ممكن تساهم المشاركة المواطنة في التنمية المحلية ؟ 🌼 كان لقاء جميل جدا بحضور أكثر من 33 شاب و شابة، و الأجمل هوما المداخلات ديالهم و التفاعل ديالهم طيلة أطوار اللقاء .. فشكرا لجميع الحاضرين على تلبية الدعوة وعلى أفكارهم الجميلة شكرا @lescitoyensma وشكرا @cctiznit ",
    "image": "forum",
    "image_url": "/static/event3/img.jpeg",
    "organizer": "Hamza Bouksim",
    "attendees": 210,
    "tags": ["Forum", "Civic", "Youth"],
    "report": "Le forum a réuni des acteurs clés de la société civile...",
    "driveLink": "https://drive.google.com/drive/folders/example1",
    "category": "org"
    },
    {
    "id": 4,
    "title": "القمة المواطنة للشباب | المركز الوطني للتخييم - مدينة بوزنيقة",
    "type": "past",
    "date": "04 – 07 دجنبر 2025",
    "location": "Bouznika",
    "region": "Casablanca - Settat",
    "description": "تنظم حركة المواطنون القمة المواطنة للشباب، الموجهة لسفراء الحركة والمشاركين الخارجيين المختارين. سينعقد الحدث من 4 إلى 7 دجنبر في المركز الوطني للتخييم ببوزنيقة الشاطئ. سيجمع هذا الموعد الوطني شبابا من مختلف الجهات في برنامج غني يضم ورشات، ندوات، تقوية القدرات ، جلسات للتفكير الجماعي و مختبرات مواطنة. فرصة لتعزيز مهاراتكم وتبادل تجاربكم وبناء طاقة مشتركة.",
    "image": "summet",
    "image_url": "/static/event4/img.jpeg",
    "organizer": "Les Citoyen",
    "attendees": 210,
    "tags": ["Forum", "Civic", "Youth"],
    "report": "Le forum a réuni des acteurs clés de la société civile...",
    "driveLink": "https://drive.google.com/drive/folders/example1",
    "category": "org"
    },
    {"id":5,"title":"Session Plaidoyer Législatif","type":"past","date":"2025-12-05","location":"Rabat","region":"Rabat-Salé-Kénitra","description":"Session de formation au plaidoyer et aux techniques d'influence législative.","image":"plaidoyer","image_url": "/static/event5/img.png","organizer":"Salma Tazi","attendees":35,"tags":["Advocacy","Legal","Training"],"report":"","driveLink":"","category":"org"},
    {"id":6,"title":"Marathon Sportif Citoyen","type":"incoming","date":"2026-04-12","location":"Fes","region":"Fès-Meknès","description":"Un marathon solidaire combinant sport et sensibilisation aux enjeux environnementaux.","image":"marathon","image_url": "/static/event6/img.png","organizer":"Omar Idrissi","attendees":500,"tags":["Sports","Environment","Youth"],"report":"","driveLink":"","category":"ambassador"},
]

OPPORTUNITIES = [
    {"id":1,"title":"Programme d'échange Euro-Med","type":"incoming","deadline":"2026-04-01","location":"Barcelone, Espagne","description":"Programme d'échange de 2 semaines pour 5 ambassadeurs en Espagne. Thème: jeunesse et citoyenneté.","tags":["Exchange","International","Youth"],"target":"Ambassadeurs","organizer":"Les Citoyens","partner":"EU Erasmus+"},
    {"id":2,"title":"Formation Leadership Avancé","type":"incoming","deadline":"2026-03-15","location":"Casablanca","description":"Formation intensive de 3 jours sur le leadership transformationnel et la gestion de projets.","tags":["Training","Leadership","Skills"],"target":"Tous","organizer":"Les Citoyens","partner":"HEM Business School"},
    {"id":3,"title":"Bourse Projet Citoyen 2026","type":"incoming","deadline":"2026-05-30","location":"National","description":"Appel à projets: financez votre initiative citoyenne jusqu'à 50,000 MAD.","tags":["Funding","Project","Grant"],"target":"Ambassadeurs","organizer":"Les Citoyens","partner":"Fondation BMCE"},
    {"id":4,"title":"Volontariat COP Climate","type":"past","deadline":"2025-10-01","location":"Nairobi, Kenya","description":"Participation en tant que délégués jeunesse à la conférence climatique COP africaine.","tags":["Environment","International","Climate"],"target":"Tous","organizer":"Les Citoyens","partner":"UN Youth"},
]

RESOURCES = [
    {"id":1,"title":"Introduction au Plaidoyer Citoyen","type":"video","duration":"5:30","thumbnail":"advocacy","category":"Plaidoyer","level":"Débutant","views":124,"description":"Les bases du plaidoyer et comment influencer les décisions publiques."},
    {"id":2,"title":"Techniques de Facilitation","type":"video","duration":"4:15","thumbnail":"facilitation","category":"Animation","level":"Intermédiaire","views":89,"description":"Comment animer des ateliers participatifs efficacement."},
    {"id":3,"title":"Community Building 101","type":"video","duration":"6:00","thumbnail":"community","category":"Communauté","level":"Débutant","views":210,"description":"Construire et maintenir une communauté engagée."},
    {"id":4,"title":"Réunion Ambassadeurs — Février 2026","type":"recording","duration":"1:22:00","thumbnail":"meeting","category":"Réunions","level":"Tous","views":45,"description":"Enregistrement de la réunion mensuelle des ambassadeurs."},
    {"id":5,"title":"Guide Gestion de Projet","type":"video","duration":"3:45","thumbnail":"project","category":"Gestion","level":"Intermédiaire","views":67,"description":"Méthodes agiles appliquées aux projets associatifs."},
    {"id":6,"title":"Réunion Stratégie 2026","type":"recording","duration":"2:05:00","thumbnail":"strategy","category":"Réunions","level":"Tous","views":38,"description":"Session de planification stratégique annuelle."},
]

MEDIA_EVENTS = [
    {"id":1,"title":"Forum Citoyen Marrakech","date":"2025-01-15","photos":24,"videos":3,"driveLink":"https://drive.google.com/drive/folders/forum2025","cover":"forum"},
    {"id":2,"title":"Caravane Culturelle Souss","date":"2025-11-10","photos":67,"videos":8,"driveLink":"https://drive.google.com/drive/folders/caravane2025","cover":"caravane"},
    {"id":3,"title":"Séminaire Leaders Jeunes","date":"2025-09-20","photos":31,"videos":2,"driveLink":"https://drive.google.com/drive/folders/seminar2025","cover":"seminar"},
]

MESSAGES = [
    {
        "id": 1,
        "from": "Salih El Mehdi",
        "fromId": 1,
        "avatar": "AB", 
        "photo_url": "/static/members/member1/img.jpg", 
        "color": "#8B5CF6",
        "time": "Il y a 2h",
        "preview": "Salut! Tu as vu le programme du hackathon?",
        "unread": True
    },
    {
        "id": 2,
        "from": "Chaimae CHAATET",
        "fromId": 5,
        "avatar": "CC",
        "photo_url": "/static/members/member5/img.jpg",
        "color": "#EF4444",
        "time": "Hier",
        "preview": "On se retrouve avant le Ftour?",
        "unread": False
    },
    {
        "id": 3,
        "from": "Mohamed EL AMRANI",
        "fromId": 2,
        "avatar": "MA",
        "photo_url": "/static/members/member2/img.jpg",
        "color": "#06B6D4",
        "time": "Il y a 3j",
        "preview": "J'ai partagé les ressources sur le drive",
        "unread": False
    },
]

TOOLKIT = [
    {"id":1,"category":"Icebreakers","title":"Le Bingo Humain","description":"Un jeu pour apprendre à se connaître rapidement en trouvant des personnes avec des caractéristiques similaires.","duration":"15 min","participants":"10-50","file":"bingo_humain.pdf"},
    {"id":2,"category":"Icebreakers","title":"La Carte des Origines","description":"Chaque participant place une épingle sur une carte pour montrer d'où il vient.","duration":"10 min","participants":"5-30","file":"carte_origines.pdf"},
    {"id":3,"category":"Animation","title":"World Café","description":"Technique de discussion en petits groupes rotatifs pour générer des idées collectives.","duration":"60-90 min","participants":"20-100","file":"world_cafe.pdf"},
    {"id":4,"category":"Animation","title":"Fishbowl","description":"Débat en cercles concentriques pour des discussions approfondies.","duration":"45 min","participants":"10-40","file":"fishbowl.pdf"},
    {"id":5,"category":"Questions","title":"Questions Déclencheurs","description":"Banque de 50 questions pour lancer des discussions sur la citoyenneté.","duration":"Variable","participants":"Tous","file":"questions_citoyennete.pdf"},
    {"id":6,"category":"Procédures","title":"Guide Organisation Événement","description":"Procédures étape par étape pour organiser un événement Les Citoyens.","duration":"—","participants":"Organisateurs","file":"guide_evenement.pdf"},
]

NOTIFICATIONS = [
    {"id":1,"type":"event","title":"Nouvel événement: Marathon Sportif Citoyen","time":"Il y a 1h","read":False,"icon":"🏃"},
    {"id":2,"type":"opportunity","title":"Nouvelle opportunité: Bourse Projet Citoyen","time":"Il y a 3h","read":False,"icon":"💼"},
    {"id":3,"type":"message","title":"Amina Benali vous a envoyé un message","time":"Il y a 5h","read":True,"icon":"💬"},
    {"id":4,"type":"event","title":"Marathon Sportif a besoin de bénévoles!","time":"Hier","read":True,"icon":"🙋"},
]

PREP_EVENTS = [
    {"id":101,"title":"Atelier Droits Numériques","organizer":"Youssef Khalil","status":"docs_pending","date":"2026-03-20","step":2,"participants":["Youssef Khalil","Amina Benali","Omar Idrissi"]},
    {"id":102,"title":"Camp Jeunesse Ouarzazate","organizer":"Omar Idrissi","status":"admin_review","date":"2026-04-05","step":3,"participants":["Omar Idrissi","Zineb Mansouri"]},
]

CURRENT_USER = {"id":99,"name":"Karim Alaoui","avatar":"KA","color":"#8B5CF6","role":"Ambassador","region":"Marrakech-Safi","city":"Marrakech","skills":["Community Building","Events"]}

# ── ROUTES ───────────────────────────────────────────────────────────────────

@app.route('/')
def login(): return render_template('login.html')

@app.route('/dashboard')
def dashboard(): return render_template('dashboard.html', user=CURRENT_USER)

@app.route('/members')
def members(): return render_template('members.html', user=CURRENT_USER)

@app.route('/events')
def events(): return render_template('events.html', user=CURRENT_USER)

@app.route('/opportunities')
def opportunities(): return render_template('opportunities.html', user=CURRENT_USER)

@app.route('/learning')
def learning(): return render_template('learning.html', user=CURRENT_USER)

@app.route('/media')
def media(): return render_template('media.html', user=CURRENT_USER)

@app.route('/messages')
def messages_page(): return render_template('messages.html', user=CURRENT_USER)

@app.route('/calendar')
def calendar_page(): return render_template('calendar.html', user=CURRENT_USER)

@app.route('/map')
def map_page(): return render_template('map.html', user=CURRENT_USER)

@app.route('/devenir-ambassadeur')
def become_ambassador(): return render_template('become_ambassador.html')

@app.route('/create-event')
def create_event(): return render_template('create_event.html', user=CURRENT_USER)

@app.route('/admin')
def admin():
    return render_template('admin.html')

# ── API ───────────────────────────────────────────────────────────────────────

@app.route('/api/ambassadors')
def api_ambassadors():
    region = request.args.get('region','')
    city = request.args.get('city','')
    skill = request.args.get('skill','')
    q = request.args.get('q','').lower()
    data = AMBASSADORS
    if region: data = [a for a in data if a['region']==region]
    if city: data = [a for a in data if a['city']==city]
    if skill: data = [a for a in data if skill in a['skills']]
    if q: data = [a for a in data if q in a['name'].lower()]
    return jsonify(data)

@app.route('/api/ambassadors/<int:aid>')
def api_ambassador(aid):
    a = next((x for x in AMBASSADORS if x['id']==aid), None)
    return jsonify(a) if a else ('Not found',404)

@app.route('/api/events')
def api_events():
    enriched = []
    for e in EVENTS:
        ev = dict(e)
        amb = next((a for a in AMBASSADORS if a['name'].lower() == e['organizer'].lower()), None)
        ev['organizer_image'] = amb['photo_url'] if amb else None
        enriched.append(ev)
    return jsonify(enriched)

@app.route('/api/events/<int:eid>')
def api_event(eid):
    e = next((x for x in EVENTS if x['id']==eid), None)
    return jsonify(e) if e else ('Not found',404)

@app.route('/api/opportunities')
def api_opportunities(): return jsonify(OPPORTUNITIES)

@app.route('/api/resources')
def api_resources(): return jsonify(RESOURCES)

@app.route('/api/media')
def api_media(): return jsonify(MEDIA_EVENTS)

@app.route('/api/messages')
def api_messages(): return jsonify(MESSAGES)

@app.route('/api/notifications')
def api_notifications(): return jsonify(NOTIFICATIONS)

@app.route('/api/toolkit')
def api_toolkit(): return jsonify(TOOLKIT)

@app.route('/api/prep-events')
def api_prep(): return jsonify(PREP_EVENTS)

@app.route('/api/user')
def api_user(): return jsonify(CURRENT_USER)

@app.route('/api/generate-rapport', methods=['POST'])
def generate_rapport():
    try:
        data = request.json or {}

        base_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(base_dir, 'Formulaire.docx'),
            os.path.join(base_dir, 'static', 'Formulaire.docx'),
            os.path.join(base_dir, 'templates', 'Formulaire.docx'),
        ]
        template_path = next((p for p in candidates if os.path.exists(p)), None)
        if template_path is None:
            app.logger.error('Formulaire.docx not found in: %s', candidates)
            return jsonify({'error': 'Formulaire.docx introuvable.'}), 500

        def fmt_date(d):
            if not d:
                return ''
            try:
                return datetime.strptime(d, '%Y-%m-%d').strftime('%d/%m/%Y')
            except Exception:
                return d

        # All placeholder variants that appear in the XML (UTF-8 encoded, XML-entity form)
        replacements = {
            '{{Nom ambassadeur}}':              data.get('ambassadeur', ''),
            '{{Ville}}':                        data.get('ville', ''),
            '{{Date rapport}}':                 fmt_date(data.get('date_rapport', '')),
            # smart-apostrophe + accented chars as they appear literally in the XML bytes
            '{{Nom de l\u2019\u00e9v\u00e9nement}}':  data.get('nom_evenement', ''),
            # XML-entity encoded variant (&#x2019; = right single quote)
            '{{Nom de l&#x2019;\u00e9v\u00e9nement}}': data.get('nom_evenement', ''),
            '{{Date \u00e9v\u00e9nement}}':     fmt_date(data.get('date_evenement', '')),
            '{{Lieu}}':                         data.get('lieu', ''),
            '{{Type activit\u00e9}}':           data.get('type_activite', ''),
            '{{Nombre participants}}':          str(data.get('nb_participants', '') or ''),
            '{{Profil participants}}':          data.get('profil_participants', ''),
            '{{Lien photos}}':                  data.get('lien_photos', ''),
            # narrative fill-in placeholders
            '(à remplir)':                      '',
            '( à remplir)':                     '',
        }

        with open(template_path, 'rb') as f:
            template_bytes = f.read()

        # Read all entries from the template zip first
        entries = {}
        with zipfile.ZipFile(io.BytesIO(template_bytes), 'r') as zin:
            for item in zin.namelist():
                entries[item] = zin.read(item)

        # Apply replacements only to XML files
        XML_FILES = ('word/document.xml', 'word/styles.xml', 'word/header1.xml',
                     'word/footer1.xml', 'word/numbering.xml')
        for fname in XML_FILES:
            if fname in entries:
                text = entries[fname].decode('utf-8')
                for placeholder, value in replacements.items():
                    # Escape XML special chars in the replacement value
                    safe_value = (value
                        .replace('&', '&amp;')
                        .replace('<', '&lt;')
                        .replace('>', '&gt;')
                        .replace('"', '&quot;'))
                    text = text.replace(placeholder, safe_value)
                entries[fname] = text.encode('utf-8')

        # Write new zip to buffer
        output_buffer = io.BytesIO()
        with zipfile.ZipFile(output_buffer, 'w', zipfile.ZIP_DEFLATED) as zout:
            for fname, content in entries.items():
                zout.writestr(fname, content)
        output_buffer.seek(0)

        nom_event = (data.get('nom_evenement', 'activite') or 'activite')
        nom_event = ''.join(c if c.isalnum() or c in '-_' else '_' for c in nom_event)[:30]
        date_ev   = data.get('date_evenement', '') or datetime.now().strftime('%Y-%m-%d')
        filename  = f'rapport_{nom_event}_{date_ev}.docx'

        from flask import make_response
        response = make_response(output_buffer.read())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Exception as e:
        app.logger.exception('generate_rapport failed')
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5050)