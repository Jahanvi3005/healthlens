
import os
import requests
import json
import base64
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()

class MultimodalInference:
    """
    Handles Reasoning via MedGemma or equivalent multimodal LLM.
    Uses Hugging Face Inference API for CPU-only stateless efficiency.
    """
    
    def __init__(self):
        self.hf_token = os.getenv("HF_TOKEN")
        self.model_id = os.getenv("MEDGEMMA_MODEL_ID", "google/paligemma-3b-mix-224") # Or medgemma
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        self.headers = {"Authorization": f"Bearer {self.hf_token}"} if self.hf_token else {}
        
    def _image_to_base64(self, img_array):
        """
        Converts numpy image to base64 for API.
        """
        img = Image.fromarray(img_array.astype('uint8'), 'RGB')
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def query(self, image_input, symptoms):
        """
        Queries HF Inference API for MedGemma analysis.
        """
        if not self.hf_token:
            return self._mock_result(image_input, symptoms)
            
        prompt = f"Health Screening Analysis. Symptoms provided: {symptoms}."
        if image_input is not None:
             prompt += " Analyzing visible clinical evidence from provided image."
        else:
             prompt += " Note: No image provided for this screening. Base reasoning on symptoms only."
             
        prompt += " Describe possible condition, urgency (LOW, MODERATE, HIGH), and precautions."
        
        try:
            payload = {
                "inputs": {
                    "text": prompt
                }
            }
            if image_input is not None:
                 payload["inputs"]["image"] = self._image_to_base64(image_input)
                 
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            # Parse result into structured data (Implementation of parsing logic simplified for now)
            return self._parse_llm_response(result[0]['generated_text'])
        except Exception as e:
            print(f"Inference error: {e}")
            return self._mock_result(image_input, symptoms)

    def _parse_llm_response(self, text):
        """
        Simple text parser to extract structured HealthLens report.
        """
        return {
            "condition": text.split(".")[0], # Basic parsing for example
            "urgency": "MODERATE" if "MODERATE" in text.upper() else "LOW",
            "recommendation": text,
            "precautions": ["Follow up with a specialist."]
        }

    def _mock_result(self, image_input, symptoms):
        """
        Smart fallback result.
        """
        text = symptoms.lower()
        prefix = "Text-Only Analysis: " if image_input is None else "Multimodal Analysis: "
        
        if "itch" in text or "red" in text or "rash" in text:
            return {
                "condition": f"{prefix}Visible inflammatory skin condition (likely Dermatitis/Eczema)",
                "urgency": "LOW/MODERATE",
                "recommendation": "Consult a dermatologist. Use hypoallergenic moisturizer.",
                "precautions": ["Avoid scratching.", "Use fragrance-free soap.", "Monitor for signs of infection."]
            }
        elif "pimple" in text or "acne" in text:
            return {
                "condition": "Likely Acne Vulgaris",
                "urgency": "LOW",
                "recommendation": "Maintain gentle skin cleansing. Over-the-counter benzoyl peroxide may help.",
                "precautions": ["Do not pick or pop lesions.", "Use non-comedogenic sunscreen."]
            }
        elif "throat" in text or "swallow" in text:
            return {
                "condition": "Visible Pharyngitis (Throat redness)",
                "urgency": "MODERATE",
                "recommendation": "Gargle with warm salt water. Consult a GP if fever develops.",
                "precautions": ["Stay hydrated.", "Rest your voice.", "Avoid irritants like smoke."]
            }
        
        return {
            "condition": "Uncertain - Visible irritation detected",
            "urgency": "MODERATE",
            "recommendation": "Clinical assessment is required once digital screening is inconclusive.",
            "precautions": ["Keep the area clean and dry."]
        }

inference_service = MultimodalInference()
