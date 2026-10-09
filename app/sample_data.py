"""
Sample realistic discharge recovery plans for Demo Mode in English, Hindi, and Kannada.
Conforms strictly to prompts/01_extraction_prompt.md schema.
"""

SAMPLE_DATA = {
    "English": {
        "document_quality": "good",
        "document_type": "discharge_summary",
        "document_language_detected": "English",
        "patient_first_name": "Ramesh",
        "discharge_date": "2026-10-06",
        "care_profile": ["post_surgery", "infection"],
        "diagnosis_plain": "Acute appendicitis with keyhole surgery to remove the appendix (laparoscopic appendectomy)",
        "procedure_plain": "Laparoscopic appendectomy under general anesthesia",
        "medicines": [
            {
                "name_as_written": "Tab Augmentin 625mg",
                "form": "tablet",
                "dose": "625mg",
                "frequency_as_written": "1-0-1 (BD)",
                "as_needed": False,
                "times_of_day": ["morning", "night"],
                "suggested_clock_times": ["08:00", "20:00"],
                "duration_days": 5,
                "duration_as_written": "5 days",
                "with_food": "after",
                "purpose_plain": "Antibiotic to prevent bacterial infection in the wound",
                "special_instructions_plain": "Complete the full 5-day course even if you feel better",
                "is_critical": True,
                "confidence": "high",
                "source_text": "Tab Augmentin 625mg 1-0-1 x 5 days PC"
            },
            {
                "name_as_written": "Tab Pantocid 40mg",
                "form": "tablet",
                "dose": "40mg",
                "frequency_as_written": "1-0-0 (OD)",
                "as_needed": False,
                "times_of_day": ["morning"],
                "suggested_clock_times": ["07:30"],
                "duration_days": 7,
                "duration_as_written": "7 days",
                "with_food": "before",
                "purpose_plain": "Reduces stomach acid to prevent heartburn from other medicines",
                "special_instructions_plain": "Take 30 minutes before breakfast with a glass of water",
                "is_critical": False,
                "confidence": "high",
                "source_text": "Tab Pantocid 40mg 1-0-0 x 7 days AC"
            },
            {
                "name_as_written": "Tab Dolo 650mg",
                "form": "tablet",
                "dose": "650mg",
                "frequency_as_written": "SOS (PRN)",
                "as_needed": True,
                "times_of_day": [],
                "suggested_clock_times": [],
                "duration_days": 3,
                "duration_as_written": "SOS max 3 days",
                "with_food": "after",
                "purpose_plain": "Pain relief and fever reduction",
                "special_instructions_plain": "Take only if pain or fever occurs, minimum 6 hours between tablets",
                "is_critical": False,
                "confidence": "high",
                "source_text": "Tab Dolo 650mg SOS for pain PC"
            },
            {
                "name_as_written": "Syp Cremaffin 15ml",
                "form": "syrup",
                "dose": "15ml",
                "frequency_as_written": "0-0-1 (HS)",
                "as_needed": False,
                "times_of_day": ["night"],
                "suggested_clock_times": ["21:00"],
                "duration_days": 3,
                "duration_as_written": "3 days",
                "with_food": "after",
                "purpose_plain": "Gentle stool softener to prevent straining after abdominal surgery",
                "special_instructions_plain": "Take with a full glass of warm water at bedtime",
                "is_critical": False,
                "confidence": "medium",
                "source_text": "Syp Cremaffin 15ml HS x 3 days"
            }
        ],
        "monitoring": [
            {
                "parameter": "temperature",
                "label_plain": "Body Temperature",
                "frequency_as_written": "Twice daily",
                "suggested_clock_times": ["08:00", "20:00"],
                "target_range": "97.5°F - 98.6°F",
                "alert_thresholds": "Above 100.4°F",
                "mentioned_in_document": True,
                "responsible_suggested": "self",
                "confidence": "high",
                "source_text": "Record temp BD, report fever >100.4F"
            },
            {
                "parameter": "wound_check",
                "label_plain": "Surgical Wound Check",
                "frequency_as_written": "Daily",
                "suggested_clock_times": ["09:00"],
                "target_range": "Dry and clean incisions",
                "alert_thresholds": "Yellow discharge, increasing redness or swelling",
                "mentioned_in_document": True,
                "responsible_suggested": "family",
                "confidence": "high",
                "source_text": "Inspect suture site daily for soakage or erythema"
            }
        ],
        "follow_ups": [
            {
                "what_plain": "Surgical OPD review for suture check and wound dressing",
                "date": None,
                "date_as_written": "Review after 7 days",
                "relative_days_from_discharge": 7,
                "doctor_or_clinic": "General Surgery OPD, Dr. K. Sharma",
                "what_to_bring_plain": "Bring discharge summary, current medicine strip, and temperature log",
                "confidence": "high"
            }
        ],
        "diet_and_activity": [
            "Eat soft, easy-to-digest light food like porridge, dal khichdi, and curd rice for 3 days.",
            "Drink at least 8 to 10 glasses of clean water daily.",
            "Avoid lifting heavy weights over 5 kg and avoid strenuous abdominal exercise for 3 weeks.",
            "Gentle walking inside the room is encouraged to help bowel movements."
        ],
        "wound_or_device_care_plain": "Keep surgical dressing completely clean and dry. Do not scrub or submerge wound in a bath. If dressing becomes soaked, visit clinic for sterile redressing.",
        "red_flags": [
            {
                "symptom_plain": "Sudden sharp or worsening severe belly pain",
                "action": "Go immediately to the hospital Emergency Department",
                "urgency": "emergency",
                "source_text": "Severe acute abdomen / persistent pain"
            },
            {
                "symptom_plain": "Fever higher than 100.4°F with chills or shivering",
                "action": "Contact the surgical duty doctor or clinic immediately",
                "urgency": "call_doctor",
                "source_text": "High grade fever with rigors >100.4 F"
            },
            {
                "symptom_plain": "Redness, warmth, or yellow pus leaking from keyhole cuts",
                "action": "Call the hospital clinic for wound evaluation",
                "urgency": "call_doctor",
                "source_text": "Purulent wound soakage or active bleeding"
            },
            {
                "symptom_plain": "Persistent vomiting or inability to keep fluids down for over 6 hours",
                "action": "Seek urgent medical attention at the emergency ward",
                "urgency": "emergency",
                "source_text": "Continuous vomiting / dehydration"
            }
        ],
        "checkin_questions": [
            {
                "question_plain": "Do you have any severe belly pain today?",
                "linked_red_flag_index": 0
            },
            {
                "question_plain": "Was your temperature above 100.4°F today?",
                "linked_red_flag_index": 1
            },
            {
                "question_plain": "Is there any redness or fluid leaking from your surgery wound?",
                "linked_red_flag_index": 2
            },
            {
                "question_plain": "Have you had a normal bowel movement without straining?",
                "linked_red_flag_index": None
            }
        ],
        "contacts": [
            {"label": "Hospital Emergency Ward", "number": "080-22223344"},
            {"label": "Surgery Department Desk", "number": "080-22223350"}
        ],
        "uncertain_items": [
            {
                "text": "Syp Cremaffin duration marked with faint pencil '3d?'",
                "reason": "Handwritten duration for laxative is faint; please confirm with doctor if needed beyond 3 days"
            }
        ],
        "missing_info": [
            "No exact date given for suture removal, only 'review after 7 days'",
            "No specific shower or bathing instructions given for the first 48 hours"
        ],
        "summary_plain": "Ramesh was treated in the hospital for sudden appendix inflammation and had keyhole surgery to safely remove it. At home, you need to finish the antibiotic course, keep the surgical incisions dry, and rest with light meals. If you develop high fever, intense belly pain, or pus from the wound, seek urgent medical help. This is a summary to help you understand your papers. It is not medical advice. Always follow your doctor's instructions."
    },

    "Hindi": {
        "document_quality": "good",
        "document_type": "discharge_summary",
        "document_language_detected": "English",
        "patient_first_name": "Ramesh",
        "discharge_date": "2026-10-06",
        "care_profile": ["post_surgery", "infection"],
        "diagnosis_plain": "अपेंडिक्स की अचानक सूजन और दूरबीन विधि से अपेंडिक्स निकालने का ऑपरेशन (लैप्रोस्कोपिक अपेंडिसेक्टॉमी)",
        "procedure_plain": "जनरल एनेस्थीसिया के तहत लैप्रोस्कोपिक अपेंडिक्स सर्जरी",
        "medicines": [
            {
                "name_as_written": "Tab Augmentin 625mg",
                "form": "tablet",
                "dose": "625mg",
                "frequency_as_written": "1-0-1 (BD)",
                "as_needed": False,
                "times_of_day": ["morning", "night"],
                "suggested_clock_times": ["08:00", "20:00"],
                "duration_days": 5,
                "duration_as_written": "5 days",
                "with_food": "after",
                "purpose_plain": "घाव में बैक्टीरिया के संक्रमण से बचाव के लिए एंटीबायोटिक दवा",
                "special_instructions_plain": "तबीयत ठीक लगने पर भी पूरे 5 दिन का कोर्स जरूर पूरा करें",
                "is_critical": True,
                "confidence": "high",
                "source_text": "Tab Augmentin 625mg 1-0-1 x 5 days PC"
            },
            {
                "name_as_written": "Tab Pantocid 40mg",
                "form": "tablet",
                "dose": "40mg",
                "frequency_as_written": "1-0-0 (OD)",
                "as_needed": False,
                "times_of_day": ["morning"],
                "suggested_clock_times": ["07:30"],
                "duration_days": 7,
                "duration_as_written": "7 days",
                "with_food": "before",
                "purpose_plain": "पेट में गैस और जलन कम करने के लिए",
                "special_instructions_plain": "सुबह नाश्ते से 30 मिनट पहले एक गिलास पानी के साथ लें",
                "is_critical": False,
                "confidence": "high",
                "source_text": "Tab Pantocid 40mg 1-0-0 x 7 days AC"
            },
            {
                "name_as_written": "Tab Dolo 650mg",
                "form": "tablet",
                "dose": "650mg",
                "frequency_as_written": "SOS (PRN)",
                "as_needed": True,
                "times_of_day": [],
                "suggested_clock_times": [],
                "duration_days": 3,
                "duration_as_written": "SOS max 3 days",
                "with_food": "after",
                "purpose_plain": "दर्द और बुखार कम करने के लिए",
                "special_instructions_plain": "केवल तेज दर्द या बुखार होने पर ही लें, दो गोलियों के बीच कम से कम 6 घंटे का अंतर रखें",
                "is_critical": False,
                "confidence": "high",
                "source_text": "Tab Dolo 650mg SOS for pain PC"
            },
            {
                "name_as_written": "Syp Cremaffin 15ml",
                "form": "syrup",
                "dose": "15ml",
                "frequency_as_written": "0-0-1 (HS)",
                "as_needed": False,
                "times_of_day": ["night"],
                "suggested_clock_times": ["21:00"],
                "duration_days": 3,
                "duration_as_written": "3 days",
                "with_food": "after",
                "purpose_plain": "पेट साफ रखने के लिए सिरप ताकि सर्जरी के बाद पेट पर जोर न पड़े",
                "special_instructions_plain": "रात को सोते समय गुनगुने पानी के साथ लें",
                "is_critical": False,
                "confidence": "medium",
                "source_text": "Syp Cremaffin 15ml HS x 3 days"
            }
        ],
        "monitoring": [
            {
                "parameter": "temperature",
                "label_plain": "शरीर का तापमान (बुखार जांच)",
                "frequency_as_written": "Twice daily",
                "suggested_clock_times": ["08:00", "20:00"],
                "target_range": "97.5°F - 98.6°F",
                "alert_thresholds": "100.4°F से अधिक",
                "mentioned_in_document": True,
                "responsible_suggested": "self",
                "confidence": "high",
                "source_text": "Record temp BD, report fever >100.4F"
            },
            {
                "parameter": "wound_check",
                "label_plain": "सर्जरी के घाव की जांच",
                "frequency_as_written": "Daily",
                "suggested_clock_times": ["09:00"],
                "target_range": "सूखा और साफ चीरा",
                "alert_thresholds": "पीला मवाद, लाली या सूजन बढ़ना",
                "mentioned_in_document": True,
                "responsible_suggested": "family",
                "confidence": "high",
                "source_text": "Inspect suture site daily for soakage or erythema"
            }
        ],
        "follow_ups": [
            {
                "what_plain": "टांके और घाव की जांच के लिए सर्जरी ओपीडी में डॉक्टर से मिलना",
                "date": None,
                "date_as_written": "7 दिन बाद दिखाएं",
                "relative_days_from_discharge": 7,
                "doctor_or_clinic": "जनरल सर्जरी ओपीडी, डॉ. के. शर्मा",
                "what_to_bring_plain": "डिस्चार्ज कार्ड, दवाओं के पत्ते और बुखार का रिकॉर्ड साथ लाएं",
                "confidence": "high"
            }
        ],
        "diet_and_activity": [
            "3 दिनों तक खिचड़ी, दलिया और दही-चावल जैसा हल्का और सुपाच्य भोजन लें।",
            "दिन भर में 8 से 10 गिलास साफ पानी पिएं।",
            "अगले 3 हफ्तों तक 5 किलो से भारी वजन न उठाएं और पेट पर जोर डालने वाले व्यायाम न करें।",
            "कमरे में धीरे-धीरे टहलें, इससे पेट और पाचन ठीक रहता है।"
        ],
        "wound_or_device_care_plain": "सर्जरी की पट्टी को पूरी तरह सूखा और साफ रखें। घाव पर पानी न पड़ने दें। यदि पट्टी भीग जाए तो तुरंत अस्पताल में नई पट्टी करवाएं।",
        "red_flags": [
            {
                "symptom_plain": "पेट में अचानक बहुत तेज दर्द होना या दर्द लगातार बढ़ना",
                "action": "तुरंत अस्पताल के आपातकालीन विभाग (Emergency) में जाएं",
                "urgency": "emergency",
                "source_text": "Severe acute abdomen / persistent pain"
            },
            {
                "symptom_plain": "100.4°F से ज्यादा तेज बुखार आना और कंपकंपी छूटना",
                "action": "तुरंत अपने सर्जन या अस्पताल के डॉक्टर से संपर्क करें",
                "urgency": "call_doctor",
                "source_text": "High grade fever with rigors >100.4 F"
            },
            {
                "symptom_plain": "घाव से पीला मवाद निकलना, खून बहना या लालिमा फैलना",
                "action": "तुरंत डॉक्टर को फोन करें या क्लिनिक जाएं",
                "urgency": "call_doctor",
                "source_text": "Purulent wound soakage or active bleeding"
            },
            {
                "symptom_plain": "लगातार उल्टियां होना या 6 घंटे से पानी भी न पच पाना",
                "action": "तुरंत आपातकालीन कक्ष में डॉक्टर को दिखाएं",
                "urgency": "emergency",
                "source_text": "Continuous vomiting / dehydration"
            }
        ],
        "checkin_questions": [
            {
                "question_plain": "क्या आज आपको पेट में तेज दर्द महसूस हो रहा है?",
                "linked_red_flag_index": 0
            },
            {
                "question_plain": "क्या आज आपका बुखार 100.4°F से ऊपर गया?",
                "linked_red_flag_index": 1
            },
            {
                "question_plain": "क्या ऑपरेशन के घाव से कोई रिसाव या लाली दिख रही है?",
                "linked_red_flag_index": 2
            },
            {
                "question_plain": "क्या आपका पेट बिना जोर लगाए आराम से साफ हुआ?",
                "linked_red_flag_index": None
            }
        ],
        "contacts": [
            {"label": "अस्पताल आपातकालीन विभाग", "number": "080-22223344"},
            {"label": "सर्जरी विभाग हेल्पडेस्क", "number": "080-22223350"}
        ],
        "uncertain_items": [
            {
                "text": "Syp Cremaffin की अवधि पर हल्की पेंसिल से '3d?' लिखा है",
                "reason": "दवा का समय स्पष्ट नहीं है; 3 दिन के बाद इसे जारी रखने के लिए डॉक्टर से पूछें"
            }
        ],
        "missing_info": [
            "टांके काटने की निश्चित तारीख नहीं दी गई है, केवल '7 दिन बाद' लिखा है",
            "पहले 48 घंटों में नहाने के संबंध में कोई स्पष्ट निर्देश नहीं हैं"
        ],
        "summary_plain": "रमेश को अपेंडिक्स में अचानक सूजन के कारण अस्पताल में भर्ती किया गया था और दूरबीन द्वारा अपेंडिक्स का ऑपरेशन किया गया। घर पर आपको एंटीबायोटिक की पूरी खुराक लेनी है, घाव को सूखा रखना है और हल्का खाना खाना है। यदि तेज बुखार, असहनीय पेट दर्द या घाव से मवाद आए तो तुरंत अस्पताल जाएं। यह सारांश आपके कागजात को समझने में मदद करने के लिए है। यह चिकित्सीय सलाह नहीं है। हमेशा अपने डॉक्टर के निर्देशों का पालन करें।"
    },

    "Kannada": {
        "document_quality": "good",
        "document_type": "discharge_summary",
        "document_language_detected": "English",
        "patient_first_name": "Ramesh",
        "discharge_date": "2026-10-06",
        "care_profile": ["post_surgery", "infection"],
        "diagnosis_plain": "ಅಪಂಡಿಕ್ಸ್‌ನ ತೀವ್ರ ಉರಿಯೂತ ಮತ್ತು ಲ್ಯಾಪರೊಸ್ಕೋಪಿಕ್ ಶಸ್ತ್ರಚಿಕಿತ್ಸೆ ಮೂಲಕ ಅಪಂಡಿಕ್ಸ್ ತೆಗೆಯುವಿಕೆ",
        "procedure_plain": "ಜನರಲ್ ಅನೆಸ್ತೇಷಿಯಾ ಅಡಿಯಲ್ಲಿ ಲ್ಯಾಪರೊಸ್ಕೋಪಿಕ್ ಅಪೆಂಡಿಸೆಕ್ಟಮಿ",
        "medicines": [
            {
                "name_as_written": "Tab Augmentin 625mg",
                "form": "tablet",
                "dose": "625mg",
                "frequency_as_written": "1-0-1 (BD)",
                "as_needed": False,
                "times_of_day": ["morning", "night"],
                "suggested_clock_times": ["08:00", "20:00"],
                "duration_days": 5,
                "duration_as_written": "5 days",
                "with_food": "after",
                "purpose_plain": "ಗಾಯದಲ್ಲಿ ಬ್ಯಾಕ್ಟೀರಿಯಾ ಸೋಂಕು ತಡೆಗಟ್ಟಲು ಆಂಟಿಬಯೋಟಿಕ್ ಔಷಧಿ",
                "special_instructions_plain": "ಗುಣಮುಖರಾದಂತೆ ಅನ್ನಿಸಿದರೂ ಪೂರ್ತಿ 5 ದಿನಗಳ ಕೋರ್ಸ್ ಮುಗಿಸಿ",
                "is_critical": True,
                "confidence": "high",
                "source_text": "Tab Augmentin 625mg 1-0-1 x 5 days PC"
            },
            {
                "name_as_written": "Tab Pantocid 40mg",
                "form": "tablet",
                "dose": "40mg",
                "frequency_as_written": "1-0-0 (OD)",
                "as_needed": False,
                "times_of_day": ["morning"],
                "suggested_clock_times": ["07:30"],
                "duration_days": 7,
                "duration_as_written": "7 days",
                "with_food": "before",
                "purpose_plain": "ಹೊಟ್ಟೆಯಲ್ಲಿ ಆಸಿಡ್ ಮತ್ತು ಎದೆಯುರಿ ಕಡಿಮೆ ಮಾಡಲು",
                "special_instructions_plain": "ಬೆಳಿಗ್ಗೆ ಉಪಾಹಾರಕ್ಕಿಂತ 30 ನಿಮಿಷ ಮುಂಚಿತವಾಗಿ ನೀರಿನೊಂದಿಗೆ ಸೇವಿಸಿ",
                "is_critical": False,
                "confidence": "high",
                "source_text": "Tab Pantocid 40mg 1-0-0 x 7 days AC"
            },
            {
                "name_as_written": "Tab Dolo 650mg",
                "form": "tablet",
                "dose": "650mg",
                "frequency_as_written": "SOS (PRN)",
                "as_needed": True,
                "times_of_day": [],
                "suggested_clock_times": [],
                "duration_days": 3,
                "duration_as_written": "SOS max 3 days",
                "with_food": "after",
                "purpose_plain": "ನೋವು ಮತ್ತು ಜ್ವರ ನಿವಾರಣೆಗೆ",
                "special_instructions_plain": "ನೋವು ಅಥವಾ ಜ್ವರ ಇದ್ದಾಗ ಮಾತ್ರ ತೆಗೆದುಕೊಳ್ಳಿ, ಎರಡು ಮಾತ್ರೆಗಳ ನಡುವೆ ಕನಿಷ್ಠ 6 ಗಂಟೆಗಳ ಅಂತರವಿರಲಿ",
                "is_critical": False,
                "confidence": "high",
                "source_text": "Tab Dolo 650mg SOS for pain PC"
            },
            {
                "name_as_written": "Syp Cremaffin 15ml",
                "form": "syrup",
                "dose": "15ml",
                "frequency_as_written": "0-0-1 (HS)",
                "as_needed": False,
                "times_of_day": ["night"],
                "suggested_clock_times": ["21:00"],
                "duration_days": 3,
                "duration_as_written": "3 days",
                "with_food": "after",
                "purpose_plain": "ಹೊಟ್ಟೆಯ ಮೇಲೆ ಒತ್ತಡ ಬೀಳದಂತೆ ಮಲಬದ್ಧತೆ ನಿವಾರಣೆಗೆ ಸಿರಪ್",
                "special_instructions_plain": "ರಾತ್ರಿ ಮಲಗುವಾಗ ಬೆಚ್ಚಗಿನ ನೀರಿನೊಂದಿಗೆ ತೆಗೆದುಕೊಳ್ಳಿ",
                "is_critical": False,
                "confidence": "medium",
                "source_text": "Syp Cremaffin 15ml HS x 3 days"
            }
        ],
        "monitoring": [
            {
                "parameter": "temperature",
                "label_plain": "ದೇಹದ ತಾಪಮಾನ (ಜ್ವರ ಪರೀಕ್ಷೆ)",
                "frequency_as_written": "Twice daily",
                "suggested_clock_times": ["08:00", "20:00"],
                "target_range": "97.5°F - 98.6°F",
                "alert_thresholds": "100.4°F ಗಿಂತ ಹೆಚ್ಚು",
                "mentioned_in_document": True,
                "responsible_suggested": "self",
                "confidence": "high",
                "source_text": "Record temp BD, report fever >100.4F"
            },
            {
                "parameter": "wound_check",
                "label_plain": "ಶಸ್ತ್ರಚಿಕಿತ್ಸೆಯ ಗಾಯದ ಪರಿಶೀಲನೆ",
                "frequency_as_written": "Daily",
                "suggested_clock_times": ["09:00"],
                "target_range": "ಒಣಗಿದ ಮತ್ತು ಸ್ವಚ್ಛವಾದ ಗಾಯ",
                "alert_thresholds": "ಹಳದಿ ಕೀವು, ಕೆಂಪಾಗುವಿಕೆ ಅಥವಾ ಊತ ಹೆಚ್ಚಾಗುವುದು",
                "mentioned_in_document": True,
                "responsible_suggested": "family",
                "confidence": "high",
                "source_text": "Inspect suture site daily for soakage or erythema"
            }
        ],
        "follow_ups": [
            {
                "what_plain": "ಹೊಲಿಗೆ ಮತ್ತು ಗಾಯ ಪರಿಶೀಲನೆಗೆ ಶಸ್ತ್ರಚಿಕಿತ್ಸಾ ವಿಭಾಗದಲ್ಲಿ ವೈದ್ಯರ ಭೇಟಿ",
                "date": None,
                "date_as_written": "7 ದಿನಗಳ ನಂತರ ಭೇಟಿ ನೀಡಿ",
                "relative_days_from_discharge": 7,
                "doctor_or_clinic": "ಜನರಲ್ ಸರ್ಜರಿ ಒಪಿಡಿ, ಡಾ. ಕೆ. ಶರ್ಮಾ",
                "what_to_bring_plain": "ಡಿಸ್ಚಾರ್ಜ್ ಸಾರಾಂಶ, ಔಷಧಿಗಳು ಮತ್ತು ಜ್ವರ ದಾಖಲೆ ಪುಸ್ತಕ ತರಬೇಕು",
                "confidence": "high"
            }
        ],
        "diet_and_activity": [
            "3 ದಿನಗಳವರೆಗೆ ಗಂಜಿ, ಕಿಚಡಿ ಮತ್ತು ಮೊಸರನ್ನದಂತಹ ಲಘು ಆಹಾರವನ್ನು ಮಾತ್ರ ಸೇವಿಸಿ.",
            "ದಿನಕ್ಕೆ ಕನಿಷ್ಠ 8 ರಿಂದ 10 ಲೋಟ ಶುದ್ಧ ನೀರು ಕುಡಿಯಿರಿ.",
            "ಮುಂದಿನ 3 ವಾರಗಳವರೆಗೆ 5 ಕೆಜಿಗಿಂತ ಹೆಚ್ಚು ಭಾರ ಎತ್ತಬೇಡಿ ಮತ್ತು ಹೊಟ್ಟೆಗೆ ಶ್ರಮ ಕೊಡುವ ಕೆಲಸ ಮಾಡಬೇಡಿ.",
            "ಜೀರ್ಣಕ್ರಿಯೆ ಸುಲಭವಾಗಲು ಮನೆಯೊಳಗೆ ನಿಧಾನವಾಗಿ ನಡೆಯುವುದು ಒಳ್ಳೆಯದು."
        ],
        "wound_or_device_care_plain": "ಗಾಯದ ಮೇಲಿನ ಬ್ಯಾಂಡೇಜ್ ಅನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ಒಣಗಿಸಿ ಸ್ವಚ್ಛವಾಗಿಡಿ. ನೀರಿನಲ್ಲಿ ನೆನೆಸಬೇಡಿ. ಬ್ಯಾಂಡೇಜ್ ಒದ್ದೆಯಾದರೆ ತಕ್ಷಣ ಕ್ಲಿನಿಕ್‌ಗೆ ಹೋಗಿ ಹೊಸ ಬ್ಯಾಂಡೇಜ್ ಹಾಕಿಸಿಕೊಳ್ಳಿ.",
        "red_flags": [
            {
                "symptom_plain": "ಹೊಟ್ಟೆಯಲ್ಲಿ ಅತಿಯಾದ ಹಠಾತ್ ನೋವು ಅಥವಾ ನಿರಂತರ ನೋವು ಹೆಚ್ಚಾಗುವುದು",
                "action": "ತಕ್ಷಣ ಆಸ್ಪತ್ರೆಯ ತುರ್ತು ಚಿಕಿತ್ಸಾ ವಿಭಾಗಕ್ಕೆ (Emergency) ತೆರಳಿ",
                "urgency": "emergency",
                "source_text": "Severe acute abdomen / persistent pain"
            },
            {
                "symptom_plain": "100.4°F ಗಿಂತ ಅಧಿಕ ಜ್ವರ ಮತ್ತು ಚಳಿಯೊಂದಿಗೆ ನಡುಕ",
                "action": "ತಕ್ಷಣ ಶಸ್ತ್ರಚಿಕಿತ್ಸಾ ವೈದ್ಯರನ್ನು ಅಥವಾ ಕ್ಲಿನಿಕ್ ಸಂಪರ್ಕಿಸಿ",
                "urgency": "call_doctor",
                "source_text": "High grade fever with rigors >100.4 F"
            },
            {
                "symptom_plain": "ಗಾಯದಿಂದ ಕೀವು, ರಕ್ತ ಸ್ರಾವ ಅಥವಾ ಕೆಂಪಾಗುವಿಕೆ ಹೆಚ್ಚಾಗುವುದು",
                "action": "ತಕ್ಷಣ ಆಸ್ಪತ್ರೆಯ ಕ್ಲಿನಿಕ್‌ಗೆ ಕರೆ ಮಾಡಿ",
                "urgency": "call_doctor",
                "source_text": "Purulent wound soakage or active bleeding"
            },
            {
                "symptom_plain": "ನಿರಂತರ ವಾಂತಿ ಅಥವಾ 6 ಗಂಟೆಗಳ ಕಾಲ ನೀರು ಸಹ ಉಳಿಯದಿರುವುದು",
                "action": "ತಕ್ಷಣ ತುರ್ತು ಚಿಕಿತ್ಸಾ ಕೊಠಡಿಗೆ ಭೇಟಿ ನೀಡಿ",
                "urgency": "emergency",
                "source_text": "Continuous vomiting / dehydration"
            }
        ],
        "checkin_questions": [
            {
                "question_plain": "ಇಂದು ನಿಮಗೆ ಹೊಟ್ಟೆಯಲ್ಲಿ ತೀವ್ರವಾದ ನೋವು ಇದೆಯೇ?",
                "linked_red_flag_index": 0
            },
            {
                "question_plain": "ಇಂದು ನಿಮ್ಮ ಜ್ವರ 100.4°F ಗಿಂತ ಹೆಚ್ಚಾಗಿದೆಯೇ?",
                "linked_red_flag_index": 1
            },
            {
                "question_plain": "ಶಸ್ತ್ರಚಿಕಿತ್ಸೆಯ ಗಾಯದಿಂದ ಕೀವು ಅಥವಾ ಕೆಂಪಾಗುವಿಕೆ ಕಂಡುಬರುತ್ತಿದೆಯೇ?",
                "linked_red_flag_index": 2
            },
            {
                "question_plain": "ಒತ್ತಡವಿಲ್ಲದೆ ಸುಲಭವಾಗಿ ಮಲವಿಸರ್ಜನೆ ಆಗಿದೆಯೇ?",
                "linked_red_flag_index": None
            }
        ],
        "contacts": [
            {"label": "ಆಸ್ಪತ್ರೆಯ ತುರ್ತು ವಿಭಾಗ", "number": "080-22223344"},
            {"label": "ಶಸ್ತ್ರಚಿಕಿತ್ಸಾ ವಿಭಾಗ", "number": "080-22223350"}
        ],
        "uncertain_items": [
            {
                "text": "Syp Cremaffin ಅವಧಿಯ ಮೇಲೆ ಪೆನ್ಸಿಲ್‌ನಿಂದ '3d?' ಎಂದು ಬರೆಯಲಾಗಿದೆ",
                "reason": "ಔಷಧಿಯ ಅವಧಿ ಸ್ಪಷ್ಟವಾಗಿಲ್ಲ; 3 ದಿನಗಳ ನಂತರ ಮುಂದುವರಿಸಬೇಕೇ ಎಂದು ವೈದ್ಯರಲ್ಲಿ ಸ್ಪಷ್ಟಪಡಿಸಿಕೊಳ್ಳಿ"
            }
        ],
        "missing_info": [
            "ಹೊಲಿಗೆ ತೆಗೆಯಲು ನಿಖರವಾದ ದಿನಾಂಕ ನೀಡಿಲ್ಲ, ಕೇವಲ '7 ದಿನಗಳ ನಂತರ' ಎಂದು ಬರೆಯಲಾಗಿದೆ",
            "ಮೊದಲ 48 ಗಂಟೆಗಳಲ್ಲಿ ಸ್ನಾನ ಮಾಡುವ ಬಗ್ಗೆ ನಿರ್ದಿಷ್ಟ ಸೂಚನೆಗಳಿಲ್ಲ"
        ],
        "summary_plain": "ರಮೇಶ್ ಅವರಿಗೆ ಅಪಂಡಿಕ್ಸ್‌ನ ತೀವ್ರ ಉರಿಯೂತವಿದ್ದ ಕಾರಣ ಆಸ್ಪತ್ರೆಗೆ ದಾಖಲಿಸಿ ಸಣ್ಣ ರಂಧ್ರದ ಶಸ್ತ್ರಚಿಕಿತ್ಸೆ ಮೂಲಕ ಅಪಂಡಿಕ್ಸ್ ತೆಗೆಯಲಾಯಿತು. ಮನೆಯಲ್ಲಿ ಆಂಟಿಬಯೋಟಿಕ್ ಮಾತ್ರೆಗಳನ್ನು ಸಮಯಕ್ಕೆ ಸರಿಯಾಗಿ ತೆಗೆದುಕೊಳ್ಳಬೇಕು, ಗಾಯವನ್ನು ಒಣಗಿಸಿಡಬೇಕು ಮತ್ತು ಲಘು ಆಹಾರ ಸೇವಿಸಬೇಕು. ಅಧಿಕ ಜ್ವರ, ಹೊಟ್ಟೆ ನೋವು ಅಥವಾ ಗಾಯದಿಂದ ಕೀವು ಬಂದರೆ ತಕ್ಷಣ ಆಸ್ಪತ್ರೆಗೆ ಭೇಟಿ ನೀಡಿ. ಇದು ನಿಮ್ಮ ದಾಖಲೆಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ಸಹಾಯ ಮಾಡುವ ಸಾರಾಂಶವಾಗಿದೆ. ಇದು ವೈದ್ಯಕೀಯ ಸಲಹೆಯಲ್ಲ. ಯಾವಾಗಲೂ ನಿಮ್ಮ ವೈದ್ಯರ ಸೂಚನೆಗಳನ್ನು ಪಾಲಿಸಿ."
    }
}


def get_sample_response(language: str = "English") -> dict:
    """Returns sample response for given language, defaulting to English."""
    lang_key = language.capitalize()
    if lang_key in SAMPLE_DATA:
        return SAMPLE_DATA[lang_key]
    return SAMPLE_DATA["English"]
