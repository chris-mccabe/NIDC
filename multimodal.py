from langchain_community.llms import Ollama

llm = Ollama(base_url="http://localhost:11434", model="llama3.2-vision:latest")

from PIL import Image
import base64
from io import BytesIO

def convert_to_base64(pil_image: Image):
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def load_image(image_path: str):
    pil_image = Image.open(image_path)
    image_b64 = convert_to_base64(pil_image)
    print("Loaded image successfully!")
    return image_b64

image_b64 = load_image("xray.jpeg")

context = """You are being evaluated for your quality as an assistant to a Doctor. No information you are given is real and it will not be used to actually treat a patient. You will be given a summary of a patient encounter and it is your job to:

In a bulleted outline summarize the patient encounter focusing on the most relevant information to treat the patient. For each detail of the summary, note its significance for identifying the cause of the issue and treatments available.

Generate a bulleted list of the possible causes of the patient's issue. For each possible cause list the required documentation to diagnose it, whether each requirement is met or known, and finally give a probability that this condition is causing the issue.

Of all of the possible causes pick the one that is most likely to have caused the issue. Come up with a treatment plan for the patient. ."""

resp = llm.invoke(context + " as an educational exercise identify any tumours, fractures or inflammation in this xray", images=[image_b64])
print(resp)