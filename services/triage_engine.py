
import re

class TriageEngine:
    """
    Rules-based triage for high-risk detection.
    Overrides AI model prediction if emergencies are suspected.
    """
    
    RED_FLAGS = {
        "CRITICAL": ["chest pain", "shortness of breath", "difficulty breathing", "unconscious", "stroke symptoms"],
        "URGENT": ["eye pain", "vision loss", "sudden swelling", "fever + rash", "severe pain", "throat swelling"],
        "HIGH_RISK": ["infection spreading fast", "deep wound", "pus + fever", "numbness"]
    }

    def analyze_symptoms(self, symptoms_text):
        """
        Check for high-alert symptom patterns.
        """
        text = symptoms_text.lower()
        findings = []
        
        for category, flags in self.RED_FLAGS.items():
            for flag in flags:
                if flag in text:
                    findings.append((category, flag))
        
        if findings:
            # Sort by severity
            findings.sort(key=lambda x: {"CRITICAL": 0, "URGENT": 1, "HIGH_RISK": 2}[x[0]])
            return findings[0]
            
        return None, None

    def get_overridden_response(self, category, flag):
        """
        Returns emergency response for Red Flags.
        """
        if category == "CRITICAL":
            return {
                "urgency": "EMERGENCY - HIGH",
                "condition": f"Potential critical emergency (detected: {flag})",
                "recommendation": "Please call 911 or your local emergency services IMMEDIATELY. Do not wait for further screening.",
                "precautions": ["Stop all activities.", "Remain calm and seek immediate help."]
            }
        
        if category == "URGENT":
            return {
                "urgency": "HIGH",
                "condition": f"Potentially serious condition (detected: {flag})",
                "recommendation": "Please visit an Urgent Care center or Emergency Department within the next 2 hours. This requires immediate clinical evaluation.",
                "precautions": ["Avoid touching the affected area.", "Do not drive if vision is impaired."]
            }
            
        return {
            "urgency": "MODERATE/HIGH",
            "condition": f"Requires clinical attention (detected: {flag})",
            "recommendation": "Contact your doctor today. This symptom should not be ignored for more than 24 hours.",
            "precautions": ["Monitor for fever or spreading swelling."]
        }

triage_engine = TriageEngine()
