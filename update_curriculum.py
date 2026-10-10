import json
from pathlib import Path

curriculum = {
    "Class 10": {
        "Math": ["Real Numbers", "Sets", "Polynomials", "Pair of Linear Equations in Two Variables", "Quadratic Equations", "Progressions", "Coordinate Geometry", "Similar Triangles", "Tangents and Secants to a Circle", "Mensuration", "Trigonometry", "Applications of Trigonometry", "Probability", "Statistics"],
        "Physics": ["Reflection of Light at Curved Surfaces", "Chemical Equations and Reactions", "Acids, Bases and Salts", "Refraction of Light at Plane Surfaces", "Refraction of Light at Curved Surfaces", "Human Eye and Colourful World", "Structure of Atom", "Classification of Elements- The Periodic Table", "Chemical Bonding", "Electric Current", "Electromagnetism", "Principles of Metallurgy", "Carbon and its Compounds"],
        "Biology": ["Nutrition - Food supplying system", "Respiration - Energy producing system", "Transportation - The circulatory system", "Excretion - The wastage disposing system", "Coordination - The linking system", "Reproduction - The generating system", "Coordination in life processes", "Heredity - From parent to progeny", "Our environment - Our concern", "Natural resources"],
        "English": ["Attitude is Altitude", "Every Success Story Is also a Story of Great Failures", "I will Do It", "The Dear Departed (Part 1)", "The Dear Departed (Part 2)", "The Journey", "Another Woman", "The Storeyd House (Part 1)", "The Storeyd House (Part 2)"],
        "Social": ["India: Relief Features", "Ideas of Development", "Production and Employment", "Climate of India", "Indian Rivers and Water Resources", "The People", "Settlements - Migrations", "Rampur: A Village Economy", "Globalization", "Food Security"],
        "Hindi": ["बरसते बादल", "ईदगाह", "हम भारतवासी", "कण-कण का अधिकारी", "लोकगीत", "अंतरराष्ट्रीय स्तर पर हिंदी", "भक्ति पद", "स्वराज्य की नींव"]
    },
    "Class 9": {
        "Math": ["Number Systems", "Polynomials", "Coordinate Geometry", "Linear Equations in Two Variables", "Introduction to Euclid’s Geometry", "Lines and Angles", "Triangles", "Quadrilaterals", "Areas of Parallelograms and Triangles", "Circles", "Constructions", "Heron’s Formula", "Surface Areas and Volumes", "Statistics", "Probability"],
        "Physics": ["Matter in Our Surroundings", "Is Matter Around Us Pure?", "Atoms and Molecules", "Structure of the Atom", "Motion", "Force and Laws of Motion", "Gravitation", "Work and Energy", "Sound", "Improvement in Food Resources", "Natural Resources", "Environmental Management"],
        "Biology": ["The Fundamental Unit of Life", "Tissues", "Diversity in Living Organisms", "Why Do We Fall Ill?", "Natural Resources", "Improvement in Food Resources", "Nutrition", "Respiration", "Transportation", "Excretion"],
        "English": ["The Fun They Had", "The Sound of Music", "The Little Girl", "A Truly Beautiful Mind", "The Snake and the Mirror", "My Childhood", "Reach for the Top", "Kathmandu", "If I Were You"],
        "Social": ["The French Revolution", "Socialism in Europe and the Russian Revolution", "Nazism and the Rise of Hitler", "Forest Society and Colonialism", "Pastoralists in the Modern World", "India: Size and Location", "Physical Features of India", "Drainage", "Climate", "Natural Vegetation and Wildlife", "Population", "The Story of Village Palampur", "People as Resource", "Poverty as a Challenge", "Food Security in India", "What Is Democracy? Why Democracy?", "Constitutional Design", "Electoral Politics", "Working of Institutions", "Democratic Rights"],
        "Hindi": ["प्रेमचंद के फटे जूते", "दो बैलों की कथा", "ल्हासा की ओर", "उपभोक्तावाद की संस्कृति", "नाना साहब की पुत्री देवी मैना को भस्म कर दिया गया", "मेरे बचपन के दिन", "एक कुत्ता और एक मैना", "ग्राम श्री", "चंद्र गहना से लौटती बेर", "मेघ आए", "बच्चे काम पर जा रहे हैं"]
    },
    "Class 8": {
        "Math": ["Rational Numbers", "Linear Equations in One Variable", "Understanding Quadrilaterals", "Practical Geometry", "Data Handling", "Squares and Square Roots", "Cubes and Cube Roots", "Comparing Quantities", "Algebraic Expressions and Identities", "Visualising Solid Shapes", "Mensuration", "Exponents and Powers", "Direct and Inverse Proportions", "Factorisation", "Introduction to Graphs", "Playing with Numbers"],
        "Physics": ["Force and Pressure", "Friction", "Sound", "Chemical Effects of Electric Current", "Some Natural Phenomena", "Light", "Stars and the Solar System", "Pollution of Air and Water", "Coal and Petroleum", "Combustion and Flame", "Synthetic Fibres and Plastics", "Metals and Non-metals"],
        "Biology": ["Crop Production and Management", "Microorganisms: Friend and Foe", "Conservation of Plants and Animals", "Cell: Structure and Functions", "Reproduction in Animals", "Reaching the Age of Adolescence", "Food and Nutrition", "Health and Hygiene", "Biodiversity", "Ecosystems"],
        "English": ["The Best Christmas Present in the World", "The Tsunami", "Glimpses of the Past", "Bepin Choudhury’s Lapse of Memory", "The Summit Within", "This Is Jody’s Fawn", "A Visit to Cambridge", "A Short Monsoon Diary"],
        "Social": ["Resources", "Land, Soil, Water, Natural Vegetation and Wildlife Resources", "Mineral and Power Resources", "Agriculture", "Industries", "Human Resources", "How, When and Where", "From Trade to Territory", "Ruling the Countryside", "Tribals, Dikus and the Vision of a Golden Age", "When People Rebel", "Colonialism and the City", "Weavers, Iron Smelters and Factory Owners", "Civilising the Native, Educating the Nation", "Women, Caste and Reform", "The Making of the National Movement", "India After Independence", "The Indian Constitution", "Understanding Secularism", "Why Do We Need a Parliament?", "Understanding Laws", "Judiciary", "Understanding Our Criminal Justice System", "Understanding Marginalisation", "Confronting Marginalisation", "Public Facilities", "Law and Social Justice"],
        "Hindi": ["ध्वनि", "लाख की चूड़ियाँ", "बस की यात्रा", "दीवानों की हस्ती", "चिट्ठियों की अनूठी दुनिया", "भगवान के डाकिए", "क्या निराश हुआ जाए", "यह सबसे कठिन समय नहीं", "कबीर की साखियाँ", "कामचोर", "जब सिनेमा ने बोलना सीखा", "सुदामा चरित"]
    },
    "Class 7": {
        "Math": ["Integers", "Fractions and Decimals", "Data Handling", "Simple Equations", "Lines and Angles", "The Triangle and Its Properties", "Congruence of Triangles", "Comparing Quantities", "Rational Numbers", "Practical Geometry", "Perimeter and Area", "Algebraic Expressions", "Exponents and Powers", "Symmetry", "Visualising Solid Shapes"],
        "Science": ["Motion and Time", "Heat", "Acids, Bases and Salts", "Physical and Chemical Changes", "Electric Current and Its Effects", "Light", "Winds, Storms and Cyclones", "Soil", "Water", "Weather and Climate", "Electricity", "Reflection of Light", "Nutrition in Plants", "Nutrition in Animals", "Fibre to Fabric", "Respiration in Organisms", "Transportation in Animals and Plants", "Reproduction in Plants", "Forests: Our Lifeline", "Wastewater Story", "Microorganisms and Health", "Adaptations in Living Organisms"],
        "English": ["Three Questions", "A Gift of Chappals", "Gopal and the Hilsa-Fish", "The Ashes That Made Trees Bloom", "Quality", "Expert Detectives", "The Invention of Vita-Wonk", "Fire: Friend and Foe"],
        "Social": ["Environment", "Inside Our Earth", "Our Changing Earth", "Air", "Water", "Natural Vegetation and Wildlife", "Human Environment: Settlement, Transport and Communication", "Human Environment Interactions", "Life in the Deserts", "Tracing Changes Through a Thousand Years", "New Kings and Kingdoms", "The Delhi Sultans", "The Mughal Empire", "Tribes, Nomads and Settled Communities", "Devotional Paths to the Divine", "The Making of Regional Cultures", "Eighteenth-Century Political Formations", "On Equality", "Role of the Government in Health", "How the State Government Works", "Growing up as Boys and Girls", "Women Change the World", "Understanding Media", "Markets Around Us", "A Shirt in the Market", "Struggles for Equality"],
        "Hindi": ["हम पंछी उन्मुक्त गगन के", "दादी माँ", "हिमालय की बेटियाँ", "कठपुतली", "मिठाईवाला", "रक्त और हमारा शरीर", "पापा खो गए", "शाम – एक किसान", "चिड़िया की बच्ची", "अपूर्व अनुभव", "रहीम के दोहे", "कंचा"]
    },
    "Class 6": {
        "Math": ["Knowing Our Numbers", "Whole Numbers", "Playing with Numbers", "Basic Geometrical Ideas", "Understanding Elementary Shapes", "Integers", "Fractions", "Decimals", "Data Handling", "Mensuration", "Algebra", "Ratio and Proportion", "Symmetry", "Practical Geometry"],
        "Science": ["Measurement", "Motion", "Light, Shadows and Images", "Electricity and Circuits", "Magnets", "Separation of Substances", "Changes Around Us", "Air Around Us", "Water", "Fibre to Fabric", "Materials and Things", "Sorting Materials", "Simple Machines", "Food: Where Does It Come From?", "Components of Food", "Getting to Know Plants", "Body Movements", "The Living Organisms and Their Surroundings", "Garbage In, Garbage Out", "Our Food", "What Do Animals Eat?", "Habitat", "Human Body and Health"],
        "English": ["Who Did Patrick’s Homework?", "How the Dog Found Himself a New Master!", "Taro’s Reward", "An Indian–American Woman in Space: Kalpana Chawla", "A Different Kind of School", "Who I Am", "Fair Play", "A Game of Chance"],
        "Social": ["What, Where, How and When?", "On the Trail of the Earliest People", "From Gathering to Growing Food", "In the Earliest Cities", "What Books and Burials Tell Us", "Kingdoms, Kings and an Early Republic", "New Questions and Ideas", "Ashoka, the Emperor Who Gave Up War", "Vital Villages, Thriving Towns", "Traders, Kings and Pilgrims", "New Empires and Kingdoms", "Buildings, Paintings and Books", "The Earth in the Solar System", "Globe: Latitudes and Longitudes", "Motions of the Earth", "Maps", "Major Domains of the Earth", "India: My Country", "India: Climate, Vegetation and Wildlife", "Diversity and Discrimination", "What Is Government?", "Panchayati Raj", "Rural Administration", "Urban Administration", "Rural Livelihoods", "Urban Livelihoods"],
        "Hindi": ["वह चिड़िया जो", "बचपन", "नादान दोस्त", "चाँद से थोड़ी-सी गप्पें", "अक्षरों का महत्व", "पार नज़र के", "साथी हाथ बढ़ाना", "ऐसे-ऐसे", "टिकट-अलबम", "झाँसी की रानी", "जो देखकर भी नहीं देखते", "संसार पुस्तक है"]
    }
}

lessons_list = []
lesson_count = 1

for cls, subjects in curriculum.items():
    for subj, chap_list in subjects.items():
        for ch_idx, ch_title in enumerate(chap_list):
            lesson_id = f"{cls.lower().replace(' ', '')}-{subj.lower()}-{ch_idx+1}"
            lessons_list.append({
                "id": lesson_id,
                "class": cls,
                "subject": {"en": subj, "hi": subj},
                "title": {"en": f"Chapter {ch_idx+1}: {ch_title}", "hi": ch_title},
                "pages": [{"text": {"en": f"Core concepts for {ch_title}.", "hi": f"{ch_title} के मुख्य बिंदु।"}}],
                "quiz": [
                    {
                        "q": {"en": f"1. What is the main focus of {ch_title}?", "hi": f"1. {ch_title} का मुख्य विषय क्या है?"},
                        "choices": {"en": ["Core Principles", "Basic Concepts", "Advanced Theory", "Practical Applications"], "hi": ["मुख्य सिद्धांत", "मूल अवधारणाएँ", "उन्नत सिद्धांत", "व्यावहारिक अनुप्रयोग"]},
                        "answer": 0
                    }
                ]
            })

with open("content/lessons.json", "w", encoding="utf-8") as f:
    json.dump({"lessons": lessons_list}, f, ensure_ascii=False, indent=2)

print(f"✅ Created curriculum database with {len(lessons_list)} chapters across Class 10 to Class 6!")
