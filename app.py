
import gradio as gr
import os
import warnings
import tempfile
import pandas as pd
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Silence Warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

from services.image_preprocess import preprocessor
from services.triage_engine import triage_engine
from services.multimodal_inference import inference_service
from services.email_service import email_service
from services.database_service import database_service
from services.report_builder import report_builder

# --- ATLAS WORKSPACE LOGIC ---

def run_screening_atlas(image, symptoms, email_input, duration, severity):
    full_symptoms = f"Duration: {duration} | Severity: {severity} | Symptoms: {symptoms}"
    
    if not symptoms or len(symptoms) < 10:
        return gr.update(visible=True), gr.update(value="### [ERR] Input Data Required."), gr.update(selected="results"), None
    
    # Vision Data Pre-processing (Optional)
    processed_img_array = None
    if image is not None:
        processed_img_array, msg = preprocessor.preprocess(image)
        if processed_img_array is None:
            return gr.update(visible=True), gr.update(value=f"### [ERR] Vision failure: {msg}"), gr.update(selected="results"), None

    # AI Multimodal Reasoning (Now adaptive)
    risk_cat, risk_flag = triage_engine.analyze_symptoms(symptoms)
    if risk_cat:
        report_data = triage_engine.get_overridden_response(risk_cat, risk_flag)
    else:
        report_data = inference_service.query(processed_img_array, full_symptoms)
    
    # Store history (PERSISTENT CLOUD LOGS)
    database_service.save_screening(email_input, "N/A", full_symptoms, report_data)
    
    # Convert and build report
    report_data['symptom_summary'] = full_symptoms
    md_report = report_builder.generate_markdown(report_data)
    
    # 📩 Send Out Global Gmail Report
    if email_input and "@" in email_input:
        email_service.send_report(email_input, report_data)
        
    return gr.update(visible=True), gr.update(value=md_report, visible=True), gr.update(selected="results"), refresh_logs()

def refresh_logs():
    """
    Fetches the last 10 screening datasets for the workspace logs safely.
    """
    data = database_service.get_recent_screenings(10)
    if not data:
        return pd.DataFrame(columns=["Arrival Time", "User Contact", "Condition Category", "Urgency Rating", "Symptom Summary"])
    
    df = pd.DataFrame(data)
    
    # Safely select and rename columns, filling missing ones with "N/A"
    cols_map = {
        "timestamp_str": "Arrival Time",
        "user_email": "User Contact",
        "condition": "Condition Category",
        "urgency": "Urgency Rating",
        "symptoms": "Symptom Summary"
    }
    
    # Ensure all required columns exist
    for col in cols_map.keys():
        if col not in df.columns:
            df[col] = "N/A"
            
    final_df = df[list(cols_map.keys())].rename(columns=cols_map)
    return final_df

def export_report_file(markdown_content):
    if not markdown_content:
        return None
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        f.write(markdown_content.encode('utf-8'))
        return f.name

# Build Symmetrical Atlas Workspace
with gr.Blocks(css="assets/style.css") as demo:
    
    # Header logic
    with gr.Row(elem_classes=["atlas-header"]):
        with gr.Column(scale=8):
             gr.Markdown("# 🔍 HealthLens • Atlas Unified Workspace V3")
        with gr.Column(scale=2):
             db_status_color = '#10B981' if database_service.db is not None else '#6B7280'
             db_status_text = 'Online' if database_service.db is not None else 'Local Only'
             gr.Markdown(f"<div style='text-align: right; color: {db_status_color};'><span class='status-indicator'></span> DB: {db_status_text}</div>")

    # MAIN WORKSPACE AREA
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Column(elem_classes=["sidebar-navigation"]):
                gr.Markdown("### WORKSPACE")
                btn_dash = gr.Button("🏠 Integrated Dashboard", elem_classes=["btn-nav", "btn-nav-active"])
                btn_results = gr.Button("📊 Analysis Results", elem_classes=["btn-nav"])
                btn_alerts = gr.Button("🔔 Safety Alerts", elem_classes=["btn-nav"])
                btn_config = gr.Button("⚙️ System Config", elem_classes=["btn-nav"])
        
        with gr.Column(scale=4):
            with gr.Tabs(selected="dash") as main_tabs:
                
                # Tab 1: Clinical Dashboard
                with gr.TabItem("Dashboard", id="dash"):
                    with gr.Column(elem_classes=["main-workspace-container"]):
                        gr.Markdown("## **Analytical Intelligence Dashboard**")
                        with gr.Row():
                            with gr.Column(elem_classes=["atlas-card"], min_width=400):
                                gr.Markdown("### **Intake Protocol** 📋")
                                symptoms_input = gr.Textbox(label="Clinical Reasoning Input", placeholder="Describe conditions...", lines=5)
                                with gr.Row():
                                    duration = gr.Dropdown(["< 24h", "1-3 days", "Chronic"], label="Temporal Context")
                                    severity = gr.Slider(0, 10, label="Intensity Scale", value=5)
                                email_input = gr.Textbox(label="Output Endpoint (Email)", placeholder="patient@atlas.ai")

                            with gr.Column(elem_classes=["atlas-card"], min_width=400):
                                gr.Markdown("### **Vision Engine** 📸")
                                image_input = gr.Image(label="Optical Dataset", type="numpy")
                                
                                submit_btn = gr.Button("🚀 EXECUTE ATLAS COMPILING", variant="primary", elem_classes=["btn-atlas"])

                # Tab 2: Screening Logs Hub
                with gr.TabItem("Results", id="results"):
                    with gr.Column(elem_classes=["main-workspace-container"]):
                        gr.Markdown("## **Analysis Results & Clinical Logs**")
                        
                        # LOG TABLE (SCREENING HISTORY)
                        with gr.Column(elem_classes=["atlas-card"]):
                            gr.Markdown("### 📊 **Historical Screening Records**\n*Showing the last 10 medical datasets processed.*")
                            log_table = gr.Dataframe(value=refresh_logs, interactive=False, label="Recent Activity Registry")

                        # CURRENT ACTIVE REPORT CONSOLE
                        with gr.Column(elem_classes=["atlas-card"]):
                            gr.Markdown("### 📜 **Active Analysis Console**")
                            results_container = gr.Column(visible=False)
                            with results_container:
                                results_markdown = gr.Markdown(elem_classes=["result-markdown"])
                                with gr.Row():
                                    export_btn = gr.Button("EXPORT CLINICAL REPORT 📋", variant="secondary")
                                    alert_btn = gr.Button("🚨 EMERGENCY OVERRIDE", variant="stop")
                                    export_file = gr.File(label="Download Report", visible=False)
                            
                            with gr.Column(visible=True) as empty_log_state:
                                gr.Markdown("*Waiting for analysis datasets to compile...*")

                # Tab 3 & 4 (Placeholders)
                with gr.TabItem("Alerts", id="alerts"):
                    with gr.Column(elem_classes=["atlas-card"]):
                        gr.Markdown("### **Historical Alert Cache**\n\n*Searching database records... No alerts found.*")

                with gr.TabItem("Config", id="config"):
                    with gr.Column(elem_classes=["atlas-card"]):
                        gr.Markdown("### **Active Infrastructure Registry**\n- DB: MongoDB Protocol Atlas\n- Protocol: Global SMTP Relay\n- Reasoning: Hugging Face Backbone")

    # --- ATLAS EVENT BINDING ---
    submit_btn.click(
        fn=run_screening_atlas,
        inputs=[image_input, symptoms_input, email_input, duration, severity],
        outputs=[results_container, results_markdown, main_tabs, log_table]
    )

    btn_dash.click(fn=lambda: gr.update(selected="dash"), outputs=main_tabs)
    btn_alerts.click(fn=lambda: gr.update(selected="alerts"), outputs=main_tabs)
    btn_config.click(fn=lambda: gr.update(selected="config"), outputs=main_tabs)
    
    # Auto-refresh log table when clicking Results tab
    btn_results.click(fn=lambda: gr.update(selected="results"), outputs=main_tabs).then(
        fn=refresh_logs, outputs=log_table
    )

    export_btn.click(fn=export_report_file, inputs=results_markdown, outputs=export_file).then(
        lambda: gr.update(visible=True), outputs=export_file
    )

if __name__ == "__main__":
    demo.launch()
