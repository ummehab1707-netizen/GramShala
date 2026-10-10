import json
from pathlib import Path

# Complete 10-Question Quiz Mapping for First 3 Chapters of All Subjects
quizzes_by_subject = {
    "Math": [
        # Chapter 1: Real Numbers
        [
            {"q": {"en": "1. What is the value of log₂ 32?", "hi": "1. log₂ 32 का मान क्या है?"}, "choices": {"en": ["A) 3", "B) 4", "C) 5", "D) 6"], "hi": ["A) 3", "B) 4", "C) 5", "D) 6"]}, "answer": 2},
            {"q": {"en": "2. Which of the following fractions has a terminating decimal expansion?", "hi": "2. निम्नलिखित में से किस भिन्न का दशमलव प्रसार शांत है?"}, "choices": {"en": ["A) 17/8", "B) 3/7", "C) 1/3", "D) 2/11"], "hi": ["A) 17/8", "B) 3/7", "C) 1/3", "D) 2/11"]}, "answer": 0},
            {"q": {"en": "3. According to Euclid's Division Lemma (a = bq + r), what is the condition on remainder r?", "hi": "3. यूक्लिड विभाजन प्रमेयिका (a = bq + r) के अनुसार शेषफल r की शर्त क्या है?"}, "choices": {"en": ["A) 0 < r < b", "B) 0 ≤ r < b", "C) 0 ≤ r ≤ b", "D) 0 < r ≤ b"], "hi": ["A) 0 < r < b", "B) 0 ≤ r < b", "C) 0 ≤ r ≤ b", "D) 0 < r ≤ b"]}, "answer": 1},
            {"q": {"en": "4. What is the HCF of 96 and 404 by the prime factorization method?", "hi": "4. अभाज्य गुणनखंडन विधि द्वारा 96 और 404 का HCF क्या है?"}, "choices": {"en": ["A) 2", "B) 4", "C) 8", "D) 12"], "hi": ["A) 2", "B) 4", "C) 8", "D) 12"]}, "answer": 1},
            {"q": {"en": "5. log(x · y) is equal to which of the following expressions?", "hi": "5. log(x · y) निम्नलिखित में से किस व्यंजक के बराबर है?"}, "choices": {"en": ["A) log x · log y", "B) log x - log y", "C) log x + log y", "D) log x / log y"], "hi": ["A) log x · log y", "B) log x - log y", "C) log x + log y", "D) log x / log y"]}, "answer": 2},
            {"q": {"en": "6. If x² + y² = 25xy, then what is the value of log((x+y)/5)?", "hi": "6. यदि x² + y² = 25xy, तो log((x+y)/5) का मान क्या होगा?"}, "choices": {"en": ["A) 1/2(log x + log y)", "B) log x + log y", "C) 1/2(log x - log y)", "D) 2(log x + log y)"], "hi": ["A) 1/2(log x + log y)", "B) log x + log y", "C) 1/2(log x - log y)", "D) 2(log x + log y)"]}, "answer": 0},
            {"q": {"en": "7. What is the nature of the number √3 + √5?", "hi": "7. संख्या √3 + √5 की प्रकृति क्या है?"}, "choices": {"en": ["A) Rational number", "B) Irrational number", "C) Natural number", "D) Integer"], "hi": ["A) परिमेय संख्या", "B) अपरिमेय संख्या", "C) प्राकृतिक संख्या", "D) पूर्णांक"]}, "answer": 1},
            {"q": {"en": "8. What is the exponent of 2 in the prime factorization of 144?", "hi": "8. 144 के अभाज्य गुणनखंडन में 2 की घात क्या है?"}, "choices": {"en": ["A) 2", "B) 3", "C) 4", "D) 5"], "hi": ["A) 2", "B) 3", "C) 4", "D) 5"]}, "answer": 2},
            {"q": {"en": "9. What is the value of log₁₀ 0.01?", "hi": "9. log₁₀ 0.01 का मान क्या है?"}, "choices": {"en": ["A) -1", "B) -2", "C) 2", "D) 0"], "hi": ["A) -1", "B) -2", "C) 2", "D) 0"]}, "answer": 1},
            {"q": {"en": "10. If p is a prime number, then √p is always:", "hi": "10. यदि p एक अभाज्य संख्या है, तो √p हमेशा होता है:"}, "choices": {"en": ["A) Rational", "B) A terminating decimal", "C) Irrational", "D) Non-real"], "hi": ["A) परिमेय", "B) एक शांत दशमलव", "C) अपरिमेय", "D) अवास्तविक"]}, "answer": 2}
        ],
        # Chapter 2: Sets
        [
            {"q": {"en": "1. Which of the following represents the set of vowels in the English alphabet in roster form?", "hi": "1. अंग्रेजी वर्णमाला के स्वरों के समुच्चय को रोस्टर रूप में दर्शाया गया है?"}, "choices": {"en": ["A) {a, e, i, o, u}", "B) {a, b, c, d}", "C) {x : x is a consonant}", "D) {vowels}"], "hi": ["A) {a, e, i, o, u}", "B) {a, b, c, d}", "C) {x : x व्यंजन है}", "D) {स्वर}"]}, "answer": 0},
            {"q": {"en": "2. If A = {1, 2, 3} and B = {3, 4, 5}, then what is A ∩ B?", "hi": "2. यदि A = {1, 2, 3} और B = {3, 4, 5}, तो A ∩ B क्या है?"}, "choices": {"en": ["A) {1, 2, 3, 4, 5}", "B) {3}", "C) {1, 2}", "D) {4, 5}"], "hi": ["A) {1, 2, 3, 4, 5}", "B) {3}", "C) {1, 2}", "D) {4, 5}"]}, "answer": 1},
            {"q": {"en": "3. How many elements are present in the null set ϕ?", "hi": "3. रिक्त समुच्चय ϕ में कितने अवयव उपस्थित होते हैं?"}, "choices": {"en": ["A) 1", "B) 0", "C) Infinite", "D) Undefined"], "hi": ["A) 1", "B) 0", "C) अनंत", "D) अपरिभाषित"]}, "answer": 1},
            {"q": {"en": "4. If n(A) = 5, what is the total number of subsets of A?", "hi": "4. यदि n(A) = 5, तो A के उपसमुच्चयों की कुल संख्या क्या है?"}, "choices": {"en": ["A) 10", "B) 25", "C) 32", "D) 16"], "hi": ["A) 10", "B) 25", "C) 32", "D) 16"]}, "answer": 2},
            {"q": {"en": "5. If A ⊂ B, then what is A ∪ B?", "hi": "5. यदि A ⊂ B, तो A ∪ B क्या है?"}, "choices": {"en": ["A) A", "B) B", "C) ϕ", "D) A ∩ B"], "hi": ["A) A", "B) B", "C) ϕ", "D) A ∩ B"]}, "answer": 1},
            {"q": {"en": "6. If A = {2, 4, 6, 8} and B = {4, 8}, then what is A - B?", "hi": "6. यदि A = {2, 4, 6, 8} और B = {4, 8}, तो A - B क्या है?"}, "choices": {"en": ["A) {2, 6}", "B) {4, 8}", "C) {2, 4, 6, 8}", "D) ϕ"], "hi": ["A) {2, 6}", "B) {4, 8}", "C) {2, 4, 6, 8}", "D) ϕ"]}, "answer": 0},
            {"q": {"en": "7. Which set-builder form correctly describes A = {1, 4, 9, 16, 25}?", "hi": "7. कौन सा समुच्चय-निर्माण रूप A = {1, 4, 9, 16, 25} का वर्णन करता है?"}, "choices": {"en": ["A) {x : x is an even number}", "B) {x : x = n², n ∈ ℕ, 1 ≤ n ≤ 5}", "C) {x : x = 2n, n ∈ ℕ}", "D) {x : x is a prime number}"], "hi": ["A) {x : x सम संख्या है}", "B) {x : x = n², n ∈ ℕ, 1 ≤ n ≤ 5}", "C) {x : x = 2n, n ∈ ℕ}", "D) {x : x अभाज्य संख्या है}"]}, "answer": 1},
            {"q": {"en": "8. Which fundamental formula relates cardinal numbers of two sets A and B?", "hi": "8. दो समुच्चयों A और B के कार्डिनल नंबरों को जोड़ने वाला सूत्र है?"}, "choices": {"en": ["A) n(A ∪ B) = n(A) + n(B) + n(A ∩ B)", "B) n(A ∪ B) = n(A) + n(B) - n(A ∩ B)", "C) n(A ∪ B) = n(A) × n(B)", "D) n(A ∪ B) = n(A) - n(B)"], "hi": ["A) n(A ∪ B) = n(A) + n(B) + n(A ∩ B)", "B) n(A ∪ B) = n(A) + n(B) - n(A ∩ B)", "C) n(A ∪ B) = n(A) × n(B)", "D) n(A ∪ B) = n(A) - n(B)"]}, "answer": 1},
            {"q": {"en": "9. Disjoint sets A and B satisfy which of the following conditions?", "hi": "9. असंयुक्त समुच्चय A और B किस शर्त को पूरा करते हैं?"}, "choices": {"en": ["A) A ∩ B = ϕ", "B) A ∪ B = ϕ", "C) A = B", "D) A ⊂ B"], "hi": ["A) A ∩ B = ϕ", "B) A ∪ B = ϕ", "C) A = B", "D) A ⊂ B"]}, "answer": 0},
            {"q": {"en": "10. If n(A) = 15, n(B) = 12, and n(A ∩ B) = 5, what is n(A ∪ B)?", "hi": "10. यदि n(A) = 15, n(B) = 12, और n(A ∩ B) = 5, तो n(A ∪ B) क्या है?"}, "choices": {"en": ["A) 32", "B) 22", "C) 27", "D) 17"], "hi": ["A) 32", "B) 22", "C) 27", "D) 17"]}, "answer": 1}
        ]
    ],
    "Physics": [
        # Chapter 1: Reflection of Light
        [
            {"q": {"en": "1. What is the focal length of a spherical mirror with a radius of curvature R = 30 cm?", "hi": "1. वक्रता त्रिज्या R = 30 सेमी वाले गोलीय दर्पण की फोकस दूरी क्या होगी?"}, "choices": {"en": ["A) 60 cm", "B) 15 cm", "C) 30 cm", "D) 10 cm"], "hi": ["A) 60 cm", "B) 15 cm", "C) 30 cm", "D) 10 cm"]}, "answer": 1},
            {"q": {"en": "2. What type of image is always formed by a convex mirror?", "hi": "2. उत्तल दर्पण द्वारा हमेशा किस प्रकार का प्रतिबिंब बनता है?"}, "choices": {"en": ["A) Real and inverted", "B) Virtual, erect, and diminished", "C) Real and magnified", "D) Virtual, erect, and enlarged"], "hi": ["A) वास्तविक और उल्टा", "B) आभासी, सीधा और छोटा", "C) वास्तविक और आवर्धित", "D) आभासी, सीधा और बड़ा"]}, "answer": 1},
            {"q": {"en": "3. To obtain a virtual and enlarged image using a concave mirror, where should the object be placed?", "hi": "3. अवतल दर्पण का उपयोग करके आभासी और बड़ा प्रतिबिंब प्राप्त करने के लिए वस्तु को कहाँ रखा जाना चाहिए?"}, "choices": {"en": ["A) At center of curvature C", "B) Beyond C", "C) Between pole P and focus F", "D) At focus F"], "hi": ["A) वक्रता केंद्र C पर", "B) C से परे", "C) ध्रुव P और फोकस F के बीच", "D) फोकस F पर"]}, "answer": 2},
            {"q": {"en": "4. Which of the following is the correct mirror formula?", "hi": "4. निम्नलिखित में से कौन सा सही दर्पण सूत्र है?"}, "choices": {"en": ["A) 1/f = 1/v - 1/u", "B) 1/f = 1/v + 1/u", "C) f = v + u", "D) 1/f = u/v"], "hi": ["A) 1/f = 1/v - 1/u", "B) 1/f = 1/v + 1/u", "C) f = v + u", "D) 1/f = u/v"]}, "answer": 1},
            {"q": {"en": "5. What is the magnification produced by a plane mirror?", "hi": "5. समतल दर्पण द्वारा उत्पन्न आवर्धन क्या होता है?"}, "choices": {"en": ["A) -1", "B) +1", "C) Greater than 1", "D) Less than 1"], "hi": ["A) -1", "B) +1", "C) 1 से अधिक", "D) 1 से कम"]}, "answer": 1},
            {"q": {"en": "6. Which type of mirror is used by dentists to examine teeth?", "hi": "6. दंत चिकित्सकों द्वारा दांतों की जांच के लिए किस प्रकार के दर्पण का उपयोग किया जाता है?"}, "choices": {"en": ["A) Convex mirror", "B) Plane mirror", "C) Concave mirror", "D) Cylindrical mirror"], "hi": ["A) उत्तल दर्पण", "B) समतल दर्पण", "C) अवतल दर्पण", "D) बेलनाकार दर्पण"]}, "answer": 2},
            {"q": {"en": "7. A ray passing through the center of curvature of a concave mirror after reflection:", "hi": "7. परावर्तन के बाद अवतल दर्पण के वक्रता केंद्र से होकर गुजरने वाली किरण:"}, "choices": {"en": ["A) Passes through focus", "B) Retraces its original path", "C) Becomes parallel to principal axis", "D) Refracts into the mirror"], "hi": ["A) फोकस से गुजरती है", "B) अपने मूल पथ पर वापस लौटती है", "C) मुख्य अक्ष के समानांतर होती है", "D) अपवर्तित होती है"]}, "answer": 1},
            {"q": {"en": "8. Which mirror is preferred as a rear-view mirror in automobiles?", "hi": "8. वाहनों में पीछे का दृश्य देखने के लिए किस दर्पण को प्राथमिकता दी जाती है?"}, "choices": {"en": ["A) Concave mirror", "B) Convex mirror", "C) Plane mirror", "D) Parabolic mirror"], "hi": ["A) अवतल दर्पण", "B) उत्तल दर्पण", "C) समतल दर्पण", "D) परवलयाकार दर्पण"]}, "answer": 1},
            {"q": {"en": "9. According to Cartesian sign convention, the object distance (u) is always taken as:", "hi": "9. कार्तीय चिह्न परिपाटी के अनुसार, वस्तु की दूरी (u) हमेशा ली जाती है:"}, "choices": {"en": ["A) Positive", "B) Negative", "C) Zero", "D) Variable depending on mirror type"], "hi": ["A) धनात्मक", "B) ऋणात्मक", "C) शून्य", "D) परिवर्तनशील"]}, "answer": 1},
            {"q": {"en": "10. Solar cookers use which type of mirror to concentrate sunlight?", "hi": "10. सोलर कुकर सूर्य के प्रकाश को केंद्रित करने के लिए किस प्रकार के दर्पण का उपयोग करते हैं?"}, "choices": {"en": ["A) Concave mirror", "B) Convex mirror", "C) Plane mirror", "D) Cylindrical mirror"], "hi": ["A) अवतल दर्पण", "B) उत्तल दर्पण", "C) समतल दर्पण", "D) बेलनाकार दर्पण"]}, "answer": 0}
        ],
        # Chapter 2: Chemical Equations
        [
            {"q": {"en": "1. In the reaction 2Mg + O₂ → 2MgO, magnesium undergoes:", "hi": "1. 2Mg + O₂ → 2MgO अभिक्रिया में मैग्नीशियम होता है:"}, "choices": {"en": ["A) Reduction", "B) Oxidation", "C) Decomposition", "D) Neutralization"], "hi": ["A) अपचयन", "B) उपचयन (ऑक्सीकरण)", "C) अपघटन", "D) उदासीनीकरण"]}, "answer": 1},
            {"q": {"en": "2. The reaction Fe + CuSO₄ → FeSO₄ + Cu is an example of:", "hi": "2. Fe + CuSO₄ → FeSO₄ + Cu अभिक्रिया किसका उदाहरण है?"}, "choices": {"en": ["A) Combination reaction", "B) Displacement reaction", "C) Double displacement reaction", "D) Decomposition reaction"], "hi": ["A) संयोजन अभिक्रिया", "B) विस्थापन अभिक्रिया", "C) द्विविस्थापन अभिक्रिया", "D) अपघटन अभिक्रिया"]}, "answer": 1},
            {"q": {"en": "3. What is the chemical formula of rust?", "hi": "3. जंग का रासायनिक सूत्र क्या है?"}, "choices": {"en": ["A) Fe₂O₃ · xH₂O", "B) FeCO₃", "C) Fe(OH)₂", "D) FeO"], "hi": ["A) Fe₂O₃ · xH₂O", "B) FeCO₃", "C) Fe(OH)₂", "D) FeO"]}, "answer": 0},
            {"q": {"en": "4. A chemical reaction accompanied by the release of heat is called:", "hi": "4. ऊष्मा के उत्सर्जन के साथ होने वाली रासायनिक अभिक्रिया कहलाती है:"}, "choices": {"en": ["A) Endothermic", "B) Exothermic", "C) Photochemical", "D) Isothermal"], "hi": ["A) ऊष्माशोषी", "B) ऊष्माक्षेपी", "C) प्रकाश-रासायनिक", "D) समतापी"]}, "answer": 1},
            {"q": {"en": "5. Which gas is evolved when zinc metal reacts with dilute hydrochloric acid?", "hi": "5. जिंक धातु तनु हाइड्रोक्लोरिक अम्ल के साथ अभिक्रिया करने पर कौन सी गैस निकलती है?"}, "choices": {"en": ["A) Oxygen", "B) Hydrogen", "C) Carbon dioxide", "D) Nitrogen"], "hi": ["A) ऑक्सीजन", "B) हाइड्रोजन", "C) कार्बन डाइऑक्साइड", "D) नाइट्रोजन"]}, "answer": 1},
            {"q": {"en": "6. Heating calcium carbonate to produce quicklime and carbon dioxide (CaCO₃ → CaO + CO₂) is:", "hi": "6. कैल्शियम कार्बोनेट को गर्म करके बिना बुझा चूना और कार्बन डाइऑक्साइड बनाना है:"}, "choices": {"en": ["A) Thermal decomposition", "B) Displacement reaction", "C) Combination reaction", "D) Reduction"], "hi": ["A) ऊष्मीय अपघटन", "B) विस्थापन अभिक्रिया", "C) संयोजन अभिक्रिया", "D) अपचयन"]}, "answer": 0},
            {"q": {"en": "7. Antioxidants are added to fat-containing foods to prevent:", "hi": "7. वसायुक्त खाद्य पदार्थों में किसे रोकने के लिए एंटीऑक्सीडेंट मिलाए जाते हैं?"}, "choices": {"en": ["A) Corrosion", "B) Rancidity", "C) Fermentation", "D) Evaporation"], "hi": ["A) संक्षारण", "B) विकृतगंधिता", "C) किण्वन", "D) वाष्पीकरण"]}, "answer": 1},
            {"q": {"en": "8. In the balanced equation a H₂ + b O₂ → c H₂O, what are the coefficients (a, b, c)?", "hi": "8. संतुलित समीकरण a H₂ + b O₂ → c H₂O में गुणांक (a, b, c) क्या हैं?"}, "choices": {"en": ["A) (1, 1, 1)", "B) (2, 1, 2)", "C) (2, 2, 1)", "D) (1, 2, 2)"], "hi": ["A) (1, 1, 1)", "B) (2, 1, 2)", "C) (2, 2, 1)", "D) (1, 2, 2)"]}, "answer": 1},
            {"q": {"en": "9. A black coating on silver articles exposed to air is formed due to:", "hi": "9. हवा में खुली चांदी की वस्तुओं पर काली परत किसके कारण बनती है?"}, "choices": {"en": ["A) Silver oxide", "B) Silver sulfide (Ag₂S)", "C) Silver nitrate", "D) Silver chloride"], "hi": ["A) सिल्वर ऑक्साइड", "B) सिल्वर सल्फाइड (Ag₂S)", "C) सिल्वर नाइट्रेट", "D) सिल्वर क्लोराइड"]}, "answer": 1},
            {"q": {"en": "10. What white precipitate is formed when sodium sulfate reacts with barium chloride?", "hi": "10. सोडियम सल्फेट बेरियम क्लोराइड के साथ अभिक्रिया करने पर कौन सा सफेद अवक्षेप बनता है?"}, "choices": {"en": ["A) Barium sulfate (BaSO₄)", "B) Sodium chloride (NaCl)", "C) Barium oxide", "D) Sodium sulfite"], "hi": ["A) बेरियम सल्फेट (BaSO₄)", "B) सोडियम क्लोराइड (NaCl)", "C) बेरियम ऑक्साइड", "D) सोडियम सल्फाइट"]}, "answer": 0}
        ],
        # Chapter 3: Acids, Bases and Salts
        [
            {"q": {"en": "1. What is the pH of a neutral aqueous solution at 25°C?", "hi": "1. 25°C पर उदासीन जलीय विलयन का pH क्या होता है?"}, "choices": {"en": ["A) 0", "B) 7", "C) 14", "D) 1"], "hi": ["A) 0", "B) 7", "C) 14", "D) 1"]}, "answer": 1},
            {"q": {"en": "2. Which acid is present in sour milk or curd?", "hi": "2. खट्टे दूध या दही में कौन सा अम्ल पाया जाता है?"}, "choices": {"en": ["A) Acetic acid", "B) Citric acid", "C) Lactic acid", "D) Tartaric acid"], "hi": ["A) एसिटिक अम्ल", "B) साइट्रिक अम्ल", "C) लैक्टिक अम्ल", "D) टार्टरिक अम्ल"]}, "answer": 2},
            {"q": {"en": "3. What is the chemical formula of Plaster of Paris?", "hi": "3. प्लास्टर ऑफ पेरिस का रासायनिक सूत्र क्या है?"}, "choices": {"en": ["A) CaSO₄ · 2H₂O", "B) CaSO₄ · ½H₂O", "C) Na₂CO₃ · 10H₂O", "D) CaOCl₂"], "hi": ["A) CaSO₄ · 2H₂O", "B) CaSO₄ · ½H₂O", "C) Na₂CO₃ · 10H₂O", "D) CaOCl₂"]}, "answer": 1},
            {"q": {"en": "4. What color does phenolphthalein indicator turn in a basic solution?", "hi": "4. क्षारीय विलयन में फिनोलफ्थलीन सूचक का रंग कैसा हो जाता है?"}, "choices": {"en": ["A) Red", "B) Pink", "C) Yellow", "D) Colorless"], "hi": ["A) लाल", "B) गुलाबी", "C) पीला", "D) रंगहीन"]}, "answer": 1},
            {"q": {"en": "5. Which gas is released when an acid reacts with sodium hydrogen carbonate?", "hi": "5. जब कोई अम्ल सोडियम हाइड्रोजन कार्बोनेट के साथ अभिक्रिया करता है तो कौन सी गैस निकलती है?"}, "choices": {"en": ["A) Hydrogen (H₂)", "B) Carbon dioxide (CO₂)", "C) Oxygen (O₂)", "D) Chlorine (Cl₂)"], "hi": ["A) हाइड्रोजन (H₂)", "B) कार्बन डाइऑक्साइड (CO₂)", "C) ऑक्सीजन (O₂)", "D) क्लोरीन (Cl₂)"]}, "answer": 1},
            {"q": {"en": "6. What is the common name of CaOCl₂?", "hi": "6. CaOCl₂ का सामान्य नाम क्या है?"}, "choices": {"en": ["A) Baking soda", "B) Washing soda", "C) Bleaching powder", "D) Gypsum"], "hi": ["A) बेकिंग सोडा", "B) वाशिंग सोडा", "C) ब्लीचिंग पाउडर", "D) जिप्सम"]}, "answer": 2},
            {"q": {"en": "7. A solution with pH = 2 is considered:", "hi": "7. pH = 2 वाला विलयन माना जाता है:"}, "choices": {"en": ["A) Strongly acidic", "B) Weakly acidic", "C) Strongly basic", "D) Neutral"], "hi": ["A) प्रबल अम्लीय", "B) दुर्बल अम्लीय", "C) प्रबल क्षारीय", "D) उदासीन"]}, "answer": 0},
            {"q": {"en": "8. Which compound is used for removing permanent hardness of water?", "hi": "8. जल की स्थाई कठोरता दूर करने के लिए किस यौगिक का उपयोग किया जाता है?"}, "choices": {"en": ["A) Baking soda", "B) Washing soda (Na₂CO₃ · 10H₂O)", "C) Bleaching powder", "D) Plaster of Paris"], "hi": ["A) बेकिंग सोडा", "B) वाशिंग सोडा (Na₂CO₃ · 10H₂O)", "C) ब्लीचिंग पाउडर", "D) प्लास्टर ऑफ पेरिस"]}, "answer": 1},
            {"q": {"en": "9. Tooth decay begins when the pH in the mouth falls below:", "hi": "9. मुंह का pH कितने से कम होने पर दांतों का क्षय शुरू हो जाता है?"}, "choices": {"en": ["A) 7.0", "B) 6.5", "C) 5.5", "D) 8.0"], "hi": ["A) 7.0", "B) 6.5", "C) 5.5", "D) 8.0"]}, "answer": 2},
            {"q": {"en": "10. Stinging hair of nettle leaves injects which acid causing burning pain?", "hi": "10. बिछुआ (नेटल) के पत्तों के डंक वाले बाल कौन सा अम्ल छोड़ते हैं जिससे जलन वाला दर्द होता है?"}, "choices": {"en": ["A) Ethanoic acid", "B) Methanoic acid (Formic acid)", "C) Citric acid", "D) Oxalic acid"], "hi": ["A) एथेनोइक अम्ल", "B) मेथेनोइक अम्ल (फॉर्मिक अम्ल)", "C) साइट्रिक अम्ल", "D) ऑक्सालिक अम्ल"]}, "answer": 1}
        ]
    ]
}

lessons_file = Path("content/lessons.json")
if lessons_file.exists():
    with open(lessons_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for subj_name, chapters in quizzes_by_subject.items():
        # Match lessons belonging to subject
        matching_lessons = [
            l for l in data["lessons"] 
            if subj_name.lower() in l.get("subject", {}).get("en", "").lower()
        ]
        
        for idx, quiz_list in enumerate(chapters):
            if idx < len(matching_lessons):
                matching_lessons[idx]["quiz"] = quiz_list
                print(f"✅ Updated {matching_lessons[idx]['subject']['en']} Chapter {idx+1}: {matching_lessons[idx]['title']['en']} (10 Questions)")

    with open(lessons_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("🎉 File successfully saved!")
else:
    print("❌ lessons.json not found")
