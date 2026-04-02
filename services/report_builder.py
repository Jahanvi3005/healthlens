
class ReportBuilder:
    """
    Builds the visual report for Gradio and the downloadable text file summary.
    """
    
    def generate_markdown(self, data):
        """
        Builds the Markdown content for the results page.
        """
        urgency_color = "#EF4444" if "HIGH" in data['urgency'] or "EMERGENCY" in data['urgency'] else "#F59E0B" if "MODERATE" in data['urgency'] else "#10B981"
        
        
        precautions_text = "\n".join([f"- {p}" for p in data['precautions']])
        
        md_content = f"""
## **Health Screening Assessment** 🏥
---

### **Visible Condition Analysis** 🔍
*Detected likely visible condition categories:* 
### **{data['condition']}**

### **Urgency Level** ⚖️
<span style="background-color: {urgency_color}; color: white; padding: 4px 12px; border-radius: 8px; font-weight: bold; font-size: 1.2rem;">{data['urgency']}</span>

### **Next Recommended Steps** 🩺
{data['recommendation']}

---

### **Precautions & Care Advice** 🛡️
{precautions_text}

---

### **Summary of Reported Symptoms** 📝
> "{data['symptom_summary']}"

---

### ⚠️ **IMPORTANT DISCLAIMER**
**This is NOT a medical diagnosis.** This tool is for **preliminary screening and educational purposes only**. 
The AI may produce inaccurate results. Always consult a licensed healthcare professional for medical advice, diagnosis, or treatment. 
**If you are experiencing a life-threatening emergency, call 911 or visit the nearest ER immediately.**
        """
        return md_content

    def generate_text_summary(self, data):
        """
        Builds a simple text file for user download.
        """
        precautions_text = "\n".join(['- ' + p for p in data['precautions']])
        summary = f"""
HealthLens AI Screening Report
------------------------------
Condition: {data['condition']}
Urgency: {data['urgency']}
Symptoms: {data['symptom_summary']}

Recommendation: {data['recommendation']}

Precautions:
{precautions_text}

DISCLAIMER: This is a preliminary AI screening tool for educational/demo use only. 
It is NOT a medical diagnosis. If you have an emergency, visit a hospital immediately.
        """
        return summary

report_builder = ReportBuilder()
