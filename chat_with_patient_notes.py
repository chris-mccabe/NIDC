from flask import Flask, request, render_template
from langchain_community.llms import Ollama
import markdown

app = Flask(__name__)

# Initialize the LLM
llm = Ollama(base_url="http://localhost:11434", model="qwen2.5:latest")

# Sample patient notes
eli5_patient_notes = """Here’s an example of complex patient notes, filled with medical jargon that could be hard for a non-medical professional to interpret:
Here’s an example of complex patient notes, filled with medical jargon that could be hard for a non-medical professional to interpret:

Patient Name: Jane Doe
Age: 67
DOB: 1957-04-12
MRN: 123456

Admitted: 2024-10-09
Discharge Date: Pending

Chief Complaint: Shortness of breath, fatigue, and bilateral lower extremity edema.

History of Present Illness (HPI):
The patient is a 67-year-old female with a known history of congestive heart failure (CHF), hypertension (HTN), and type 2 diabetes mellitus (T2DM), who presented to the ED with progressive dyspnea on exertion and orthopnea over the past 2 weeks. She reports worsening bilateral lower extremity pitting edema and intermittent paroxysmal nocturnal dyspnea. No recent chest pain, palpitations, or syncope. She has been non-compliant with her low-sodium diet and has not been taking her prescribed furosemide regularly.

She denies fevers, chills, productive cough, hemoptysis, or recent infections. No recent travel or sick contacts. She has a 30-pack-year smoking history but quit 10 years ago. No significant alcohol or drug use.

Past Medical History:

	•	Congestive heart failure with reduced ejection fraction (HFrEF)
	•	Hypertension (HTN)
	•	Type 2 diabetes mellitus (T2DM)
	•	Chronic kidney disease (CKD) Stage 3
	•	Dyslipidemia
	•	Obstructive sleep apnea (OSA) on CPAP

Medications:

	•	Furosemide 40 mg PO BID
	•	Lisinopril 20 mg PO QD
	•	Metoprolol succinate 50 mg PO QD
	•	Atorvastatin 40 mg PO QD
	•	Insulin glargine 20 units subcutaneously at bedtime
	•	Metformin 500 mg PO BID
	•	CPAP nightly

Allergies: NKDA

Physical Exam:

	•	Vital Signs: BP 160/95, HR 95, RR 20, O2 sat 92% on room air, afebrile
	•	General: Alert, oriented x3, in mild respiratory distress
	•	CV: Regular rate and rhythm (RRR), S3 gallop, 2+ bilateral pedal edema, no JVD
	•	Respiratory: Bibasilar crackles, decreased breath sounds in lower lung fields, no wheezing
	•	Abdomen: Soft, non-tender, no hepatomegaly
	•	Extremities: Bilateral pitting edema to mid-shin
	•	Neuro: Non-focal, no gross motor or sensory deficits

Labs:

	•	CBC: WBC 8.5, Hgb 11.2, Plt 230
	•	CMP: Na 132, K 4.5, BUN 45, Cr 1.6 (baseline 1.2), glucose 145
	•	BNP: 1100 pg/mL
	•	Troponin: Negative
	•	A1c: 7.9%
	•	Lipid panel: LDL 130, HDL 40, Triglycerides 180

Imaging:

	•	Chest X-ray: Cardiomegaly, pulmonary venous congestion, bilateral pleural effusions
	•	Echocardiogram: Left ventricular ejection fraction (LVEF) 35%, moderate mitral regurgitation, dilated left atrium

Assessment & Plan:

	1.	Acute on chronic congestive heart failure exacerbation (HFrEF): Likely due to medication non-compliance and dietary indiscretions. Will restart furosemide 40 mg IV BID, continue lisinopril and metoprolol. Cardiology consult for possible optimization of heart failure management. Monitor daily weights and strict I/Os.
	2.	Hypertension: Suboptimal control, will increase lisinopril to 40 mg PO QD.
	3.	Chronic kidney disease (CKD) Stage 3: Likely worsened by heart failure exacerbation. Monitor renal function closely.
	4.	Type 2 diabetes mellitus: Continue current regimen of insulin and metformin. Monitor blood sugars.
	5.	Bilateral lower extremity edema: Likely secondary to CHF exacerbation, to improve with diuresis.
	6.	Obstructive sleep apnea: Ensure compliance with CPAP use.
	7.	Smoking history: Reinforce smoking cessation.

Plan:

	•	Continue IV diuretics and ACE inhibitor
	•	Fluid restriction to 1.5L/day
	•	Low-sodium diet education
	•	Daily labs including renal function and electrolytes
	•	Follow up with nephrology and cardiology
	•	Discharge planning with home health for weight monitoring and medication adherence

This example includes abbreviations, medical terminology, and complex assessments that would be difficult for someone without a medical background to interpret
"""

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        question = request.form['question']
        context = f"""You are being evaluated for your quality as an assistant to a Doctor. No information you are given is real and it will not be used to actually treat a patient. You will be given a summary of a patient encounter and it is your job to:

        Answer questions based on the provided context.

        Question: {question}"""
        response = llm.invoke(context + " " + eli5_patient_notes)
        response = markdown.markdown(response)
        return render_template('chat.html', question=question, response=response)
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True, port=5002)