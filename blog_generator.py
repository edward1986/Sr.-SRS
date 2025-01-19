import random
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import json
import feedparser
import requests
file_path = "topics.json"

def load_topics():
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data.get("topics", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to save topics to the file
def save_topics(topics):
    with open(file_path, "w") as file:
        json.dump({"topics": topics}, file, indent=2)

# Function to add topics without duplication
def add_topics(new_topics):
    existing_topics = load_topics()
    for topic in new_topics:
        if topic not in existing_topics:
            existing_topics.append(topic)
    save_topics(existing_topics)

# New topics to be added
rss_url = 'https://www.manilatimes.net/business/foreign-business/feed/'
feed = feedparser.parse(rss_url)

# Parse the RSS feed entries
new_entries = []
new_guids = set()

for entry in feed.entries:
    new_entries.append(entry.title)

add_topics(new_entries)
def ensure_model_available(model_name):
    """Ensure the model[
        "Researchers", "Data Scientists", "Common People", "Students", "Entrepreneurs",
        "Marketers", "Tech Enthusiasts", "Environmentalists", "Educators", "Healthcare Professionals",
        "Investors", "Content Creators", "Policy Makers", "Journalists", "Travel Enthusiasts",
        "Parents", "Artists", "Fitness Enthusiasts", "Engineers", "Historians",
        "Teachers", "Developers", "Startup Founders", "Writers", "Bloggers",
        "Gamers", "Environmental Activists", "Social Workers", "Consultants", "Small Business Owners",
        "Public Speakers", "Podcasters", "Psychologists", "Sociologists", "Economists",
        "Architects", "Designers", "Photographers", "Lawyers", "Accountants",
        "Athletes", "Personal Trainers", "Chefs", "Food Critics", "Fashion Designers",
        "Musicians", "Film Makers", "Storytellers", "Book Lovers", "Minimalists",
        "Philosophers", "Technologists", "AI Enthusiasts", "Robotics Experts", "Urban Planners",
        "Astronomers", "Mathematicians", "Physicists", "Chemists", "Biologists",
        "Medical Researchers", "Veterinarians", "Farmers", "Futurists", "Cryptocurrency Enthusiasts",
        "HR Professionals", "Recruiters", "Sales Experts", "E-commerce Entrepreneurs", "Digital Nomads",
        "Remote Workers", "Mental Health Advocates", "Mindfulness Coaches", "Public Relations Experts", "Event Planners",
        "Adventure Seekers", "Wildlife Conservationists", "Marine Biologists", "Astronauts", "Space Enthusiasts",
        "DIY Hobbyists", "Car Enthusiasts", "Pet Owners", "Nature Photographers", "Gardeners",
        "Home Decorators", "Interior Designers", "Outdoor Enthusiasts", "Sports Fans", "Social Media Influencers",
        "YouTubers", "Film Critics", "Comedians", "Lifestyle Bloggers", "Relationship Coaches",
        "Spiritual Guides", "Religious Leaders", "Ethicists", "Activists", "Human Rights Advocates",
        "Policy Analysts", "Data Analysts", "Startup Mentors", "Cultural Historians", "Linguists"
    ] is available locally or pull it if missing."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if model_name not in result.stdout:
            print(f"Model {model_name} not found locally. Attempting to pull...")
            pull_result = subprocess.run(
                ["ollama", "pull", model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if pull_result.returncode != 0:
                raise Exception(f"Error pulling model: {pull_result.stderr.strip()}")
            print(f"Model {model_name} pulled successfully.")
        else:
            print(f"Model {model_name} is already available locally.")
    except Exception as e:
        raise Exception(f"Error ensuring model availability: {e}")

def fetch_word_of_the_day():
    """Fetch the Word of the Day from Merriam-Webster."""
    try:
        url = "https://www.merriam-webster.com/word-of-the-day"
        response = subprocess.run(
            ["curl", "-s", "-o", "/tmp/response.html", "-w", "%{http_code}", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if response.stdout.strip() != "200":
            print(f"Failed to fetch Word of the Day. HTTP Status: {response.stdout.strip()}")
            return None
        with open("/tmp/response.html", "r") as file:
            html_content = file.read()
        word = subprocess.run(
            ["grep", "-oP", '(?<=<h2 class="word-header-txt">)[^<]+', "/tmp/response.html"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        ).stdout.strip()
        if word:
            print(f"Fetched Word of the Day: {word}")
            return word
        print("Word of the Day not found in the response.")
        return None
    except Exception as e:
        print(f"Error fetching Word of the Day: {e}")
        return None

def generate_random_inputs():
    topics = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            topics = json.load(f)
    else:
        topics = [
        "It literally takes fire and brimstone to transport gold to Earth's surface",
  "New study explains how gold reaches Earth’s surface",
  "From magma to treasure: Scientists uncover secrets of gold’s journey through magmatic fluids",
  "Gold-sulfur complex found to play crucial role in gold deposit formation",
  "77% of coastal areas threatened by saltwater intrusion",
  "Enhanced Raman microscopy of cryofixed specimens for sharper chemical imaging",
  "Nanobubbles as game-changers for chemistry and sustainability",
  "Could AI robots replace human astronauts in space?",
  "NASA reveals new Mars helicopter design inspired by Ingenuity's success",
  "Northern lights to ring in New Year's Eve across parts of the United States",
  "How does space affect the brain? Groundbreaking ISS experiment reveals insights",
  "Octopus DNA indicates total collapse of Antarctic ice sheet may be close",
  "Paleontologists discover new species of sauropodomorph dinosaur in China",
  "Coolest space missions coming in 2025",
  "Big plans for NASA next year",
  "10 jaw-dropping space photos that defined 2024",
  "10 times space missions went very wrong in 2024",
  "Revolutionizing connectivity: Sateliot’s 5G IoT network in space",
  "Near-Earth asteroid 2024 YW8's extremely close encounter",
  "Astronomers explore 3D structure of the Milky Way galaxy",
  "Hotter white dwarfs get puffier, researchers find",
  "Jones polynomial calculations based on Majorana zero modes",
  "Get ready for the 'New Year Comet' — What to expect from Comet ATLAS",
  "NASA’s Europa Clipper features 3D printed topology-optimized bracket",
  "NASA develops swimming robots to find life on Jupiter’s moon",
  "Mirror bacteria could wreak havoc on life and the environment, scientists warn",
  "Emirates Astronomical Society spots 16 major lunar events in 2025",
  "How old are Saturn’s rings? Studies suggest they could be 4.5 billion years old",
  "Underwater volcano off US West Coast 'primed to erupt' in 2025",
  "NASA redefines the future of flight with innovative probes",
  "The most important scientific breakthroughs of 2024",
  "Ten cool science stories we almost missed",
        "Why did Filipinos buy more food additives from sari-sari stores in 2024?",
  "Peso strengthens back to P57 vs dollar level",
  "Google Labs launches Whisk, a new image generation tool",
  "Ellen Adarna covers baby's face in Christmas family photo",
  "WINNER Mino’s military discharge could be revoked",
  "Squid Game Season 2: Character guide and reviews",
  "Filipinos adapt to rising prices with smart spending",
  "Camembert cheese compounds improve memory and learning",
  "Bitcoin loses $2 trillion market cap post-Christmas",
  "MMFF review: 'The Kingdom' imagines alternate reality for PH",
  "IMF urges restoration of LandBank and DBP capital",
  "OpenAI’s ChatGPT experiences post-Christmas outage",
  "Goodbye to the $100 bill: US confirms ban",
  "Denise Julia responds to BJ Pascual controversy",
  "Psychological insights on cultivating mystery with potential partners",
  "Favorite holiday cocktail recipes from around the world",
  "Philippines has 2nd largest share of branded residences in Asia",
  "Rosé and Bruno Mars dominate global charts with 'APT.'",
  "Reuse hacks for old pasta sauce jars",
  "Lee Junho undergoes intensive tax audit investigation",
  "Samsung One UI 7 introduces HDR fine-tuning",
  "Pig Chinese Horoscope 2025: Insights on overnight success",
  "Ruby 3.4 programming language brings performance updates",
  "First-ever solar night panel unveiled: How it works with moonlight",
  "Captain America’s replacement achieves milestones quickly",
  "Crypto donations for tax benefits",
  "Gold prices rise amid holiday trading",
  "Denzel Washington gets baptized and receives minister’s license",
  "Cyberpunk 2077 players question lingering food graphics issues",
  "Floki DAO proposes European ETP launch",
  "ERC caps reserve market price at P25/kWh",
  "Unreal Engine 5.5 shows massive performance improvements",
  "Weird Windows 11 bug prevents security updates",
  "Gold forecast for 2025: Spot price predictions",
  "Yin-yang mindset proposed to heal polarized societies",
  "DA proposes removing brand labels from imported rice",
  "Lab-grown cocoa set to revolutionize the industry",
  "Super veggie rich in calcium and vitamin C gains attention",
  "Meta’s gains for a third straight year: Challenges and factors",
  "Elon Musk’s continued dominance and wealth accumulation in 2024",
  "Tax hike risks amidst economic turmoil in the UK",
  "Which scent do you find the most soothing?",
  "What is a language you love to listen to even if you don’t understand it?",
  "Oceans or mountains? Why?",
  "What color would you choose to describe yourself?",
  "What’s something you’ve accomplished as an adult that your younger self would be proud of?",
  "What tasks make you feel like your best self?",
  "What’s your Enneagram number, and how does it influence your self-care practices?",
  "What do you love most about your personality?",
  "What do you look for and need in your friendships?",
         "Suspect in New Orleans Attack Is Identified: What We Know",
  "What we know about Shamsud-Din Jabbar, the suspect in the New Orleans attack",
  "Pels, in Miami for game, 'devastated' after attack",
  "Why bollards weren’t in place before New Orleans deadly attack",
  "South Korea's Choi orders immediate action on aircraft inspection as crash probe ramps up",
  "Blame mounts over concrete structure at Muan airport for amplifying crash impact",
  "More than 170 killed after South Korean jet crash-lands at airport. Here’s what we know",
  "Expert focuses on structure close to runway plane skidded off in South Korea",
  "Taiwan president vows to boost the island's defense budget as China threats rise",
  "Taiwan president wants exchanges with China, sees lack of goodwill",
  "Taiwan's Lai says island must show 'determination' to defend itself",
  "Taiwan’s presidential office runs first ‘tabletop’ simulation of Chinese military escalation",
  "IN PHOTOS: New Year celebrations around the world",
  "Around the world in fireworks: New Year celebrations in pictures",
  "World greets 2025 after sweltering year of Olympics, turmoil and Trump",
  "PHOTO COLLECTION: New Year’s Eve",
  "How do you feel best supported in hard times?",
  "What small joys bring light to your day?",
  "What do you love most about our relationship?",
  "What’s your earliest memory?",
  "What’s one thing you’d tell yourself at my age?",
  "What’s a favorite memory of your parents?",
  "Which characteristics do you think you inherited from our parents?",
  "Do you have any tattoos?",
  "What Netflix show or movie are you watching?",
  "What are you currently reading?",
  "What do you do for enjoyment?",
  "What projects are you working on that bring you joy?",
  "How do you unwind after work?",
        "Cold hands are common in winter: When are they a health issue?",
  "DOH: Private hospitals should bare info on charity beds, fees",
  "PhilHealth hikes benefit packages for heart patients",
  "Eye drops recalled nationwide due to fungal contamination",
  "Morgan Stanley sees potential growth in surgical robotic stocks",
  "AI tech gains traction at hospitals",
  "TRENDS Study highlights AI's new healthcare horizons",
  "AI-driven digital health revolution transforming medical decision-making",
  "Preparing healthcare education for an AI-augmented future",
  "The world’s first virtual hospital is here",
  "Amazon’s next big acquisition prediction",
  "A public health emergency is waiting at the bottom of the antibiotic resistance cliff",
  "Stocks in healthcare sector set to surge in 2025",
  "Human error blamed in Ascension data breach affecting 5.6 million patients",
  "Healthcare giant admits over 5 million patients affected by ransomware attack",
  "NHS issues warning as norovirus cases rise",
  "Biden administration proposes new cybersecurity rules for healthcare",
  "NHS to begin world-first trial of AI tool to identify type 2 diabetes risk",
  "Hospitals trial AI to spot type 2 diabetes risk",
  "Groundbreaking AI tool to predict diabetes risk years in advance",
  "Top 7 health stories of 2024",
  "Pig kidney transplants and new schizophrenia drug among 2024 medical breakthroughs",
  "Royal Papworth Hospital’s 'lungs in a box' technology boosts transplants",
  "Lab-grown blood cells created without donors",
  "NHS coping with 'upsurge' in flu cases",
  "Families urged to stay home to stop contagious virus spread",
  "Visiting restrictions imposed on hospitals amid respiratory illness surge",
  "Welsh hospitals reintroduce face masks for visitors and staff",
  "Reliance acquires Karkinos Healthcare for Rs 375 crore",
        "Experts raise the alarm about incoming massive volcanic eruption",
        "New study explains how gold reaches Earth’s surface",
        "Stunning James Webb images reveal the birth of a Milky Way twin",
        "Chinese scientists' major discovery innovating pesticide industry",
        "US researchers to study viability of carbon capture in fish farms",
        "Oldest saber-toothed creature found, rewriting the story of mammal evolution",
        "Scientists discover a 'Goldilocks' zone for DNA organization, opening new doors for drug development",
        "Fly adopts wasp defense to foil predator",
        "Uplift underway in Finland’s Kvarken Archipelago",
        "Astronomers spot an enormous explosion from the 1st black hole ever photographed",
        "Saturn’s rings might be much older than had been thought",
        "Astronauts send Christmas message to Earth from International Space Station",
        "James Webb telescope's big year for cosmology",
        "Webb observes protoplanetary disks that contradict models of planet formation",
        "Christmas night lights: Geomagnetic storm to dazzle 10 US states with Northern Lights",
        "Two populations of dark comets in the solar system could explain where Earth got its oceans",
        "Distant quasar found with 140 trillion times Earth's ocean water",
        "Marmosets call each other by 'names' with distinct vocalizations",
        "Scientists explore negative time in quantum experiments",
        "NASA's Perseverance rover captures oddball rock on Mars",
        "When will we know if NASA’s Parker Solar Probe survived ‘touching’ the sun?",
        "Earth's orbit is crowded with over 1,000 collision warnings per day",
        "Mars orbiter captures a winter wonderland on summertime Mars",
        "500-million-year-old Ecdysozoan fossil embryos found in China",
        "James Webb Space Telescope catches monster black hole napping after 'overeating'",
        "Giant sloths and mastodons coexisted with humans for millennia in the Americas",
        "Ants outshine humans in teamwork",
        "Mars opposition 2025 — How to see the Red Planet at its biggest and brightest",
        "Fruit flies in space — Chinese astronauts show experiment on Tiangong Station",
        "Scientists take a closer look at rare particles called hypernuclei",
        "Dazzling star cluster creates a cosmic holiday wreath",
        "Milky Way’s fluffiest system found a new planet",
        "Chinese satellite poses no danger but gives US observers a ‘spectacular’ light show",
        "Ocean explorers film enchanting marine snow drifting like a symphony through the deep sea",
        "Scientists create 'twisted light' so robots can see like shrimp",
        "Scientists discover a mysterious new predator living deep in the ocean",
        "Asteroid alert! Giant asteroid narrowly misses Earth this Christmas",
        "In Carl Sagan’s death, an amazing life lesson",
        "Gloria in Excelsis Deo! What was the Star of Bethlehem?",
        "Polymer coating gives electron microscopes enhanced 3D vision",
        "Researchers quantify the speed of human thought",
        "Humans almost went extinct 930,000 years ago",
        "Inside the faraway planet where scientists have found shocking signs of life",
        "Santa’s speed on Christmas Eve calculated",
        "NASA’s X-59 silent supersonic aircraft ready to fly for the first time",
        "New study reveals how leaves’ resilience to raindrops might help in agriculture and renewable energy",
        "Revolutionary maps reveal Earth’s geological secrets",
        "The Moon's significant impact on animals worldwide",
        "The controversy over cannibalism",
        "Home foundations are crumbling due to a mineral",
          "MLBB new hero Kalea: Skills, Abilities, Release Date, & More",
  "FC Tactical announces v2.1 update with Guild vs Guild battles and more",
  "Boom Beach free rewards and how to claim them",
  "Vivo X200 Ultra camera specs leak: 200 MP telephoto and 4K recording",
  "Tongits Go: Strategies for success and holiday rewards",
  "Infinix HOT 50 Pro+ released in 4 new colors",
  "Realme Neo7 SE to feature MediaTek Dimensity 8400 SoC",
  "Mobile Legends: Bang Bang – Best Lukas Build",
  "Apple no longer top smartwatch brand in the world",
  "HUAWEI Mate X6 pre-orders with early bird offers",
  "Naruto Ultimate Ninja Storm series sales milestone",
  "Solo Leveling: ARISE – New Jeju Island Raid Update",
  "Anker unveils high-speed USB-C chargers",
  "PUBG Mobile A11 Royale Pass leaks: Upcoming skins and rewards",
  "OPPO Find X8 Mini: Compact design with impressive battery life",
  "HONOR Magic7 RSR Porsche Design unveiled",
  "Samsung Galaxy M16 design and specs revealed",
  "AI phones could sustain chip sector amid slowed data center spending",
  "Samsung to reduce 2025 foldable phone targets due to weak sales",
  "Sony celebrates 30 years of PlayStation",
  "Micron advances HBM4 development, mass production in 2026",
  "Nothing Phone 3a series to get major performance upgrades",
  "Best After Christmas Sales 2024: Top deals",
  "Microsoft leads passkey adoption, aims to eliminate passwords",
  "Samsung Galaxy S25 family's rumored release date",
  "Best Boxing Day deals on games, consoles, and tech",
  "Google launches Android XR platform for extended reality",
  "Xiaomi unveils Cross Door Mijia refrigerator",
  "AMD’s CES 2025 press conference: How to watch",
  "Nobara Linux introduces custom KDE Plasma desktop",
  "ChatGPT hidden content rewrite highlights risks",
  "JBL Xtreme 3 discounted for Christmas",
  "Sony XM5 headphones hit lowest-ever price",
  "Qwen's QVQ rivals top AI models in visual reasoning",
  "Lifetime Microsoft Office subscription deals",
  "50,000-year-old baby mammoth remains found in Siberia",
  "Ruijie Networks' cloud platform flaws expose devices to attacks",
  "Zero-bezel iPhone unlikely before 2026",
  "Escape From Tarkov wipe and patch date confirmed",
  "Chinese OEMs to increase battery capacity by 2025",
  "Google Maps integration in Hyundai vehicles",
         "Moon's bygone magnetic field present 2 billion years ago",
    "UK's biggest dinosaur footprint site uncovered",
    "Jurassic highway: Hundreds of dinosaur footprints found in UK quarry",
    "Watch video of 'dinosaur highway' found with hundreds of giant Jurassic-era tracks",
    "166-million-year-old dinosaur tracks found in the UK",
    "Scientists Predict Loss Of Deep Snow In Most Of U.S.",
    "Biologists Call For A Halt To ‘Mirror Life’ Research",
    "Mirror bacteria could pose major health risks",
    "Scientists Sound Alarm: 'Mirror Life' Microbes Pose Catastrophic Risk to Humanity",
    "Scientists Sound a Warning About Mirror Life",
    "New resource available to help scientists better classify cancer subtypes",
    "Quadrantid meteor shower to be visible on early Friday morning",
    "Viewing the 2025 Quadrantid Meteor Shower",
    "When and where to see the Quadrantids, 2025's first meteor shower",
    "Quadrantid meteor shower: How to watch the first 'shooting stars' of 2025 rain over Earth tonight",
    "Science shorts: dsm-firmenich funds HMOs studies, top 10 research news and more",
    "Ancient brain circuit stabilizes gaze during movement in early development",
    "Detecting disease with a single molecule: Nanopore-based sensors could transform diagnostics",
    "The Chilling Discovery That Could Point to Life Beyond Earth",
    "The Sky This Week from January 3 to 10: Earth’s closest approach to the Sun",
    "How to watch the Quadrantid meteor shower as it peaks this week",
    "See the First Meteor Shower of the Year, Six Planets in One Night, and More in January",
    "January Night Sky Brings Parade Of Planets",
    "A new computational model can predict antibody structures more accurately",
    "Gene expression in the human brain: cell types become more specialized, not just more numerous",
    "New artificial muscle mimics natural tissue with high elasticity and toughness",
    "Dead stars can celebrate 2 New Years every second with nearby cosmic fireworks",
    "Scientists Trace Fast Radio Burst to Surprise Source For First Time",
    "An alien signal hit Earth in 2022. Astronomers have now found its original source",
    "10,000-kilometer precision: Astronomers pinpoint origin of mysterious space signals",
    "NASA Scientists Discover 'Dark Comets' Come in Two Populations.",
    "2 populations of dark comets in the solar system could tell researchers where the Earth got its oceans",
    "Surveillance of Earth by “Dark Comets”",
    "What is a dark comet?",
    "Bats surf storm fronts during continental migration",
    "Migrating bats “surf” on storms, study finds",
    "How maggots may be key to solving rape cases",
    "These Migrating Bats Are Surfers — Sort Of",
    "Advancing space medicine: a global perspective on in-orbit research and future directions",
    "Undersea volcano off Oregon coast could erupt this year, geologists predict",
    "Scientists predict an undersea volcano eruption near Oregon in 2025",
    "Warning as underwater volcano off US West Coast 'is primed to erupt' in 2025",
    "Undersea Volcano Threat: The Hidden Risks of Axial Seamount",
    "Unlocking Ocean Secrets: NASA’s PACE and SWOT Reveal a Hidden World",
    "NASA's Parker Solar Probe beams home 1st detailed update after record-breaking approach to the sun",
    "Parker Solar Probe reports healthy status after solar encounter",
    "The Amazing NASA Probe Footage Flying Through The Sun's Corona",
    "NASA’s Parker Solar Probe Offers Assurance Of Its Well-Being",
    "Massive 'Grand Design' Spiral Galaxy Found Just a Billion Years After Big Bang",
    "Maine’s Scopan Lake",
    "Genetic mechanism of alternating sexes in walnut trees has some parallels to sex determination in humans",
    "How plants and trees are able to predict volcano eruptions",
    "Nanoparticle technique gauges bite force in tiny C. elegans worms",
    "SpaceX delays launch of Thuraya 4 mission for UAE satellite company",
    "Live coverage: SpaceX to launch Thuraya 4-NGS telecommunications satellite on Falcon 9 rocket from Cape Canaveral",
    "SpaceX readies for next Falcon 9 rocket launch from Florida coast",
    "SpaceX Thuraya 4 mission now on for Friday",
    "January 2025: Science as art, fellows capture NIEHS research in vibrant images",
    "Reed beds offer eco-friendly solution for sludge pollution management",
    "Elon Musk is standing in the way as Jeff Bezos reaches for orbit",
    "Transforming the Moon Into Humanity’s First Space Hub",
    "Space Billionaires Count Down To Their Rocket Race To The Moon",
    "Astronomy and space: highlights of 2024",
    "Double Trouble? Two large asteroids flying at high speed approaching Earth on January 3 says NASA",
    "NASA tracks two massive asteroids approaching Earth today at this time",
    "Is Earth ready? Asteroid 2024 YF7 zips past Earth at over 13 km/s",
    "Alert! NASA Warns Of Massive Asteroid Racing Toward Earth Tomorrow At Over 74,500 KMPH",
    "Treating gut injuries caused by too much sugar consumption",
    "An Astrobiology Spinoff? Microbe Recovered From Mars 2020 Cleanroom May Have Commercial Applications",
    "Rewriting the Rules: Scientists Tinker With the “Clockwork” Mechanisms of Life",
    "Diversifying DNA origami: Generative design tool relies on grammar rules for finding best shape",
    "Don’t burst that bubble: research explores nanobubble stability",
    "Scientists reveal the distribution pattern of butterfly diversity in China",
    "Using an Oil Industry Framework to Map Space Resources",
    "Near-Earth Asteroid 2025 AC very close encounter: an image – 2 Jan. 2025.",
    "Magmatic Fluids and Melts May Lie Beneath Dormant German Volcanoes",
    "New Theory Solves Paradox of Schrödinger's Cat by Claiming We're in a Multiverse",
    "Some black holes at the centers of galaxies have a buddy − but detecting these binary pairs isn’t easy",
    "Hourglass body shape is ideal for hula hooping, says study",
    "Geometrically modulated contact forces enable hula hoop levitation",
    "Mathematicians are hula-hooping to understand how it defies gravity",
    "Study suggests 'hourglass' body shape ideal for sustained hula-hooping",
    "Wildfire Surges Tied to Past Climate Shifts: Study",
    "Ice samples show ancient link between wildfires and climate change, OSU study finds",
    "Wildfire activity surged during Ice Age's abrupt climate shifts, study suggests",
    "Intuitive Machines enhances lunar and deep space data transmission services",
    "Laboratory Studies On The Influence of Hydrogen on Titan-like Photochemistry",
    "HYPSO-2 satellite monitors harmful algae from space",
    "These are the space stocks to watch in 2025",
    "Is 2025 the year we find a real SpaceX competitor?",
    "What to Expect in 2025",
    "The Conversation: From New Commercial Moon Landers to Asteroid Investigations, Expect a Slate of Exciting Space Missions in 2025",
    "Video: NASA Open Science Data Repository OSDR Chats Featuring Celebration of 30 Years of Open Science",
    "Novel SiC UV Instrumentation Development with Potential Applications for the Habitable Worlds Observatory",
    "Chinese researchers use CRISPR to improve seed oil content and flowering time",
    "Mars Helicopter Ingenuity Takes Off And Spins As Perseverance Watches",
    "Multiscale Force Sensing with Photon-Avalanching Nanocrystals",
    "New 'all-optical' nanoscale sensors of force access previously unreachable environments",
    "New 'all-optical' nanoscale sensors of force",
    "Following the coronal temperature profiles of stars",
    "Could There Be Bacteria Living on Mars Today?",
    "Mars' Hidden Methane Deposits Could Be Underneath the Crust, Host Alien Life",
    "We finally know where to look for life on Mars",
    "Dark Sky Field Talks",
    "Accelerated Biological Evolution In Outer Space: Insights From Numerical Analysis",
    "Improving Earthquake Early Warning Access for the Deaf Community",
    "Earth-Size Planet Found In TOI 700 System's Habitable Zone",
    "UAF professor proves it was Denali's Fault",
    "Unusual binary system hosts a massive fast-spinning white dwarf",
    "Bacteria to the rescue: A sustainable solution for growing organoids",
    "The Webb Captures Spectra of Trans-Neptunian Objects, and Reveals a History of Our Solar System",
    "The Minor Planet Chiron Is Strange – And So Is Its Ice",
    "Webb Telescope’s Dazzling Discovery: Icy Relics Reveal the Secrets of Our Solar System’s Origins",
    "Webb captures best view ever of icy objects from the early solar system",
    "Meteor showers, eclipses and supermoons. What you can expect for 2025 in astronomy",
    "Your Ultimate Guide To Stargazing And Astronomy In 2025",
    "When to see ‘blood’ moons, eclipses and meteor showers in 2025",
    "Full moons of 2025: Names, dates and everything you need to know",
    "He thought it was gold, but inside this 4.6 billion-year-old meteorite he found something even stranger",
    "Australian man who kept rock for 17 years learns it's 4.6-billion-year-old Maryborough meteorite",
    "Man thinks rock is gold, turns out to be ancient meteorite worth lot more",
    "Man finds mysterious rock that turns out to be 5 billion-year-old meteorite worth fortune",
    "Could Habitable White Dwarf Planets Retain Their Oceans? Maybe.",
    "How does the number of wings on a seed affect spin as it falls?",
    "Humans will soon be able to mine on the moon—but should we? Four questions to consider",
    "Earth’s balance at risk': Mining the Moon could trigger an apocalypse, warns NASA",
    "Lunar Gold Rush: Navigating the Ethical Minefield of Moon Mining",
    "Here Are 4 Things We Need to Consider Before We Mine Our Moon",
    "Scientists Re-Create the Microbial Dance That Sparked Complex Life",
    "Black holes can squash star formation, James Webb Space Telescope finds",
    "King Solomon's Mines Were Far Cleaner Than Previously Thought",
  "Instagram testing expired story highlights feature",
  "Pokémon Go Mega Abomasnow counters and moveset explained",
  "Nvidia RTX 5090 spotlight at CES 2025",
  "Evangelion's Rei and Asuka new PVC Nendoroid figures",
  "Lenovo ThinkVision M14t Gen2 review",
  "2024 winners and losers: Samsung and Apple",
         "Dozens dead as passenger plane crashes in Kazakhstan",
  "Russian missile likely cause of Azerbaijan Airlines crash",
  "38 dead and 29 survivors in Azerbaijani airliner crash in Kazakhstan",
  "Passenger captures moments before and after plane crash in Kazakhstan",
  "Biden slams Russia’s Christmas Day assault on Ukraine",
  "Putin 'inhumane,' Zelensky says, as Russia attacks Ukrainian power grid",
  "Ukraine: Zelensky condemns Russia's Christmas Day attack",
  "Russia carried out massive strike on Ukrainian energy system",
  "Pope launches 2025 Jubilee Year with opening of Holy Doors",
  "Pope Francis inaugurates 2025 Jubilee with Holy Door opening",
  "Celebrating Jubilee 2025",
  "Pope Francis opens Holy Door to kick off jubilee year",
  "Pope calls for 'arms to be silenced' in Christmas appeal",
  "Man finds bear in living room as Japan readies license to kill",
  "Bear found under heated table in Fukushima home is captured",
  "South Korean president Yoon defies Christmas summons",
  "South Korea's Yoon defies agency summons over martial law",
  "Chinese embassy demands release of Huawei CFO arrested in Canada",
  "Gemini's Deep Research AI feature expands globally",
  "Ford Ranger Raptor Diesel drag races Toyota Hilux Revo GR Sport",
        "Study sheds light on how gold reaches the Earth’s surface",
  "New study explains how gold reaches Earth’s surface",
  "It literally takes fire and brimstone to transport gold to Earth's surface",
  "Scientists crack the code of how gold reaches Earth’s surface",
  "How to catch the Quadrantids, the first meteor shower of 2025",
  "Breakthrough discovery links new gene to autism",
  "WWI fighter plane hack inspires breakthrough in cancer treatment",
  "Space billionaires count down to their rocket race to the Moon",
  "A total eclipse of the Moon, Saturn’s rings ‘disappear’, meteors and more: your guide to the southern sky in 2025",
  "Out-of-this-world space missions to watch in 2025",
  "Massive Antarctic icebergs' split from glaciers may be unrelated to climate change",
  "Metal-organic frameworks as nanoplatforms for combination therapy in cancer treatment",
  "Magnificent Moon in January 2025: Southern Hemisphere sky highlights",
  "Starlink launch concludes record-breaking 2024 for SpaceX",
  "German astronomers discover three new hydrogen-deficient pre-white dwarfs",
  "Greek scientists digitally reconstruct skull of 200,000-year-old dwarf hippopotamus",
  "Magnetism redefined: Nanoscale discovery powering future technology",
  "NASA's Lunar Trailblazer mission to measure lunar surface in 2025",
  "Ice world dynamics: Antarctic fast-ice thickness variability",
  "Introducing HORNET: Novel RNA structure visualization method",
  "Quantum mechanics and negative time with photon-atom interactions",
  "A young exoplanet's atmosphere doesn't match its birthplace",
  "Mars mission cleanroom found to be harboring new bacterial species",
  "10 amazing things discovered on Mars in 2024",
  "Space science in 2024: Moon missions, Martian milestones, astrophysics discoveries, and more",
  "New study uncovers key insights into protein interactions in Duchenne muscular dystrophy",
  "The newly discovered Archaeocursor asiaticus is Asia's earliest-known ornithischian dinosaur",
  "Saturn's moon Titan captured by the James Webb Space Telescope",
  "How early experiences shape genes, brain health, and resilience",
  "Interstellar formation of lactaldehyde: A key in the methylglyoxal pathway",
  "A stellar explosion 650 million light-years away captured by Hubble",
  "SpaceX Dragon Crew-8 returns to Earth after 235 days in space",
  "Manta rays inspire faster swimming robots and better water filters",
  "Avalanches and katabatic winds ring in the Martian New Year",
  "Scientists find record high-energy cosmic ray electrons, but origin remains elusive",
  "Africa splits apart, forming a new ocean faster than predicted",
  "Earth's space debris problem is jeopardizing the internet and astronaut missions",
  "China's two new radio telescopes commence operation",
  "Quantum Kinetics' Arc Reactor achieves first-ever sustained nuclear fusion",
  "Massive weak spot in Earth's magnetic field is growing and could have huge consequences",
  "Boeing astronauts to return with SpaceX after extended time in space",
  "Biocompatibility of novel marine collagen on periodontal ligament fibroblasts",
  "Mystery of 194-year-old world famine-causing volcanic eruption solved",
  "Reasons why life on Earth rarely makes fluorine-containing compounds",
  "Northern lights displays hit a 500-year peak in 2024",
  "Boltz-1: A new open-source AI tool for drug discovery",
  "Cosmic X-ray mystery solved: Scientists discover new class of exploding stars",
  "Asteroid alert: New Year asteroid 2024 YJ9 set to skim Earth's cosmic backyard",
  "NASA reveals new Mars helicopter design inspired by Ingenuity's success",
  "Discovery of the distant spiral galaxy Zhúlóng",
  "Lake Razzaza: A shrinking oasis shaped by salinity",
  "Have scientists solved the chicken or egg problem?",
        "Philippines logs over 4,000 measles, rubella cases",
        "Community action to curb dengue crisis in PH",
        "Food sharing practices in Caribbean countries using intergenerational interviews",
        "Determinants of gender-equitable attitudes among adult men in Malawi",
        "Bird flu kills 20 big cats at Washington animal sanctuary",
        "Bird flu concerns lead LA County officials to warn against feeding pets raw food",
        "AI-designed 'nanocages' mimic viral behavior for gene therapy",
        "Study: Exercise boosts brain function for 24 hours",
        "17-year-old from Jerusalem contracts polio",
        "Effects of smokeless tobacco on cancer incidence: meta-analysis",
        "Linking genetics of dyslexia to brain structure",
        "Heart attack deaths spike during winter holidays",
        "Teabags release billions of microplastics",
        "Study links coffee to lower head and neck cancer risk",
        "H5N1 detected in dairy cattle for the first time",
        "Mongolia confirms outbreak of meningococcal disease",
        "Tips for managing Seasonal Affective Disorder",
        "Hospital wards 'full to bursting' with respiratory patients",
        "The Role of Blockchain in Government Systems",
        "The Future of Self-Driving Cars",
        "How AI is Transforming Video Games",
        "Ethical Concerns in Facial Recognition Technology",
        "The Rise of Open Source in Artificial Intelligence",
        "How 5G Technology Impacts Rural Connectivity",
        "The History and Evolution of Cloud Computing",
        "Renewable Energy Storage Innovations",
        "The Role of Big Data in Fighting Climate Change",
        "How Augmented Reality is Redefining Travel",
        "Understanding the Metaverse: Beyond Gaming",
        "Ethical Dilemmas in Biometric Surveillance",
        "Space Mining: Is it Feasible?",
        "Robotics in Everyday Life",
        "The Evolution of Smart Cities",
        "AI in Customer Service: Boon or Bane?",
        "Data Science Trends Shaping the Future",
        "The Impact of IoT on Healthcare Delivery",
    
        # Health Topics
        "The Science Behind Sleep Cycles",
        "How Mental Health Awareness is Changing Society",
        "The Role of Technology in Elderly Care",
        "Preventing Chronic Diseases Through Lifestyle Changes",
        "Exploring the Benefits of Telemedicine",
        "How AI is Transforming Cancer Detection",
        "Genetic Engineering in Modern Medicine",
        "The Role of Gut Health in Mental Wellbeing",
        "Understanding the Rise of Anti-Microbial Resistance",
        "Fitness Trends in 2024",
        "The Future of Preventive Healthcare",
        "How Wearable Devices Revolutionize Personal Fitness",
        "The Impact of Climate Change on Public Health",
        "How Nutrition Affects Brain Function",
        "The Role of Meditation in Chronic Pain Management",
        "Digital Detox and Its Impact on Mental Health",
        "The Benefits of Mindfulness in Stress Management",
        "How Personalized Medicine is Changing Treatment",
        "The Evolution of Vaccine Technology",
        "Yoga: An Ancient Solution to Modern Stress",
    
        # Education Topics
        "The Rise of Online Learning Platforms",
        "How AI is Transforming Personalized Education",
        "The Future of Hybrid Learning Models",
        "The Impact of Gamification in Education",
        "How Technology Helps Overcome Learning Disabilities",
        "The Role of VR in Virtual Classrooms",
        "Why Emotional Intelligence Should Be Taught in Schools",
        "Benefits of Cross-Disciplinary Education",
        "The Future of Coding Bootcamps",
        "Addressing the Digital Divide in Education",
        "How Peer Learning Boosts Engagement",
        "The Role of Open Educational Resources",
        "How Project-Based Learning Improves Retention",
        "STEM Education: Encouraging Girls in Tech",
        "The Evolution of Traditional Libraries in the Digital Age",
        "Why Financial Literacy is Essential for Students",
        "How Online Certifications Are Reshaping Careers",
        "The Role of Podcasts in Self-Learning",
        "Language Learning in a Globalized World",
        "How Parent Involvement Enhances Student Performance",
    
        # Business and Economics Topics
        "How E-Commerce is Shaping Retail",
        "The Future of Subscription-Based Business Models",
        "How AI is Enhancing Employee Productivity",
        "Ethical Challenges in Corporate Data Usage",
        "The Evolution of Customer Loyalty Programs",
        "The Impact of Digital Transformation on Small Businesses",
        "How Startups are Innovating Supply Chains",
        "The Role of Behavioral Economics in Marketing",
        "Remote Work: Productivity Challenges and Benefits"
    ]
    
    styles = [
        "Origami Artists",
    "Cartographers",
    "Climate Scientists",
    "Geologists",
    "Volcanologists",
    "Storm Chasers",
    "Hurricane Researchers",
    "Tornado Enthusiasts",
    "Urban Historians",
    "Civic Planners",
    "Transportation Designers",
    "Automotive Engineers",
    "Drone Pilots",
    "Space Engineers",
    "Satellite Designers",
    "Rocket Enthusiasts",
    "AI Trainers",
    "Machine Learning Engineers",
    "Cybersecurity Experts",
    "Penetration Testers",
    "Digital Artists",
    "Motion Graphics Designers",
    "Augmented Reality Developers",
    "Holography Experts",
    "3D Printing Specialists",
    "Prototyping Engineers",
    "Industrial Designers",
    "Material Scientists",
    "Nanotechnologists",
    "Biochemists",
    "Geneticists",
    "Microbiologists",
    "Plant Scientists",
    "Agricultural Technologists",
    "Aquaponics Enthusiasts",
    "Permaculture Designers",
    "Ecotourism Experts",
    "Sustainable Architects",
    "Green Builders",
    "Zero Waste Advocates",
    "Upcycling Artists",
    "Circular Economy Specialists",
    "Clean Energy Researchers",
    "Solar Panel Engineers",
    "Wind Energy Specialists",
    "Hydropower Experts",
    "Battery Technologists",
    "Electric Vehicle Enthusiasts",
    "Energy Storage Innovators",
    "Waste Management Experts",
    "Recycling Advocates",
    "Composting Enthusiasts",
    "Environmental Policy Experts",
    "Biodiversity Advocates",
    "Endangered Species Researchers",
    "Wetland Conservationists",
    "Mountain Climbers",
    "Cave Explorers",
    "Arctic Explorers",
    "Desert Survival Experts",
    "Deep Sea Explorers",
    "Polar Researchers",
    "Adventure Photographers",
    "Cultural Storytellers",
    "Folklore Researchers",
    "Traditional Crafts Enthusiasts",
    "Festivals Organizers",
    "Ethnomusicologists",
    "Traditional Dancers",
    "Calligraphers",
    "Typography Designers",
    "Sign Painters",
    "Street Artists",
    "Muralists",
    "Protest Artists",
    "Activist Designers",
    "Political Cartoonists",
    "Social Documentary Filmmakers",
    "War Photographers",
    "Crisis Management Experts",
    "Humanitarian Workers",
    "Refugee Advocates",
    "Disability Activists",
    "Accessible Technology Designers",
    "Inclusive Educators",
    "Interpreters",
    "Translators",
    "Language Preservationists",
    "Dialect Coaches",
    "Cognitive Scientists",
    "Behavioral Economists",
    "Neuroscientists",
    "Psychiatric Researchers",
    "Addiction Counselors",
    "Rehabilitation Experts",
    "Wellness Coaches",
    "Positive Psychologists",
    "Happiness Researchers",
    "Holistic Healers",
         "Archaeologists",
    "Game Designers",
    "Puzzle Enthusiasts",
    "Mythologists",
    "Paleontologists",
    "Astrobiologists",
    "Metaverse Creators",
    "Blockchain Developers",
    "Web3 Enthusiasts",
    "App Developers",
    "Cryptographers",
    "Zoologists",
    "Epidemiologists",
    "Astrologers",
    "Numismatists",
    "Philatelists",
    "Toy Collectors",
    "Historical Reenactors",
    "Craftsmen",
    "Leatherworkers",
    "Blacksmiths",
    "Woodworkers",
    "Beekeepers",
    "Cheesemakers",
    "Winemakers",
    "Brewmasters",
    "Tea Sommeliers",
    "Whiskey Connoisseurs",
    "Luxury Brand Experts",
    "Sneaker Collectors",
    "Fashion Historians",
    "Tattoo Artists",
    "Bodybuilders",
    "Yoga Instructors",
    "Pilates Trainers",
    "Climbers",
    "Parkour Enthusiasts",
    "Survivalists",
    "Bushcrafters",
    "Stunt Performers",
    "Escape Room Designers",
    "Magic Enthusiasts",
    "Illusionists",
    "Stand-Up Comedians",
    "Screenwriters",
    "Playwrights",
    "Voice Actors",
    "Radio Hosts",
    "Audiobook Narrators",
    "Music Producers",
    "Sound Engineers",
    "Songwriters",
    "Lyricists",
    "DJ Artists",
    "Classical Musicians",
    "Orchestra Conductors",
    "Street Performers",
    "Circus Artists",
    "Jugglers",
    "Acrobats",
    "Equestrians",
    "Cyclists",
    "Runners",
    "Marathon Trainers",
    "Triathletes",
    "Swimmers",
    "Scuba Divers",
    "Freedivers",
    "Surfing Enthusiasts",
    "Skiers",
    "Snowboarders",
    "Skaters",
    "Roller Derby Athletes",
    "Mixed Martial Artists",
    "Fencers",
    "Archers",
    "Chess Players",
    "Board Game Designers",
    "Fantasy Writers",
    "Sci-Fi Enthusiasts",
    "Cosplayers",
    "Fanfiction Writers",
    "Graphic Novel Artists",
    "Comic Collectors",
    "Animators",
    "VFX Artists",
    "3D Modelers",
    "Game Streamers",
    "Urban Explorers",
    "Treasure Hunters",
    "Forensic Scientists",
    "Crime Writers",
    "Private Investigators",
    "Ethnographers",
    "Sociolinguists",
    "Educational Technologists",
    "Knowledge Managers",
    "Information Architects",
    "Museum Technologists",
    "Cultural Preservationists",
    "Ecosystem Restorers",
        "Researchers", "Data Scientists", "Common People", "Students", "Entrepreneurs",
        "Marketers", "Tech Enthusiasts", "Environmentalists", "Educators", "Healthcare Professionals",
        "Investors", "Content Creators", "Policy Makers", "Journalists", "Travel Enthusiasts",
        "Parents", "Artists", "Fitness Enthusiasts", "Engineers", "Historians",
        "Teachers", "Developers", "Startup Founders", "Writers", "Bloggers",
        "Gamers", "Environmental Activists", "Social Workers", "Consultants", "Small Business Owners",
        "Public Speakers", "Podcasters", "Psychologists", "Sociologists", "Economists",
        "Architects", "Designers", "Photographers", "Lawyers", "Accountants",
        "Athletes", "Personal Trainers", "Chefs", "Food Critics", "Fashion Designers",
        "Musicians", "Film Makers", "Storytellers", "Book Lovers", "Minimalists",
        "Philosophers", "Technologists", "AI Enthusiasts", "Robotics Experts", "Urban Planners",
        "Astronomers", "Mathematicians", "Physicists", "Chemists", "Biologists",
        "Medical Researchers", "Veterinarians", "Farmers", "Futurists", "Cryptocurrency Enthusiasts",
        "HR Professionals", "Recruiters", "Sales Experts", "E-commerce Entrepreneurs", "Digital Nomads",
        "Remote Workers", "Mental Health Advocates", "Mindfulness Coaches", "Public Relations Experts", "Event Planners",
        "Adventure Seekers", "Wildlife Conservationists", "Marine Biologists", "Astronauts", "Space Enthusiasts",
        "DIY Hobbyists", "Car Enthusiasts", "Pet Owners", "Nature Photographers", "Gardeners",
        "Home Decorators", "Interior Designers", "Outdoor Enthusiasts", "Sports Fans", "Social Media Influencers",
        "YouTubers", "Film Critics", "Comedians", "Lifestyle Bloggers", "Relationship Coaches",
        "Spiritual Guides", "Religious Leaders", "Ethicists", "Activists", "Human Rights Advocates",
        "Policy Analysts", "Data Analysts", "Startup Mentors", "Cultural Historians", "Linguists"
    ]

    input_text = random.choice(topics)
    no_words = 50000
    blog_style = random.choice(styles)
    return input_text, no_words, blog_style
class AICrew:
    """AI Crew with specialized roles."""
    def __init__(self, model_name):
        self.model_name = model_name
    def run_ollama(self, prompt):
        """Run a prompt through the Ollama model."""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                raise Exception(f"Error running Ollama: {result.stderr.strip()}")
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {e}"
    
    def creative_write(self, topic):
        prompt = f"""
        Write an engaging blog post about the topic: {topic}. 
        Include interesting anecdotes, relatable examples, and a strong conclusion.
        """
        return self.run_ollama(prompt)

    def fact_check(self, content):
        prompt = f"""
        Verify the accuracy of the following text: {content}. 
        Highlight any inaccuracies and provide confidence levels for each fact.
        """
        return self.run_ollama(prompt)

    def optimize_for_seo(self, content, keyword):
        prompt = f"""
        Optimize the following blog post for SEO. 
        Improve keyword density, add meta descriptions, and ensure readability.
        Content: {content}
        """
        return self.run_ollama(prompt)

    def edit_content(self, content):
        prompt = f"""
        Edit the following blog post for tone, grammar, and readability. 
        Make it polished and professional. Content: {content}
        """
        return self.run_ollama(prompt)
def get_ollama_response(input_text, no_words, blog_style, word_of_the_day, model_name="llama3"):
    """Generate a blog using Ollama with the provided inputs."""
    today_year = datetime.now().year
    prompts = [
        # Conversational Prompt
        f"""
            Write a blog for {blog_style} professionals about the topic "{input_text}". Make it engaging and easy to read, with approximately {no_words} words. 
            Use the word "{word_of_the_day}" creatively and naturally. Include:
            - Practical examples or relatable anecdotes to illustrate key points.
            - Synonyms and alternative phrases for "{input_text}" to improve SEO.
            - Eye-catching headings and bullet points for better readability.
            - A concluding call-to-action to inspire further thought or action.with seo optimize
        """,

        # Research-Oriented Prompt
        f"""
            Develop an in-depth, SEO-optimized blog for {blog_style} professionals on the topic "{input_text}". The blog should:
            - Be around {no_words} words.
            - Use "{word_of_the_day}" thoughtfully in a relevant context.
            - Include statistics, references, or data-driven insights to support the content.
            - Highlight challenges, solutions, or innovations related to the topic.
            - Use structured formatting, with headings, subheadings, and lists to organize the information.with seo optimize
        """,

        # Storytelling Prompt
        f"""
            Create a narrative-style blog for {blog_style} professionals that focuses on the topic "{input_text}". The blog should:
            - Be {no_words} words long.
            - Include the word "{word_of_the_day}" in a meaningful and creative way.
            - Start with a captivating story or anecdote to draw readers in.
            - Include a moral, takeaway, or lesson that ties back to the topic.
            - Use vivid language and relatable examples to make the content engaging.with seo optimize
        """,

        # Listicle Prompt
        f"""
            Write a blog for {blog_style} professionals in the form of a listicle about "{input_text}". The blog should:
            - Contain {no_words} words and use the word "{word_of_the_day}" naturally.
            - Include at least 5 main points or items, each with a brief explanation or example.
            - Use headings and bullet points to make the content scannable.
            - End with a summary or call-to-action to encourage further engagement. with seo optimize
        """,

        # Opinion Piece Prompt
        f"""
            Write an opinion-based blog for {blog_style} professionals about the topic "{input_text}". The blog should:
            - Be {no_words} words long.
            - Use "{word_of_the_day}" in a bold and creative way to emphasize your perspective.
            - Present a clear stance on the topic and support it with logical arguments.
            - Address potential counterarguments and provide rebuttals.
            - Conclude with a strong and memorable statement to leave an impact.with seo optimize
        """,

        # How-To Guide Prompt
        f"""
            Create a detailed how-to guide for {blog_style} professionals about "{input_text}". The blog should:
            - Be {no_words} words in length and include "{word_of_the_day}" in a practical context.
            - Outline clear, step-by-step instructions with examples or tips.
            - Use headings, subheadings, and numbered lists for easy navigation.
            - Address common challenges and provide solutions for each step.with seo optimize
        """,

        # FAQ-Style Prompt
        f"""
            Write a blog for {blog_style} professionals in a FAQ format about the topic "{input_text}". The blog should:
            - Be around {no_words} words long and include "{word_of_the_day}" in a creative way.
            - Address at least 5 common questions or concerns related to the topic.
            - Provide concise and informative answers with actionable advice.
            - Use headings or bold text for each question to improve readability.with seo optimize
        """,

        # Problem-Solution Prompt
        f"""
            Write a blog for {blog_style} professionals focused on solving a specific problem related to "{input_text}". The blog should:
            - Be {no_words} words long.
            - Use "{word_of_the_day}" in the context of addressing or overcoming the problem.
            - Clearly define the problem and explain why it matters.
            - Offer practical solutions or strategies to tackle the issue.
            - Conclude with a summary or call-to-action encouraging readers to act.with seo optimize
        """,

        # Analytical Prompt
        f"""
            Create an analytical blog for {blog_style} professionals that examines "{input_text}". The blog should:
            - Be approximately {no_words} words in length.
            - Include "{word_of_the_day}" to emphasize key points or findings.
            - Break down the topic into smaller components or trends for analysis.
            - Use data, graphs, or references to support arguments.
            - Conclude with insights or predictions based on the analysis.with seo optimize
        """,

        # Creative Prompt
        f"""
            Write a creative blog for {blog_style} professionals about the topic "{input_text}". The blog should:
            - Be around {no_words} words and incorporate "{word_of_the_day}" in an imaginative way.
            - Use storytelling, metaphors, or fictional scenarios to explore the topic.
            - Focus on originality and unique perspectives to captivate readers.
            - Provide a meaningful takeaway or lesson at the end.with seo optimize
        """,
        f"Write a blog {blog_style}: Why {input_text} No Longer Works in {today_year} and What to Do Instead. Be around {no_words} words and include '{word_of_the_day}'.",
        f"Write a blog How {blog_style} Professionals Can Benefit from {input_text} in {today_year}. Write {no_words} words and creatively use '{word_of_the_day}'.",
        f"Write a blog 5 Underrated Tools for {blog_style} Professionals to Master {input_text} in {today_year}. Cover this in {no_words} words with '{word_of_the_day}' included.",
        f"Write a blog What {input_text} Means for {blog_style} Professionals in {today_year}. Analyze in {no_words} words while emphasizing '{word_of_the_day}'.",
        f"Write a blog How {blog_style} Professionals Can Master {input_text} in {today_year}. Provide actionable tips in {no_words} words and include '{word_of_the_day}'.",
        f"Write a blog Why {input_text} Is Critical for {blog_style} Success in {today_year}. Dive into the topic in {no_words} words, using '{word_of_the_day}' naturally.",
        f"Write a blog Lessons on {input_text} for {blog_style} Professionals in {today_year}. Share insights in {no_words} words, creatively using '{word_of_the_day}'.",
        f"Write a blog The Evolution of {input_text} for {blog_style} Professionals in {today_year}. Cover its journey in {no_words} words and include '{word_of_the_day}'.",
        f"Write a blog How {blog_style} Professionals Can Overcome Challenges with {input_text} in {today_year}. Offer solutions in {no_words} words, using '{word_of_the_day}'.",
        f"Write a blog Behind the Scenes: {input_text} for {blog_style} in {today_year}. Unveil insights in {no_words} words with a focus on '{word_of_the_day}'.",
        f"Write a blog Top Strategies for {blog_style} Professionals to Excel in {input_text} in {today_year}. Outline in {no_words} words while incorporating '{word_of_the_day}'.",
        f"Write a blog 5 Ways {blog_style} Professionals Can Leverage {input_text} in {today_year}. Highlight approaches in {no_words} words, using '{word_of_the_day}' creatively.",
        f"Write a blog The Role of {input_text} in {blog_style} Growth in {today_year}. Explain in {no_words} words while weaving in '{word_of_the_day}'.",
        f"Write a blog Why {input_text} Matters for {blog_style} in {today_year}. Discuss its significance in {no_words} words and incorporate '{word_of_the_day}'.",
        f"Write a blog The Future of {input_text} for {blog_style} Professionals Beyond {today_year}. Speculate in {no_words} words, making '{word_of_the_day}' central to the narrative.",
        f"Write a blog 5 Key Insights on {input_text} for {blog_style} in {today_year}. Provide them in {no_words} words and include '{word_of_the_day}' creatively.",
        f"Write a blog How {input_text} Is Shaping the Future of {blog_style} in {today_year}. Write {no_words} words and make '{word_of_the_day}' a focus point.",
        f"Write a blog The Importance of {input_text} for {blog_style} Professionals in {today_year}. Highlight why in {no_words} words, incorporating '{word_of_the_day}' naturally.",
        f"Write a blog How to Use {input_text} Effectively as a {blog_style} Professional in {today_year}. Cover this in {no_words} words, using '{word_of_the_day}' practically.",
        f"The Challenges of {input_text} in {blog_style} and How to Overcome Them in {today_year}. Write {no_words} words and creatively use '{word_of_the_day}'.",
        f"How {blog_style} Professionals Can Navigate {input_text} in {today_year}. Provide guidance in {no_words} words and include '{word_of_the_day}'.",
        f"Write a blog 5 Lessons Learned from {input_text} for {blog_style} Professionals in {today_year}. Share these in {no_words} words while incorporating '{word_of_the_day}'.",
        f"Write a blog The Power of {input_text} for {blog_style} in {today_year}. Explain its influence in {no_words} words, ensuring '{word_of_the_day}' is highlighted.",
        f"Write a blog Why {input_text} Should Be a Priority for {blog_style} in {today_year}. Discuss in {no_words} words while weaving '{word_of_the_day}' into the narrative.",
        f"Write a blog How {blog_style} Professionals Can Improve Their Work Through {input_text} in {today_year}. Cover this in {no_words} words and use '{word_of_the_day}'.",
        f"Write a blog The Impact of {input_text} on {blog_style} Success in {today_year}. Analyze in {no_words} words while making '{word_of_the_day}' central to the discussion.",
        f"Write a blog The Role of {input_text} in Transforming {blog_style} in {today_year}. Write about this in {no_words} words, ensuring '{word_of_the_day}' is included.",
        f"Write a blog How {input_text} Can Revolutionize {blog_style} in {today_year}. Explore the potential in {no_words} words with '{word_of_the_day}' creatively used.",
        f"Write a blog The Ultimate Guide to {input_text} for {blog_style} Professionals in {today_year}. Write this in {no_words} words, incorporating '{word_of_the_day}' throughout."


    ]                     
    prompt = random.choice(prompts)
    try:
        ensure_model_available(model_name)
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            raise Exception(f"Error running model: {result.stderr.strip()}")
        print("Ollama Response Retrieved Successfully.")
        crew = AICrew(model_name)
    
        # Step 2: Fact Checker validates the draft
        print("\nFact Checker: Validating content...")
        fact_check_results = crew.fact_check(result.stdout.strip())
        print("Fact check results:\n", fact_check_results)
    
        # Step 3: SEO Specialist optimizes the draft
        print("\nSEO Specialist: Optimizing for SEO...")
        seo_optimized = crew.optimize_for_seo(result.stdout.strip(), word_of_the_day)
        print("SEO-optimized content:\n", seo_optimized)
    
        # Step 4: Editor refines the final draft
        print("\nEditor: Polishing content...")
        final_content = crew.edit_content(seo_optimized)
        print("Final edited content:\n", final_content)
        promptTitle = f"what is the title  {final_content}?"
        resultTitle = subprocess.run(
            ["ollama", "run", model_name, promptTitle],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return {
            "blog": (final_content),
            "title": resultTitle.stdout.strip()
        }
    except Exception as e:
        return f"Error during query: {e}"

def send_email(recipient_email, subject, content):
    """Send the generated blog content via email."""
    try:
        sender_email = "edwardlance.lorilla@ustp.edu.ph"
        sender_password = "fpkb thiy cwmx vknz"

        # Set up the MIME message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject.replace("\n", " ").strip()

        # Attach the blog content
        message.attach(MIMEText(content, "plain"))

        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent successfully to {recipient_email}.")
    except Exception as e:
        print(f"Error sending email: {e}")


if __name__ == "__main__":
    # Generate random inputs
    
    word_of_the_day = fetch_word_of_the_day() or "innovation"
    
    # List of recipients
    recipients = [
        "edwardlorilla2081.edwardlancelorilla@blogger.com",
        "edwardlorilla2082.edwardlancelorilla@blogger.com",
        "edwardlorilla2088.edwardlancelorilla@blogger.com",
        "edwardlorilla2091.edwardlancelorilla@blogger.com",
    ]
    for recipient in recipients:
        topic, word_count, audience = generate_random_inputs()
        print(f"Generating content for: {recipient}")
        
        # Generate unique blog content for each recipient
        blog_content = get_ollama_response(topic, word_count, audience, word_of_the_day)
        
        print("Generated Blog Content:\n")
        print(blog_content)
        
        # Send the blog content via email
        if "Error" not in blog_content:
            send_email(
                recipient_email=recipient,
                subject=blog_content["title"],
                content=blog_content["blog"]
            )
            print(f"Email sent to {recipient}")
        else:
            print(f"Blog content generation failed for {recipient}. Email will not be sent.")
