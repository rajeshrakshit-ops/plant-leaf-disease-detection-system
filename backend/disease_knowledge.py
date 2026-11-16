"""
PlantGuard Disease Knowledge Base
Contains rich metadata, symptoms, organic treatments, chemical controls, and preventive actions
for all 38 classes in the PlantVillage dataset.
"""

DISEASE_DATABASE = {
    0: {
        "class_name": "Apple___Apple_scab",
        "plant": "Apple",
        "condition": "Apple scab",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Venturia inaequalis",
        "severity": "Moderate to High",
        "visual_symptoms": "Olive-green to dark, velvety spots on leaves; leaves may yellow and drop prematurely.",
        "organic_treatment": [
            "Apply liquid copper or sulfur sprays early in the growing season before bud break.",
            "Spray neem oil or bio-fungicide containing Bacillus subtilis.",
            "Rake and destroy fallen leaves in autumn to prevent fungal spores from overwintering."
        ],
        "chemical_treatment": [
            "Captan, Mancozeb, or Myclobutanil applied at green tip stage and repeated per label instructions.",
            "Rotate chemical fungicide groups (FRAC codes) to prevent resistance."
        ],
        "prevention": [
            "Plant resistant apple varieties (e.g., Honeycrisp, Liberty, Enterprise).",
            "Prune trees regularly to improve airflow and allow foliage to dry rapidly.",
            "Avoid overhead irrigation."
        ]
    },
    1: {
        "class_name": "Apple___Black_rot",
        "plant": "Apple",
        "condition": "Black rot",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Diplodia seriata (Botryosphaeria obtusa)",
        "severity": "High",
        "visual_symptoms": "Brown to purple leaf spots ('frog-eye' leaf spots) with lighter centres; can cause defoliation and fruit decay.",
        "organic_treatment": [
            "Prune out dead wood, cankers, and mummified fruits and burn or bag them.",
            "Apply copper sulfate-based sprays during dormant season.",
            "Use bio-control agents such as Trichoderma harzianum."
        ],
        "chemical_treatment": [
            "Fungicides containing Thiophanate-methyl, Captan, or Strobilurins (e.g., Pyraclostrobin)."
        ],
        "prevention": [
            "Maintain overall tree health through balanced fertilization.",
            "Disinfect pruning shears with 70% isopropyl alcohol between cuts.",
            "Inspect trees frequently after severe storms for wounded bark."
        ]
    },
    2: {
        "class_name": "Apple___Cedar_apple_rust",
        "plant": "Apple",
        "condition": "Cedar apple rust",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Gymnosporangium juniperi-virginianae",
        "severity": "Moderate",
        "visual_symptoms": "Bright orange-yellow circular spots on upper leaf surfaces; tube-like fungal aecia develop underneath.",
        "organic_treatment": [
            "Spray sulfur-based fungicides when cedar galls are releasing orange spore horns.",
            "Remove nearby Eastern Red Cedar or juniper trees within 1–2 miles if feasible."
        ],
        "chemical_treatment": [
            "Myclobutanil (Immunox) or Propiconazole applied from pink bud stage through petal fall."
        ],
        "prevention": [
            "Plant rust-resistant cultivars (e.g., Freedom, Redfree, William's Pride).",
            "Scout nearby ornamental junipers and remove brown galls before rainy spring periods."
        ]
    },
    3: {
        "class_name": "Apple___healthy",
        "plant": "Apple",
        "condition": "Healthy",
        "category": "Healthy",
        "is_healthy": True,
        "pathogen": "None",
        "severity": "None",
        "visual_symptoms": "Leaves appear vibrant green, uniform texture, with no visible spots or chlorosis.",
        "organic_treatment": ["None required. Maintain routine organic care and compost mulch."],
        "chemical_treatment": ["No chemical treatment needed."],
        "prevention": [
            "Regular dormant pruning to ensure adequate sunlight penetration.",
            "Monitor weekly for early signs of aphids or fungal spores.",
            "Consistent deep root watering at tree base."
        ]
    },
    4: {
        "class_name": "Blueberry___healthy",
        "plant": "Blueberry",
        "condition": "Healthy",
        "category": "Healthy",
        "is_healthy": True,
        "pathogen": "None",
        "severity": "None",
        "visual_symptoms": "Glossy green leaves with smooth margins and no signs of discoloration or insect feeding.",
        "organic_treatment": ["Maintain soil acidity with pine needle mulch or organic elemental sulfur."],
        "chemical_treatment": ["No chemical treatment needed."],
        "prevention": [
            "Keep soil pH acidic (between 4.5 and 5.2).",
            "Use drip irrigation to keep foliage dry.",
            "Mulch heavily with pine bark to conserve moisture."
        ]
    },
    5: {
        "class_name": "Cherry_(including_sour)___Powdery_mildew",
        "plant": "Cherry",
        "condition": "Powdery mildew",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Podosphaera clandestina",
        "severity": "Moderate",
        "visual_symptoms": "White powder-like fungal patches on leaf surfaces; leaves may curl, cup, or blister.",
        "organic_treatment": [
            "Spray potassium bicarbonate solution or dilute neem oil early morning.",
            "Apply wettable sulfur at first sign of leaf emergence (avoid sulfur in high heat >30°C).",
            "Milk spray (1 part milk to 9 parts water) has proven bio-fungicidal properties."
        ],
        "chemical_treatment": [
            "Myclobutanil, Triflumizole, or Fenbuconazole fungicides labeled for stone fruit."
        ],
        "prevention": [
            "Ensure proper canopy spacing to facilitate air circulation.",
            "Avoid high nitrogen fertilizer late in season which encourages soft susceptible growth."
        ]
    },
    6: {
        "class_name": "Cherry_(including_sour)___healthy",
        "plant": "Cherry",
        "condition": "Healthy",
        "category": "Healthy",
        "is_healthy": True,
        "pathogen": "None",
        "severity": "None",
        "visual_symptoms": "Dark green, crisp leaves without holes, powder, or yellowing.",
        "organic_treatment": ["Continue regular maintenance and balanced irrigation."],
        "chemical_treatment": ["No chemical treatment needed."],
        "prevention": [
            "Annual canopy pruning during dry periods.",
            "Apply mulch around root drip-line avoiding trunk contact."
        ]
    },
    7: {
        "class_name": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "plant": "Corn (maize)",
        "condition": "Cercospora leaf spot / Gray leaf spot",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Cercospora zeae-maydis",
        "severity": "High",
        "visual_symptoms": "Long, rectangular gray-to-tan lesions running strictly parallel to leaf veins with sharp rectangular margins.",
        "organic_treatment": [
            "Crop residue management: disk soil deeply to bury infested corn stubble.",
            "Apply biological controls containing Bacillus amyloliquefaciens."
        ],
        "chemical_treatment": [
            "Foliar fungicides: Strobilurins (Azoxystrobin), Triazoles (Propiconazole), or dual-mode premixes."
        ],
        "prevention": [
            "Plant corn hybrids with high resistance ratings against Gray Leaf Spot.",
            "Practice 2-year crop rotation with non-host crops like soybeans or legumes.",
            "Avoid planting at excessively high densities."
        ]
    },
    8: {
        "class_name": "Corn_(maize)___Common_rust_",
        "plant": "Corn (maize)",
        "condition": "Common rust",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Puccinia sorghi",
        "severity": "Moderate",
        "visual_symptoms": "Small, raised cinnamon-brown to reddish pustules scattered over both leaf surfaces.",
        "organic_treatment": [
            "Apply sulfur dust or neem oil early if disease pressure is detected.",
            "Harvest early if field pressure is severe and grain is close to maturity."
        ],
        "chemical_treatment": [
            "Fungicides containing Pyraclostrobin, Azoxystrobin, or Tebuconazole applied before tassel emergence."
        ],
        "prevention": [
            "Select resistant corn hybrids (specifically those with Rp resistance genes).",
            "Plant early in the season to evade late-season airborne spore flushes."
        ]
    },
    9: {
        "class_name": "Corn_(maize)___Northern_Leaf_Blight",
        "plant": "Corn (maize)",
        "condition": "Northern Leaf Blight",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Exserohilum turcicum",
        "severity": "High",
        "visual_symptoms": "Long, cigar-shaped or elliptical gray-green to tan lesions (1-6 inches long) across leaves.",
        "organic_treatment": [
            "Deep tilling to bury infected residue.",
            "Application of bio-fungicides with Trichoderma or Bacillus species."
        ],
        "chemical_treatment": [
            "Strobilurin and triazole fungicides (e.g., Headline AMP, Quilt Xcel) applied at VT/R1 stage."
        ],
        "prevention": [
            "Use Northern Leaf Blight-resistant seed hybrids.",
            "Crop rotation away from corn for at least 1–2 growing seasons."
        ]
    },
    10: {
        "class_name": "Corn_(maize)___healthy",
        "plant": "Corn (maize)",
        "condition": "Healthy",
        "category": "Healthy",
        "is_healthy": True,
        "pathogen": "None",
        "severity": "None",
        "visual_symptoms": "Long, vibrant green arching leaves without lesions, streaking, or pustules.",
        "organic_treatment": ["Maintain balanced nitrogen and phosphorus fertilization."],
        "chemical_treatment": ["No chemical treatment needed."],
        "prevention": [
            "Soil testing to ensure balanced micronutrients (zinc, sulfur).",
            "Adequate weed control to eliminate alternate hosts."
        ]
    },
    11: {
        "class_name": "Grape___Black_rot",
        "plant": "Grape",
        "condition": "Black rot",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Guignardia bidwellii",
        "severity": "High",
        "visual_symptoms": "Small reddish-brown circular spots on leaves; black fruiting specks (pycnidia) inside spots; shriveled black mummified berries.",
        "organic_treatment": [
            "Copper hydroxide or sulfur sprays applied from bud break to veraison.",
            "Prune and destroy infected cane spurs and old dried mummies."
        ],
        "chemical_treatment": [
            "Mancozeb, Captan, or DMI fungicides like Myclobutanil or Tebuconazole."
        ],
        "prevention": [
            "Trellis training for canopy openness and maximum sun exposure.",
            "Keep grass and weeds mowed short beneath vines."
        ]
    },
    12: {
        "class_name": "Grape___Esca_(Black_Measles)",
        "plant": "Grape",
        "condition": "Esca (Black Measles)",
        "category": "Fungal Complex",
        "is_healthy": False,
        "pathogen": "Phaeomoniella chlamydospora, Phaeoacremonium minimum, and Fomitiporia mediterranea",
        "severity": "High",
        "visual_symptoms": "'Tiger-stripe' interveinal chlorosis and necrosis; dark spotting on berries; internal trunk wood decay.",
        "organic_treatment": [
            "Protect pruning wounds with wound sealant or paste containing Trichoderma.",
            "Cut out decayed cordon arms several inches below visible wood staining."
        ],
        "chemical_treatment": [
            "No effective curative chemical once vascular trunk system is colonized; protect fresh cuts with Thiophanate-methyl."
        ],
        "prevention": [
            "Delay annual pruning until late winter when wound susceptibility is lower.",
            "Avoid making large pruning wounds on main trunks where possible."
        ]
    },
    13: {
        "class_name": "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
        "plant": "Grape",
        "condition": "Leaf blight (Isariopsis Leaf Spot)",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Pseudocercospora cladosporioides",
        "severity": "Moderate",
        "visual_symptoms": "Irregular dark brown lesions on older leaves, often defined by leaf veins, causing early defoliation.",
        "organic_treatment": [
            "Bordeaux mixture (copper sulfate + lime) spray during wet periods.",
            "Rake and compost fallen leaves away from vineyard."
        ],
        "chemical_treatment": [
            "Fungicides containing Mancozeb, Ziram, or Strobilurins."
        ],
        "prevention": [
            "Canopy management for air circulation.",
            "Ensure proper vine nutrition to prevent premature leaf senescence."
        ]
    },
    14: {
        "class_name": "Grape___healthy",
        "plant": "Grape",
        "condition": "Healthy",
        "category": "Healthy",
        "is_healthy": True,
        "pathogen": "None",
        "severity": "None",
        "visual_symptoms": "Broad, deep green leaves with crisp edges and healthy tendrils.",
        "organic_treatment": ["Maintain balanced organic vine nutrition and drip irrigation."],
        "chemical_treatment": ["No chemical treatment needed."],
        "prevention": [
            "Standard shoot thinning and leaf pulling around fruit clusters."
        ]
    },
    15: {
        "class_name": "Orange___Haunglongbing_(Citrus_greening)",
        "plant": "Orange",
        "condition": "Haunglongbing (Citrus greening)",
        "category": "Bacterial",
        "is_healthy": False,
        "pathogen": "Candidatus Liberibacter asiaticus (vectored by Asian citrus psyllid)",
        "severity": "Critical / Severe",
        "visual_symptoms": "Asymmetrical blotchy yellow mottle on leaves, yellow shoots, hard bitter lopsided fruit that remains green at the bottom.",
        "organic_treatment": [
            "Release parasitoid wasps (Tamarixia radiata) to suppress citrus psyllid vector.",
            "Foliar micronutrient sprays (zinc, manganese, iron) to prolong tree productivity."
        ],
        "chemical_treatment": [
            "Control psyllid vectors with Imidacloprid, Thiamethoxam, or Fenpropathrin.",
            "Trunk injection of oxytetracycline in certified commercial operations."
        ],
        "prevention": [
            "Plant only certified disease-free citrus nursery stock.",
            "Strict regional quarantine enforcement; do not transport citrus cuttings.",
            "Immediate removal and eradication of severely symptomatic infected trees."
        ]
    },
    16: {
        "class_name": "Peach___Bacterial_spot",
        "plant": "Peach",
        "condition": "Bacterial spot",
        "category": "Bacterial",
        "is_healthy": False,
        "pathogen": "Xanthomonas arboricola pv. pruni",
        "severity": "High",
        "visual_symptoms": "Angular purple-black water-soaked leaf spots that drop out creating a 'shot-hole' effect; fruit cracking and gumming.",
        "organic_treatment": [
            "Copper bactericides applied during dormant/delayed dormant stage.",
            "Oxytetracycline sprays during bloom under low-stress conditions."
        ],
        "chemical_treatment": [
            "Fixed copper sprays, Dodine, or Oxytetracycline (Mycoshield) during cover sprays."
        ],
        "prevention": [
            "Plant resistant peach varieties (e.g., Clayton, Candor, Biscoe).",
            "Avoid sandy sites prone to windblown sand damage which facilitates bacterial entry."
        ]
    },
    17: {
        "class_name": "Peach___healthy",
        "plant": "Peach",
        "condition": "Healthy",
        "category": "Healthy",
        "is_healthy": True,
        "pathogen": "None",
        "severity": "None",
        "visual_symptoms": "Long, lanceolate green leaves without spotting, curling, or shot holes.",
        "organic_treatment": ["Maintain weed-free tree base and adequate soil moisture."],
        "chemical_treatment": ["No chemical treatment needed."],
        "prevention": [
            "Open center (vase) pruning system for uniform sunlight."
        ]
    },
    18: {
        "class_name": "Pepper,_bell___Bacterial_spot",
        "plant": "Bell pepper",
        "condition": "Bacterial spot",
        "category": "Bacterial",
        "is_healthy": False,
        "pathogen": "Xanthomonas campestris pv. vesicatoria",
        "severity": "High",
        "visual_symptoms": "Small, water-soaked dark circular-to-angular spots on leaves with yellow halos, causing heavy leaf drop.",
        "organic_treatment": [
            "Copper octanoate (copper soap) sprays on a 7-day schedule.",
            "Bacillus subtilis or Bacillus amyloliquefaciens bio-bactericide foliar applications."
        ],
        "chemical_treatment": [
            "Copper hydroxide mixed with Mancozeb (helps overcome copper-resistant bacterial strains)."
        ],
        "prevention": [
            "Purchase hot-water treated or certified disease-free pepper seeds.",
            "Avoid overhead sprinkler irrigation; always use drip tape.",
            "Do not work in pepper fields when foliage is wet."
        ]
    },
    19: {
        "class_name": "Pepper,_bell___healthy",
        "plant": "Bell pepper",
        "condition": "Healthy",
        "category": "Healthy",
        "is_healthy": True,
        "pathogen": "None",
        "severity": "None",
        "visual_symptoms": "Lush green glossy foliage with sturdy upright stems and clean leaves.",
        "organic_treatment": ["Side-dress with balanced organic compost or calcium-magnesium feed."],
        "chemical_treatment": ["No chemical treatment needed."],
        "prevention": [
            "Maintain consistent soil moisture to prevent blossom end rot.",
            "Stake plants to keep lower foliage off the soil."
        ]
    },
    20: {
        "class_name": "Potato___Early_blight",
        "plant": "Potato",
        "condition": "Early blight",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Alternaria solani",
        "severity": "Moderate to High",
        "visual_symptoms": "Dark brown to black spots with distinct concentric rings ('target-board' pattern) surrounded by chlorotic yellow halos.",
        "organic_treatment": [
            "Copper hydroxide or copper oxychloride foliar sprays.",
            "Biofungicides containing Bacillus amyloliquefaciens.",
            "Remove lower infected leaves as soon as first spots appear."
        ],
        "chemical_treatment": [
            "Chlorothalonil, Mancozeb, Azoxystrobin, or Boscalid."
        ],
        "prevention": [
            "Rotate crops away from Solanaceae (tomatoes, peppers, eggplants) for 3 years.",
            "Ensure adequate nitrogen and potassium; stressed older plants are more susceptible.",
            "Water at ground level in the morning."
        ]
    },
    21: {
        "class_name": "Potato___Late_blight",
        "plant": "Potato",
        "condition": "Late blight",
        "category": "Oomycete / Water Mold",
        "is_healthy": False,
        "pathogen": "Phytophthora infestans",
        "severity": "Critical",
        "visual_symptoms": "Water-soaked, rapidly expanding dark green-to-black lesions; white fuzzy mold on leaf undersides in humid weather; quick collapse of entire plant.",
        "organic_treatment": [
            "Fixed copper sprays applied protectively before rain/fog events.",
            "Immediate destruction of infected vines to prevent tuber infection."
        ],
        "chemical_treatment": [
            "Systemic fungicides: Mandipropamid, Dimethomorph, Fluopicolide, or Cymoxanil."
        ],
        "prevention": [
            "Plant only certified disease-free seed tubers.",
            "Eliminate cull piles and volunteer potato plants nearby.",
            "Hill soil well over tubers to prevent spore wash-down."
        ]
    },
    22: {
        "class_name": "Potato___healthy",
        "plant": "Potato",
        "condition": "Healthy",
        "category": "Healthy",
        "is_healthy": True,
        "pathogen": "None",
        "severity": "None",
        "visual_symptoms": "Uniform compound green leaves with crisp margins and healthy vigor.",
        "organic_treatment": ["Maintain loose, well-draining organic soil and hill plants regularly."],
        "chemical_treatment": ["No chemical treatment needed."],
        "prevention": [
            "Keep soil evenly moist, never waterlogged.",
            "Scout weekly for Colorado potato beetles."
        ]
    },
    23: {
        "class_name": "Raspberry___healthy",
        "plant": "Raspberry",
        "condition": "Healthy",
        "category": "Healthy",
        "is_healthy": True,
        "pathogen": "None",
        "severity": "None",
        "visual_symptoms": "Bright green pinnate leaves with fine serrations and clean, cane growth.",
        "organic_treatment": ["Apply organic compost mulch along row bases."],
        "chemical_treatment": ["No chemical treatment needed."],
        "prevention": [
            "Prune floricanes immediately after fruiting.",
            "Trellis canes to facilitate airflow and rapid drying."
        ]
    },
    24: {
        "class_name": "Soybean___healthy",
        "plant": "Soybean",
        "condition": "Healthy",
        "category": "Healthy",
        "is_healthy": True,
        "pathogen": "None",
        "severity": "None",
        "visual_symptoms": "Trifoliate leaves with vibrant green coloration and uniform texture.",
        "organic_treatment": ["Maintain symbiotic rhizobium inoculation in soil."],
        "chemical_treatment": ["No chemical treatment needed."],
        "prevention": [
            "Rotate crops annually with non-legume crops.",
            "Ensure proper soil drainage."
        ]
    },
    25: {
        "class_name": "Squash___Powdery_mildew",
        "plant": "Squash",
        "condition": "Powdery mildew",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Podosphaera xanthii / Erysiphe cichoracearum",
        "severity": "Moderate",
        "visual_symptoms": "White talcum-powder-like spots on upper and lower leaf surfaces, causing leaves to yellow, dry out, and curl.",
        "organic_treatment": [
            "Potassium bicarbonate (MilStop or homemade: 1 tbsp baking soda + 1 tsp horticultural oil per gallon).",
            "Neem oil or sulfur sprays at first sign of white spots.",
            "Dilute milk spray (10-20% milk in water) under direct sunlight."
        ],
        "chemical_treatment": [
            "Fungicides containing Myclobutanil, Quinoxyfen, or Triflumizole."
        ],
        "prevention": [
            "Plant resistant cucurbit varieties (labeled PMR).",
            "Space plants generously to promote rapid air drying.",
            "Plant in full sun (at least 6–8 hours daily)."
        ]
    },
    26: {
        "class_name": "Strawberry___Leaf_scorch",
        "plant": "Strawberry",
        "condition": "Leaf scorch",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Diplocarpon earlianum",
        "severity": "Moderate",
        "visual_symptoms": "Small purple-to-reddish spots that enlarge and coalesce into dark blotches; leaf margins look burned or scorched.",
        "organic_treatment": [
            "Remove and discard severely affected leaves.",
            "Apply copper fungicides in early spring before blossoms open."
        ],
        "chemical_treatment": [
            "Captan, Thiophanate-methyl, or Pyraclostrobin."
        ],
        "prevention": [
            "Renovate strawberry beds after harvest by mowing and removing old foliage.",
            "Use straw mulch to keep leaves off bare soil.",
            "Use drip irrigation rather than overhead sprinklers."
        ]
    },
    27: {
        "class_name": "Strawberry___healthy",
        "plant": "Strawberry",
        "condition": "Healthy",
        "category": "Healthy",
        "is_healthy": True,
        "pathogen": "None",
        "severity": "None",
        "visual_symptoms": "Vibrant emerald green trifoliate leaves with clean serrated edges.",
        "organic_treatment": ["Maintain straw mulch and balanced pine bark amendment."],
        "chemical_treatment": ["No chemical treatment needed."],
        "prevention": [
            "Ensure beds are well weeded and crowns are not buried too deeply."
        ]
    },
    28: {
        "class_name": "Tomato___Bacterial_spot",
        "plant": "Tomato",
        "condition": "Bacterial spot",
        "category": "Bacterial",
        "is_healthy": False,
        "pathogen": "Xanthomonas species",
        "severity": "High",
        "visual_symptoms": "Small dark brown water-soaked lesions on leaves with greasy appearance and yellow margins; severe defoliation.",
        "organic_treatment": [
            "Copper soap (copper octanoate) sprays every 7–10 days.",
            "Bio-control with bacteriophage products (AgriPhage).",
            "Bacillus subtilis foliar application."
        ],
        "chemical_treatment": [
            "Tank mix of fixed copper fungicide plus Mancozeb."
        ],
        "prevention": [
            "Use certified disease-free seed and transplants.",
            "Never overhead water tomato foliage.",
            "Avoid handling plants when wet from dew or rain."
        ]
    },
    29: {
        "class_name": "Tomato___Early_blight",
        "plant": "Tomato",
        "condition": "Early blight",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Alternaria solani",
        "severity": "Moderate to High",
        "visual_symptoms": "Brown to black spots with distinct concentric target rings, starting on lower leaves and yellowing surrounding tissue.",
        "organic_treatment": [
            "Prune off the lowest 12–18 inches of foliage once plant is established.",
            "Apply liquid copper or Serenade (Bacillus subtilis).",
            "Thick straw or plastic mulch to stop soil spores splashing onto leaves."
        ],
        "chemical_treatment": [
            "Chlorothalonil (Daconil), Mancozeb, or Azoxystrobin."
        ],
        "prevention": [
            "Stake or cage tomatoes to keep foliage off the ground.",
            "Crop rotation away from nightshades for 3 years.",
            "Disinfect stakes and cages with bleach solution between seasons."
        ]
    },
    30: {
        "class_name": "Tomato___Late_blight",
        "plant": "Tomato",
        "condition": "Late blight",
        "category": "Oomycete / Water Mold",
        "is_healthy": False,
        "pathogen": "Phytophthora infestans",
        "severity": "Critical",
        "visual_symptoms": "Large, irregular water-soaked pale-to-dark gray lesions; white fungal felt underneath during high humidity; rapid vine collapse.",
        "organic_treatment": [
            "Preventive copper sprays before wet, cool disease-favorable weather.",
            "Immediately bag and dispose of infected plants in trash (do not compost!)."
        ],
        "chemical_treatment": [
            "Chlorothalonil for prevention; Cymoxanil, Mandipropamid, or Propamocarb for active disease."
        ],
        "prevention": [
            "Plant resistant tomato cultivars (e.g., Defiant, Mountain Magic, Iron Lady).",
            "Maximize spacing between plants for airflow.",
            "Keep greenhouse humidity below 85%."
        ]
    },
    31: {
        "class_name": "Tomato___Leaf_Mold",
        "plant": "Tomato",
        "condition": "Leaf Mold",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Passalora fulva (Cladosporium fulvum)",
        "severity": "Moderate",
        "visual_symptoms": "Pale green or yellowish spots on upper leaf surfaces; velvety olive-green to brown fungal growth directly beneath.",
        "organic_treatment": [
            "Bio-fungicides like Bacillus subtilis.",
            "Copper fungicides sprayed thoroughly on the undersides of leaves."
        ],
        "chemical_treatment": [
            "Chlorothalonil, Mancozeb, or Difenoconazole."
        ],
        "prevention": [
            "Ventilate high tunnels and greenhouses thoroughly; reduce relative humidity below 85%.",
            "Ensure wide plant spacing and drip irrigation."
        ]
    },
    32: {
        "class_name": "Tomato___Septoria_leaf_spot",
        "plant": "Tomato",
        "condition": "Septoria leaf spot",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Septoria lycopersici",
        "severity": "High",
        "visual_symptoms": "Numerous circular, 1–3 mm spots with dark brown margins and gray or tan centers containing tiny black specks (pycnidia).",
        "organic_treatment": [
            "Remove lower infected leaves as soon as spots appear.",
            "Copper octanoate or sulfur-based sprays.",
            "Mulch heavily around base of plants."
        ],
        "chemical_treatment": [
            "Chlorothalonil, Mancozeb, or Quadris (Azoxystrobin)."
        ],
        "prevention": [
            "Clean up all plant debris at the end of the season.",
            "Avoid overhead watering; water at base in the morning."
        ]
    },
    33: {
        "class_name": "Tomato___Spider_mites Two-spotted_spider_mite",
        "plant": "Tomato",
        "condition": "Spider mites (Two-spotted spider mite)",
        "category": "Pest / Arachnid",
        "is_healthy": False,
        "pathogen": "Tetranychus urticae",
        "severity": "Moderate to High",
        "visual_symptoms": "Fine yellow stippling or bronzing on leaves; delicate webbing visible between stems and leaf undersides; leaves dry and drop.",
        "organic_treatment": [
            "Spray with insecticidal soap or horticultural oil (ensure complete leaf underside coverage).",
            "Release predatory mites (Phytoseiulus persimilis or Neoseiulus californicus).",
            "Strong blast of water to dislodge mites and disrupt webs."
        ],
        "chemical_treatment": [
            "Acaricides/Miticides: Bifenazate (Floramite), Abamectin, or Spiromesifen."
        ],
        "prevention": [
            "Avoid dusty, drought-stressed conditions which favor mite reproduction.",
            "Avoid excessive use of broad-spectrum synthetic pyrethroids that kill natural mite predators."
        ]
    },
    34: {
        "class_name": "Tomato___Target_Spot",
        "plant": "Tomato",
        "condition": "Target Spot",
        "category": "Fungal",
        "is_healthy": False,
        "pathogen": "Corynespora cassiicola",
        "severity": "High",
        "visual_symptoms": "Brown circular lesions with light brown centers and dark concentric rings resembling a target board; can affect foliage and fruit.",
        "organic_treatment": [
            "Copper hydroxide sprays.",
            "Pruning lower foliage and ensuring strict sanitation."
        ],
        "chemical_treatment": [
            "Chlorothalonil, Azoxystrobin, Boscalid, or Fluxapyroxad."
        ],
        "prevention": [
            "Maintain wide plant spacing.",
            "Rotate crops with non-susceptible species (avoid planting after soybeans or cucurbits)."
        ]
    },
    35: {
        "class_name": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "plant": "Tomato",
        "condition": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "category": "Viral",
        "is_healthy": False,
        "pathogen": "Begomovirus (vectored by Silverleaf whitefly Bemisia tabaci)",
        "severity": "Severe",
        "visual_symptoms": "Pronounced upward curling and cupping of leaves; yellowing leaf margins; severe plant stunting and flower abortion.",
        "organic_treatment": [
            "Immediate removal and bagging of infected plants to protect healthy crop.",
            "Yellow sticky traps to monitor and trap whitefly vectors.",
            "Spray insecticidal soaps or neem oil to reduce whitefly populations."
        ],
        "chemical_treatment": [
            "No chemical cure exists for the virus itself. Control whitefly vector with Dinotefuran, Acetamiprid, or Spirotetramat."
        ],
        "prevention": [
            "Plant TYLCV-resistant tomato varieties.",
            "Use fine insect netting (50-mesh) in greenhouses to exclude whiteflies.",
            "Use reflective silver mulches which repel whiteflies."
        ]
    },
    36: {
        "class_name": "Tomato___Tomato_mosaic_virus",
        "plant": "Tomato",
        "condition": "Tomato mosaic virus (ToMV)",
        "category": "Viral",
        "is_healthy": False,
        "pathogen": "Tobamovirus (mechanically transmitted)",
        "severity": "Severe",
        "visual_symptoms": "Mottled light and dark green patterns on leaves ('mosaic'); leaf distortion, blistering, strapping (shoestring leaf shape); stunted growth.",
        "organic_treatment": [
            "Carefully rogue and destroy infected plants immediately.",
            "Wash hands and tools with nonfat dry milk (20%) or trisodium phosphate (TSP) which denatures the virus."
        ],
        "chemical_treatment": [
            "No curative chemicals exist for viral infections."
        ],
        "prevention": [
            "Plant virus-resistant tomato hybrids (look for 'ToMV' or 'TMV' on seed packets).",
            "Strict sanitation: tobacco users must wash hands thoroughly before touching tomato plants.",
            "Disinfect trellises, stakes, and pruning tools."
        ]
    },
    37: {
        "class_name": "Tomato___healthy",
        "plant": "Tomato",
        "condition": "Healthy",
        "category": "Healthy",
        "is_healthy": True,
        "pathogen": "None",
        "severity": "None",
        "visual_symptoms": "Deep green, fragrant foliage with robust growth, sturdy stems, and no visible spotting or curling.",
        "organic_treatment": ["Maintain regular organic feeding (fish emulsion, compost tea)."],
        "chemical_treatment": ["No chemical treatment needed."],
        "prevention": [
            "Consistent drip watering to avoid blossom end rot.",
            "Mulch bed with clean straw or organic shredded leaves.",
            "Prune suckers and stake cleanly."
        ]
    }
}

