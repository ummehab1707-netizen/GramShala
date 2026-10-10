import json

lessons_path = "content/lessons.json"

with open(lessons_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for lesson in data.get("lessons", []):
    title_en = lesson["title"]["en"]
    title_hi = lesson["title"]["hi"]
    subj = lesson["subject"]["en"]
    cls = lesson.get("class", "Class 10")
    
    # Template to generate 10 questions per chapter
    q_templates = [
        ("What is the primary concept covered in {}?", "{} में मुख्य अवधारणा क्या है?", ["Core Principles", "Basic Definitions", "Advanced Calculations", "Historical Background"], 0),
        ("Which of the following is an essential rule in {}?", "{} में निम्नलिखित में से कौन सा एक आवश्यक नियम है?", ["Standard Formula", "Observation Rule", "Provisional Hypothesis", "Random Guessing"], 0),
        ("In practical problem solving for {}, what is the first step?", "{} के प्रश्नों को हल करने में पहला कदम क्या है?", ["Analyze Given Data", "Jump to Conclusion", "Ignore Units", "Skip Steps"], 0),
        ("Why is {} important in modern study?", "अध्ययन में {} का क्या महत्व है?", ["Builds Foundational Logic", "Only for Memory", "No Practical Use", "Historical Artifact"], 0),
        ("Which factor most directly influences outcomes in {}?", "{} में परिणामों को कौन सा कारक सबसे सीधे प्रभावित करता है?", ["System Variables", "External Noise", "Random Chance", "Page Number"], 0),
        ("What is a common property associated with {}?", "{} से जुड़ी एक सामान्य विशेषता क्या है?", ["Consistent Behavior", "Random Fluctuation", "Irrelevant Data", "Undefined State"], 0),
        ("How do we classify the key elements of {}?", "हम {} के प्रमुख तत्वों को कैसे वर्गीकृत करते हैं?", ["By Core Properties", "Alphabetically", "By Size Only", "At Random"], 0),
        ("Which tool or method is commonly used to study {}?", "{} का अध्ययन करने के लिए किस विधि का उपयोग किया जाता है?", ["Systematic Analysis", "Guess Work", "Trial without Observation", "Opinion Poll"], 0),
        ("What is the expected outcome when applying principles of {}?", "{} के सिद्धांतों को लागू करने पर क्या परिणाम मिलता है?", ["Accurate Results", "Unpredictable Error", "Contradiction", "Zero Output"], 0),
        ("Which statement accurately summarizes {}?", "{} का सही सारांश कौन सा कथन देता है?", ["Integrates Fundamental Ideas", "Contains No Rules", "Applies to Nothing", "Only Theoretical"], 0)
    ]
    
    quiz_10 = []
    for q_idx, (en_q, hi_q, opts, ans) in enumerate(q_templates):
        quiz_10.append({
            "q": {
                "en": f"{q_idx + 1}. " + en_q.format(title_en),
                "hi": f"{q_idx + 1}. " + hi_q.format(title_hi)
            },
            "choices": {
                "en": [f"A) {opts[0]}", f"B) {opts[1]}", f"C) {opts[2]}", f"D) {opts[3]}"],
                "hi": [f"A) {opts[0]}", f"B) {opts[1]}", f"C) {opts[2]}", f"D) {opts[3]}"]
            },
            "answer": ans
        })
        
    lesson["quiz"] = quiz_10

with open(lessons_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"🎉 Updated all {len(data['lessons'])} chapters with 10 questions each!")
