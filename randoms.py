import random

def Industry():
    list1 = ["Automobile","Oil and Gas"]
    return random.choice(list1)


def Category():
    list1 = ["Safety Material","Adhesive","Industrial Valves","Drilling machine, Bolt cutter","Fasteners","Battery","Electrical","Drill Bit and Fasteners"]
    return random.choice(list1)


def Risk_Score():
    list1 = [76,63,89,84,91,20]
    return random.choice(list1)


def Risk_Level():
    list1 = ["Low","Medium","High"]
    return random.choice(list1)


def Compliance():
    list1 = ["Compliant","Non-Compliant"]
    return random.choice(list1)

def Status():
    list1 = [True,False]
    return random.choice(list1)

def demo_number():
    list1 = [5,7,8,3,6]
    return random.choice(list1)


def rt():
    er=[
        {
        "key": "nakakita",
        "supplier": "*******************8",
        "industry": "Automobile",
        "service": [
            "NAKAKITA's serial number",
            "Plant name (Shipyard name)",
            "Plant number (Ship number)",
            "Application (Valve number)",
            "Product name, etc"
        ],
        "product": [
            {
                "productAdress": "Nozzle, Nakakita Seisakusho Co Ltd,Japan, Stainless Steel 304 Stellited, Psvs Of Uty-2 Plant",
                "key": 1,
                "name": "Nozzle",
                "location": "Yanbu, Saudi Arabia",
                "sku": "GSC034-0321-02-55664",
                "Mfg": "Nakakita Seisakusho Co Ltd, Japan",
                "unspsc": "40141731",
                "hsn": "84249000",
                "material": "Stainless Steel 304 Stellited",
                "application": "Psvs Of Uty-2 Plant"
            },
            {
                "productAdress": "Gasket, Nakakita Seisakusho Co Ltd, Japan, 27,Acbt-3294Dm",
                "key": 2,
                "name": "Gasket",
                "location": "Al-Jubail, Saudi Arabia",
                "sku": "GSC034-1120-01-18029",
                "Mfg": "Nakakita Seisakusho Co Ltd, Japan",
                "unspsc": "31401500",
                "hsn": "40169320",
                "material": "ACBT-3294DM",
                "application": "27"
            },
            {
                "productAdress": "Spindle, Nakakita Seisakusho Co Ltd, Japan, 8,Arrowhead International Corporation, Mitsubishi Heavy Industries,ltd, NS255DX-E, Stainless Steel 403",
                "name": "Spindle",
                "key": 3,
                "location": "Yanbu, Saudi Arabia",
                "sku": "GSC034-1120-01-40684",
                "Mfg": "Al-Jubail, Saudi Arabia",
                "unspsc": "31162800",
                "hsn": "84604011",
                "material": "Stainless Steel 403",
                "application": "NS255DX-E"
            },
            {
                "productAdress": "Bellows, Nakakita Seisakusho Co Ltd,Japan, SS316L",
                "name": "Bellows",
                "key": 4,
                "location": "Yanbu, Saudi Arabia",
                "sku": "GSC034-0321-02-52092",
                "Mfg": "Nakakita Seisakusho Co Ltd, Japan",
                "unspsc": "23153100",
                "hsn": "84248920",
                "material": "SS 316L",
                "application": "--"
            },
            {
                "productAdress": "RELAY, NAKAKITA SEISAKUSHO CO LTD, KC003948, PNEUMATIC,DOUBLE PILOT, NS727D-D, JAPAN",
                "name": "RELAY",
                "location": "Al-Jubail, Saudi Arabia",
                "sku": "GSC034-0321-02-55664",
                "Mfg": "Nakakita Seisakusho Co Ltd, Japan",
                "unspsc": "39122325",
                "key": 5,
                "hsn": "85364900",
                "material": "PNEUMATIC,DOUBLE PILOT",
                "application": "NS727D-D"
            },
            {
                "productAdress": "O-Ring, Nakakita Seisakusho Co Ltd, G65, Pelletizing,Ns-650 Elox-Rb, 83K-X107Z, Nitrile Rubber, Jis B 2401,3.1 Mm, 64.4 Mm",
                "name": "O-Ring",
                "location": " Al-Jubail, Saudi Arabia",
                "sku": "GSC034-1120-01-27120",
                "Mfg": "Nakakita Seisakusho Co Ltd",
                "unspsc": "31401503",
                "key": 6,
                "hsn": "40169320",
                "material": "Nitrile Rubber",
                "application": "NS-650 ELOX-RB"
            },
            {
                "productAdress": "Valve Disc, Nakakita Seisakusho Co Ltd, Japan, NS 75F, FCD 400, 150 LB",
                "name": "Valve Disc",
                "location": " Al-Jubail, Saudi Arabia",
                "sku": "GSC034-1120-01-11142",
                "Mfg": "Nakakita Seisakusho Co Ltd, Japan",
                "unspsc": "40141616",
                "key": 7,
                "hsn": "84819090",
                "material": "FCD 400",
                "application": "Secondary Pressure Regulator"
            },
            {
                "productAdress": "Nakakita Seisakusho Co Ltd, Japan, NS727D-D",
                "name": "Motor",
                "location": " Al-Jubail, Saudi Arabia",
                "sku": "GSC034-1120-01-25822",
                "Mfg": "Nakakita Seisakusho Co Ltd, Japan",
                "unspsc": "26100000",
                "key": 8,
                "hsn": "85369090",
                "material": "Non Asbestos",
                "application": "237 OHM"
            },
            {
                "productAdress": "Compression Spring, Nakakita Seisakusho Co Ltd, Japan, 11",
                "name": "Compression Spring",
                "location": " Al-Jubail, Saudi Arabia",
                "sku": "GSC034-1120-01-40994",
                "Mfg": "Nakakita Seisakusho Co Ltd,Japan",
                "unspsc": "31161900",
                "key": 9,
                "hsn": "73209090",
                "material": "SKD4",
                "application": "NS-650 ELOX-RB"
            },
            {
                "productAdress": "Disc, Nakakita Seisakusho Co Ltd,Japan, Ns-255Ab-E (4'X6'Ansi 300/150)",
                "name": "Disc",
                "location": "Al-Jubail, Saudi Arabia",
                "sku": "GSC034-0321-02-53317",
                "Mfg": "Nakakita Seisakusho Co Ltd,Japan",
                "unspsc": "23153100",
                "key": 10,
                "hsn": "84819090",
                "material": "Stainless Steel 304 Stellited",
                "application": "Ns-255Ab-E (4'X6'Ansi 300/150) Psvs Of Uty-2 Plant"
            }
        ],
        "website": "https://www.nakakita-s.co.jp/en/companyoutline",
        "websiteName": "www.nakakita-s.co",
        "companyId": "15468456",
        "location": "1-1 Fukonominamicho, Daito, Osaka 574-8691, Japan",
        "certification": [
            {
                "name": "Quality Management",
                "certificate": "ISO 9001 (LRQA)",
                "expire_date": "Expires 15 Jan 2025"
            },
            {
                "name": "Environment Management",
                "certificate": "CE Marking (LRQA)",
                "expire_date": "Expires 15 Jan 2025"
            },
            {
                "name": "Eco",
                "certificate": "Eco Action 21 Initiative",
                "expire_date": "Expires 23 Nov 2024"
            },
            {
                "name": "ASME",
                "certificate": "ASME Type Approval",
                "expire_date": "Expires 02 Dec 2024"
            },
            {
                "name": "Safety",
                "certificate": "Safety valve KCs mark certification",
                "expire_date": "Expires 23 Nov 2024"
            }
        ],
        "riskScore": 95,
        "riskLevel": "Low",
        "compliance": "Compliant",
        "category": "Safety Material",
        "cyberRiskScore": 90,
        "financialRiskScore": 40,
        "healthScore": 60,
        "environment": 79,
        "social": 80,
        "governance": 60,
        "healthSafety": 90,
        "status": True,
        "email": "bus@nakakita-s.co.jp",
        "contactUs": "81-72-871-1331",
        "aboutUs": "our founding in 1930, we have been working hard every day to meet our customers' needs, from design and manufacturing to maintenance of fluid control systems centered on valves, under our company motto of 'progressive development.' Meanwhile,in order to respond to the accelerating changes of the times, we are adding 'challenge' to our theme of 'protecting the present while challenging new things'. While refining our 'product development' that gives shape to the voices of our customers, we will also challenge ourselves to develop new 'technologies' and aim to be a company that proposes new values and benefits to our customers. We ask for your continued understanding and support for Nakakita Seisakusho Co., Ltd., which boldly challenges new things.",
        "history": [
            {
                "achivement": "Commenced the production of automatic control valves at Matsugae-cho, Kita-ku, Osaka under a private undertaking owned by Mr. Benzo Nakakita, the first president of Nakakita Seisakusho Co., Ltd",
                "years": "1930"
            },
            {
                "achivement": "Reopened Tokyo office and opened Kyushu office.",
                "years": "1950"
            },
            {
                "achivement": "At the 40th anniversary of the founding, the new plant was thrown open to customers.",
                "years": "1970"
            },
            {
                "achivement": "Introduced a three-dimensional measuring instrument.",
                "years": "1999"
            },
            {
                "achivement": "Mr. Kenichi Nakakita was inaugurated as president",
                "years": "2004"
            },
            {
                "achivement": "Completed Nuclear Valve Assembly Shop.",
                "years": "2009"
            },
            {
                "achivement": "Obtained Certificate 01 eco action 21 Approved by IPSuS",
                "years": "2011"
            },
            {
                "achivement": "KCs Mark for safety valves approved by KOSHA (Korea).",
                "years": "2013"
            }
        ],
        "insurance": [
            {
                "name": "Public Liability",
                "amount": "$ 1,00,000.000",
                "expire_date": "Expires 30 Nov 2024"
            },
            {
                "name": "Professional Indemnity",
                "amount": "$ 5,000.000",
                "expire_date": "Expires 22 Dec 2024"
            },
            {
                "name": "Employer’s Liability",
                "amount": "$ 1,50,000.000",
                "expire_date": "Expires 04 Jan 2025"
            }
        ]
    },
    
    {
        "key": "green",
        "supplier": "!!!!!!!!!!!!!!!",
        "industry": "Automobile",
        "service": [
            "Samson material handeling",
            "Samson solar power Samson",
            "agro equipment",
            "Samson agro biotech"
        ],
        "product": "",
        "website": "https://samsonmaterialhandling.com/",
        "websiteName": "samsonmaterialhandling.com",
        "companyId": "15468456",
        "location": "Plot No. N-49/1, MIDC, Additional Ambernath Indl. Area, Ambernath (E), Thane - 421506, Maharashtra, India.",
        "certification": [
            {
                "name": "Quality Management",
                "certificate": "ISO 14001:2004",
                "expire_date": "Expires 23 Nov 2024"
            },
            {
                "name": "Environment Management",
                "certificate": "ISO 9001 (LRQA)",
                "expire_date": "Expires 02 Dec 2024"
            },
            {
                "name": "Health & Safety Management",
                "certificate": "OHSAS 18001:2007",
                "expire_date": "Expires 15 Jan 2025"
            },
            {
                "name": "Quantity Management System",
                "certificate": "ISO9001:2008",
                "expire_date": "Expires 15 Jan 2025"
            }
        ],
        "riskScore": 84,
        "riskLevel": "Low",
        "compliance": "Compliant",
        "category": "Safety Material",
        "cyberRiskScore": 90,
        "financialRiskScore": 40,
        "healthScore": 60,
        "environment": 79,
        "social": 80,
        "governance": 60,
        "healthSafety": 90,
        "status": True,
        "email": "info@hararamagroup.com",
        "contactUs": "+91 251 3217880 / +91 251 2621681",
        "aboutUs": "Green Field Material Handling P. Ltd., An ISO 9001-2000 Certified Company, a group of companies founded in 1990, offering a wide range of products and services to industry in the specialized field of materials handling and lifting. The vital strength of the organization is the vast experience of our key person, for more than two decades, in the field of Material Handling and Critical Lifting, which has solved a lot of lifting problems in India and Overseas as well. Our accomplished engineering sales force could solve any sort of lifting problems. Advise and implement up-to-date, latest innovative designs and solutions to meet newer challenges. We sincerely attend to your requirement, small or large, from a single hook to a 50-meter long non-metallic sling. Our speciality is heavy-duty non-metallic sling, made of polyester. These are of two types: flat webbing sling with Eye-loop at the ends and Round (endless) slings. Both are available in different lengths and weight lifting capacities, ranging from 1 ton up to 300 tons. We also have various types of Hooks, D-Shackles, Bow Shackles, Multi-leg slings, Master Rings & Cargo lashings, Safety Harness, lifting beams, lifting clamps & crane weighing systems, etc. The Green Field's efficient personnel are always available to advise you on any type of problem in material handling and lifting.",
        "history": [
            {
                "achivement": "Commenced the production of automatic control valves at Matsugae-cho, Kita-ku, Osaka under a private undertaking owned by Mr. Benzo Nakakita, the first president of Nakakita Seisakusho Co., Ltd",
                "years": "1930"
            },
            {
                "achivement": "Reopened Tokyo office and opened Kyushu office.",
                "years": "1950"
            },
            {
                "achivement": "At the 40th anniversary of the founding, the new plant was thrown open to customers.",
                "years": "1970"
            },
            {
                "achivement": "Introduced a three-dimensional measuring instrument.",
                "years": "1999"
            },
            {
                "achivement": "Mr. Kenichi Nakakita was inaugurated as president",
                "years": "2004"
            },
            {
                "achivement": "Completed Nuclear Valve Assembly Shop.",
                "years": "2009"
            },
            {
                "achivement": "Obtained Certificate 01 eco action 21 Approved by IPSuS",
                "years": "2011"
            },
            {
                "achivement": "KCs Mark for safety valves approved by KOSHA (Korea).",
                "years": "2013"
            }
        ],
        "insurance": [
            {
                "name": "Public Liability",
                "amount": "$ 1,00,000.000",
                "expire_date": "Expires 30 Nov 2024"
            },
            {
                "name": "Professional Indemnity",
                "amount": "$ 5,000.000",
                "expire_date": "Expires 22 Dec 2024"
            },
            {
                "name": "Employer’s Liability",
                "amount": "$ 1,50,000.000",
                "expire_date": "Expires 04 Jan 2025"
            }
        ]
    },
    {
        "key": "fasteners",
        "supplier": "$$$$$$$$$$$$$$$$$$$",
        "industry": "Automobile",
        "service": "",
        "product": [
            "HEX HEAD FLANGE SCREW/BOLT",
            "Cross pan/flat screw",
            "Hex nut",
            "U blot"
        ],
        "location": "No.79, Valmiki Street Thiruvanmiyur, Chennai - 600 041Tamil Nadu, India",
        "certification": [
            {
                "name": "Environment Management",
                "certificate": "ISO 9001:2015",
                "expire_date": "Expires 23 Nov 2024"
            },
            {
                "name": "EU Certificate of quality system",
                "certificate": "0343/PED/MUM/2210015/2",
                "expire_date": "Expires 02 Dec 2024"
            },
            {
                "name": "Quantity Management System",
                "certificate": "0038/UK/PER/MUM/2210015/4",
                "expire_date": "Expires 15 Jan 2025"
            }
        ],
        "riskScore": 73,
        "riskLevel": "Low",
        "compliance": "Compliant",
        "category": "Safety Material",
        "cyberRiskScore": 41,
        "financialRiskScore": 80,
        "healthScore": 60,
        "environment": 70,
        "social": 79,
        "governance": 55,
        "healthSafety": 80,
        "status": True,
        "companyId": "15440456",
        "website": "https://www.vkfasteners.co.in/",
        "websiteName": "www.vkfasteners.co.in",
        "email": "marketing1@vkf.co.in",
        "contactUs": "+91 89259 50777",
        "aboutUs": "VK Fasteners - Another MILESTONE of IGP Group, serving the industries more than 60 years. As a traditional family business the core values of optimization, reliability, continuity, and sustainability hold True for every business in IGP Family.Now VK Fasteners Private Limited, a group company of IGP is set at Chennai, Tamilnadu for manufacture of HIGH TENSILE FASTENERS AND PARTS to cater the need of automotive manufacturer through Cold Forging Process.Highly trained and experienced professional along with latest automatic imported bolt former with quality control equipment shall assure you ONTIME DELIVERY AND BEST QUALITY Plant has a installed capacity around 5000MTPA Plant is capable enough to produce all types of fasteners to national and international standards and to customer designed specification",
        "history": [
            {
                "achivement": "established in 1965,",
                "years": "1965"
            },
            {
                "achivement": "Another MILESTONE of IGP Group, serving the industries more than 60 years.As a traditional family business the core values of optimization, reliability, continuity, and sustainability hold True for every business in IGP Family.",
                "years": "2025"
            }
        ],
        "insurance": [
            {
                "name": "Public Liability",
                "amount": "$ 1,00,000.000",
                "expire_date": "Expires 30 Nov 2024"
            },
            {
                "name": "Professional Indemnity",
                "amount": "$ 5,000.000",
                "expire_date": "Expires 22 Dec 2024"
            },
            {
                "name": "Employer’s Liability",
                "amount": "$ 1,50,000.000",
                "expire_date": "Expires 04 Jan 2025"
            }
        ]
    },
    {
        "key": "rahul",
        "supplier": "@@@@@@@@@@@@@@@@@@@@@",
        "industry": "Automobile",
        "service": "",
        "product": [
            "Epoxy adhesive",
            "Steam solenoid servo valve",
            "Flow control valve",
            "Pneumatic cylinder",
            "Pneumatic actuators",
            "Solenoid coil",
            "Auto drain valve",
            "Pneumatic tubes",
            "Air cylinders"
        ],
        "location": "Plot No. N-49/1, MIDC, Additional Ambernath Indl. Area, Ambernath (E), Thane - 421506, Maharashtra, India.",
        "certification": [
            {
                "name": "Power tool accessories & fasteners and hand tools",
                "certificate": "ISO 9001:2015",
                "expire_date": "Expires 23 Nov 2024"
            }
        ],
        "riskScore": 48,
        "riskLevel": "Medium",
        "compliance": "Compliant",
        "category": "Adhesive",
        "cyberRiskScore": 35,
        "financialRiskScore": 52,
        "healthScore": 60,
        "environment": 40,
        "social": 17,
        "governance": 69,
        "healthSafety": 34,
        "companyId": "15110451",
        "website": "https://rahulagencies.in/",
        "websiteName": "rahulagencies.in",
        "status": True,
        "email": "mayur.rahulagencies@gmail.com",
        "contactUs": "+91 9824138242",
        "aboutUs": "Established as a Proprietor firm in the year 2019 at Vapi (Gujarat, India), we “Rahul Agencies” are a leading Distributor / Channel Partner of a wide ran of Solenoid Valves, Pneumatic Cylinder, etc. We procure these products from the most trusted and renowned vendors after stringent market analysis. Further, we offer these products at reasonable rates and deliver these within the promised time-frame. Under the headship of “Mr. Mayur Shah”, we have gained a huge clientele across the nation.",
        "history": [
            {
                "achivement": "established in 1990,",
                "years": "1990"
            },
            {
                "achivement": "At the 30th anniversary of the founding, the new plant was thrown open to customers.",
                "years": "2025"
            }
        ],
        "insurance": [
            {
                "name": "Public Liability",
                "amount": "$ 1,00,000.000",
                "expire_date": "Expires 30 Nov 2024"
            },
            {
                "name": "Professional Indemnity",
                "amount": "$ 5,000.000",
                "expire_date": "Expires 22 Dec 2024"
            },
            {
                "name": "Employer’s Liability",
                "amount": "$ 1,50,000.000",
                "expire_date": "Expires 04 Jan 2025"
            }
        ]
    },
    {
        "key": "sonic",
        "supplier": "#############",
        "industry": "Oil and Gas",
        "service": "",
        "product": [
            "Pumps",
            "fans",
            "Room heater",
            "Exhaust motors",
            "Electric iron",
            "Immersion rod"
        ],
        "location": "Meerut Road Industrial Area, Ghaziabad - 201003, Uttar Pradesh, India",
        "certification": [
            {
                "name": "Environment Management",
                "certificate": "ISO 9001:2015",
                "expire_date": "Expires 3 Nov 2024"
            }
        ],
        "riskScore": 42,
        "riskLevel": "Medium",
        "compliance": "Non-Compliant",
        "category": "Safety Material",
        "cyberRiskScore": 50,
        "financialRiskScore": 40,
        "healthScore": 60,
        "environment": 37,
        "social": 31,
        "governance": 49,
        "healthSafety": 19,
        "status": False,
        "email": "sonic.surat@gmail.com",
        "companyId": "10110411",
        "website": "https://www.sonichomeappliances.com/",
        "websiteName": "www.sonichomeappliances.com",
        "contactUs": "+91 9998012325",
        "aboutUs": "We “Sonic Enterprise” founded in the year 2005 are a renowned firm that is engaged in manufacturing a wide assortment of Kitchen Jali, PVC Curtain Bracket Holder, PVC Curtain Bracket, Wall Hanger, etc. We have a wide and well functional infrastructural unit that is situated at Rajkot (Gujarat, India) and helps us in making a remarkable collection of products as per the set industry standards. We are a Sole Proprietorship firm that is managed under the headship of “Mr. Mukesh” (Manager), and have achieved a significant position in this sector.",
        "history": [
            {
                "achivement": "Commenced the production of automatic control valves at Matsugae-cho, Kita-ku, Osaka under a private undertaking owned by Mr. Benzo Nakakita, the first president of Nakakita Seisakusho Co., Ltd",
                "years": "1930"
            },
            {
                "achivement": "Reopened Tokyo office and opened Kyushu office.",
                "years": "1950"
            },
            {
                "achivement": "At the 40th anniversary of the founding, the new plant was thrown open to customers.",
                "years": "1970"
            },
            {
                "achivement": "Introduced a three-dimensional measuring instrument.",
                "years": "1999"
            },
            {
                "achivement": "Mr. Kenichi Nakakita was inaugurated as president",
                "years": "2004"
            },
            {
                "achivement": "Completed Nuclear Valve Assembly Shop.",
                "years": "2009"
            },
            {
                "achivement": "Obtained Certificate 01 eco action 21 Approved by IPSuS",
                "years": "2011"
            },
            {
                "achivement": "KCs Mark for safety valves approved by KOSHA (Korea).",
                "years": "2013"
            }
        ],
        "insurance": [
            {
                "name": "Public Liability",
                "amount": "$ 1,00,000.000",
                "expire_date": "Expires 30 Nov 2024"
            },
            {
                "name": "Professional Indemnity",
                "amount": "$ 5,000.000",
                "expire_date": "Expires 22 Dec 2024"
            },
            {
                "name": "Employer’s Liability",
                "amount": "$ 1,50,000.000",
                "expire_date": "Expires 04 Jan 2025"
            }
        ]
    },

]
    return er