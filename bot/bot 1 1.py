from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from deep_translator import GoogleTranslator
import telebot
import wikipedia


API_TOKEN = '6475136928:AAEkhSCur00CZHsJaxx14-oR9og1ckX_Ijc'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def classifica_procura(message):
    tradutorPortugues = GoogleTranslator(source= "en", target= "pt")
    tradutorIngles = GoogleTranslator(source= "pt", target= "en")
    palavras_chave = {
        "World History": ["history", "historical", "past", "ancient", "civilization"],
        "Science and Technology": ["science", "technology", "innovation", "discovery"],
        "Arts and Culture": ["art", "culture", "artist", "cultural", "painting", "sculpture"],
        "Geography": ["geography", "landforms", "countries", "cities", "maps"],
        "Food and Cuisine": ["food", "cuisine", "recipe", "cooking", "dish"],
        "Sports": ["sports", "athlete", "game", "competition", "tournament"],
        "Music": ["music", "musician", "genre", "instrument", "song"],
        "Literature": ["literature", "author", "book", "novel", "poem"],
        "Movies": ["movies", "film", "actor", "actress", "director"],
        "Television": ["television", "tv show", "series", "channel"],
        "Fashion": ["fashion", "style", "designer", "clothing", "model"],
        "Business": ["business", "industry", "company", "economy", "entrepreneur"],
        "Finance": ["finance", "investment", "stock", "market", "economics"],
        "Politics": ["politics", "government", "policy", "election", "democracy"],
        "Health and Fitness": ["health", "fitness", "nutrition", "exercise", "wellness"],
        "Travel": ["travel", "tourism", "destination", "adventure", "journey"],
        "Education": ["education", "school", "learning", "student", "teacher"],
        "Technology": ["technology", "innovation", "digital", "gadget", "internet"],
        "Environment": ["environment", "sustainability", "climate", "nature", "ecology"],
        "Animals": ["animals", "wildlife", "species", "zoo", "conservation"],
        "Psychology": ["psychology", "mind", "behavior", "therapy", "counseling"],
        "Religion": ["religion", "belief", "faith", "spirituality", "god"],
        "Space": ["space", "universe", "galaxy", "astronomy", "cosmos"],
        "Law": ["law", "legal", "justice", "court", "crime"],
        "Artificial Intelligence": ["artificial intelligence", "AI", "machine learning", "robotics", "automation"],
        "History of Art": ["history of art", "art movements", "artists", "art periods"],
        "Human Rights": ["human rights", "civil rights", "freedom", "equality", "justice"],
        "Social Media": ["social media", "platforms", "networking", "community", "online"],
        "Gaming": ["gaming", "video games", "gamer", "console", "esports"],
        "Cooking": ["cooking", "recipes", "ingredients", "chef", "baking"],
        "Photography": ["photography", "photographer", "camera", "photo", "pictures"],
        "Science Fiction": ["science fiction", "sci-fi", "fictional", "futuristic", "aliens"],
        "Mythology": ["mythology", "mythical", "legend", "gods", "folklore"],
        "Crime": ["crime", "criminal", "investigation", "detective", "mystery"],
        "Engineering": ["engineering", "engineer", "design", "innovation", "construction"],
        "Architecture": ["architecture", "architect", "building", "design", "structure"],
        "Psychiatry": ["psychiatry", "mental health", "psychiatric", "therapy", "diagnosis"],
        "Fashion Design": ["fashion design", "designer clothes", "style", "couture", "runway"],
        "Astronomy": ["astronomy", "cosmology", "stars", "planets", "telescope"],
        "Philosophy": ["philosophy", "philosopher", "thought", "ethics", "morality"],
        "Anthropology": ["anthropology", "culture", "society", "human behavior", "evolution"],
        "Business Management": ["business management", "leadership", "strategy", "entrepreneurship", "organization"],
        "Marketing": ["marketing", "advertising", "branding", "promotion", "market research"],
        "Economics": ["economics", "economic theory", "macroeconomics", "microeconomics", "economic policy"],
        "Fashion Modeling": ["fashion modeling", "modeling industry", "runway", "catwalk", "fashion show"],
        "Sociology": ["sociology", "social science", "social behavior", "society", "culture"],
        "Communication": ["communication", "media", "journalism", "public relations", "speech"],
        "Human Anatomy": ["human anatomy", "anatomy", "physiology", "body structure", "organs"],
        "Chemistry": ["chemistry", "chemical reactions", "elements", "molecules", "laboratory"],
        "Physics": ["physics", "physical science", "laws of motion", "energy", "particles"],
        "Biology": ["biology", "life science", "organisms", "ecosystems", "genetics"],
        "Botany": ["botany", "plants", "flora", "plant biology", "gardening"],
        "Zoology": ["zoology", "animals", "fauna", "animal behavior", "wildlife"],
        "Meteorology": ["meteorology", "weather", "climate", "atmosphere", "forecast"],
        "Oceanography": ["oceanography", "oceans", "marine life", "sea", "aquatic ecosystems"],
        "Geology": ["geology", "earth science", "rocks", "minerals", "geological processes"],
        "Paleontology": ["paleontology", "fossils", "prehistoric life", "dinosaurs", "evolution"],
        "Astrophysics": ["astrophysics", "cosmology", "stellar phenomena", "black holes", "galactic structure"],
        "Environmental Science": ["environmental science", "environmental studies", "ecology", "sustainability", "conservation"],
        "Neuroscience": ["neuroscience", "brain science", "neurons", "cognitive functions", "neurological disorders"],
        "Computer Science": ["computer science", "computing", "programming", "algorithms", "software engineering"],
        "Cybersecurity": ["cybersecurity", "information security", "cyber threats", "data protection", "network security"],
        "Data Science": ["data science", "big data", "data analysis", "machine learning", "data visualization"],
        "Mathematics": ["mathematics", "mathematical theory", "calculus", "algebra", "geometry"],
        "Statistics": ["statistics", "statistical analysis", "probability", "data interpretation", "inferential statistics"],
        "Psychology": ["psychology", "psychological theory", "mental processes", "behavioral patterns", "psychotherapy"],
        "Cognitive Science": ["cognitive science", "cognition", "mental representation", "consciousness", "perception"],
        "Linguistics": ["linguistics", "language", "linguistic theory", "semantics", "syntax"],
    }
    mensagemtraduzida = tradutorIngles.translate(message.text)
    assunto = mensagemtraduzida

    categoria_encontrada = False
    for categoria, chave in palavras_chave.items():
        if any(chave in assunto.lower() for chave in chave):
            try:
                resposta = wikipedia.summary(assunto)
                resposta = tradutorPortugues.translate(resposta)
                categoria = tradutorPortugues.translate(categoria)
                bot.reply_to(message, f"Classificação: {categoria}\n\n{resposta}")
                categoria_encontrada = True
                break
            except wikipedia.exceptions.DisambiguationError as e:
                bot.send_message(message.chat.id, text=f"Existem múltiplas opções para {assunto}. Tente ser mais específico.")
                bot.send_message(message.chat.id, text="Opções relacionadas: " + ", ".join(e.options))
                break
            except wikipedia.exceptions.PageError:
                pass

    if not categoria_encontrada:
        bot.send_message(message.chat.id, text="Por favor, mande algo mais relevante")

bot.polling()