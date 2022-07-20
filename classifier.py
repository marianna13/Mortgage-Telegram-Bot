import spacy
from numpy import mean, array

nlp = spacy.load("ru_core_news_lg")

tags = [
    "вторичного жилья",
    "для новостроек",
    "для семей",
    "с государственной поддержкой",
]

data = {
    "intents": [
        {"вторичного жилья": ["вторичное жилье", "вторичный рынок", "старое"]},
        {"для новостроек": ["новое жилье", "новостройки"]},
        {"для семей": ["семьи", "семейное"]},
        {
            "с государственной поддержкой": [
                "поддержка",
                "государственное",
                "гоусдарство",
            ]
        },
    ]
}


def get_tag(message):
    statement1 = nlp(message)
    sims = {k: [] for k in tags}
    for tag, p in zip(tags, data["intents"]):
        for pattern in p[tag]:
            statement2 = nlp(pattern)
            statement1.similarity(statement2)
            sims[tag].append(statement1.similarity(statement2))

    sims_mean = {k: mean(sim) for k, sim in sims.items()}
    if any(sm > 0.1 for sm in sims_mean.values()):
        return max(sims_mean, key=sims_mean.get)
    else:
        return "not recognized"


print(get_tag("кофта"))
