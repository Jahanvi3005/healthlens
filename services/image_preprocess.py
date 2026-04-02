
import cv2
import numpy as np

class ImagePreprocessor:
    """
    Handles image preprocessing for HealthLens AI.
    Ensures images meet quality standards for AI analysis.
    """
    
    def __init__(self, target_size=(640, 640)):
        self.target_size = target_size
        
    def check_blur(self, image, threshold=100.0):
        """
        Uses Laplacian variance to detect blurry images.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
        return fm < threshold, fm

    def check_lighting(self, image, low_threshold=40, high_threshold=230):
        """
        Ensures lighting is adequate for visible symptoms.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        avg_brightness = np.mean(gray)
        
        if avg_brightness < low_threshold:
            return False, "Image too dark. Please add more lighting."
        if avg_brightness > high_threshold:
            return False, "Image too bright / overexposed."
        return True, "Good lighting."

    def preprocess(self, image_input):
        """
        Main pipeline for cleaning and validating the image.
        """
        if image_input is None:
            return None, "No image provided."

        # Convert to BGR for OpenCV
        img = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
        
        # 1. Check for blur
        is_blurry, score = self.check_blur(img)
        if is_blurry:
            return None, f"Image is too blurry (score: {score:.1f}). Please capture a steady, clear photo."
            
        # 2. Check lighting
        is_lit, msg = self.check_lighting(img)
        if not is_lit:
            return None, msg

        # 3. Resize maintaining aspect ratio
        h, w = img.shape[:2]
        ratio = min(self.target_size[0]/w, self.target_size[1]/h)
        new_size = (int(w * ratio), int(h * ratio))
        img_resized = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
        
        # 4. Enhance contrast slightly (CLAHE)
        lab = cv2.cvtColor(img_resized, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl,a,b))
        final_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

        # Convert back to RGB for Gradio display/Inference
        return cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB), "Image quality verified."

preprocessor = ImagePreprocessor()
