import os
import deepl
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from unidecode import unidecode

def extract(topic, content):
    topicKeys = [
        "uc","area","duration","workingHours","contactHours","ects","lead","auxiliary","ilo","syllabus","evidenceIS","tm","assessments","evidenceTAI","bibliography","syllabusBooks","obs","suggestions"
    ]
    # topicValues = [
    #     "[Curricular Unit]", "[Scientific area]", "[Duration]",
    #     "[Working Hours]", "[Contact Hours]", "[ECTS]",
    #     "[Responsible Teaching Staff]", "[Other Teaching Staff]", "[ILOs]", 
    #     "[Syllabus", "[Evidence ILO & Syllabus]", "[Teaching Methodology]", "[Assessments]", "[Evidence TMs and A & ILOs]", "[Bibliography]", 
    #     "[Syllabus in Books]", "[Observations]", "[Suggestions]" 
    # ]
    topicMap = dict(zip(topicKeys, topicValues))
    _topic = topic
    topic = topicMap.get(topic)

    if topic not in content:
        # content = content#.replace("**", "")\
        #                  .replace("]:", "]")\
        #                  .replace("Topic: ", "")\
        #                  .replace("Topic:", "")
        topics = extractAllTopcis(content)
        topicMap = dict(zip(topicKeys, topics))
        topic = topicMap.get(_topic)
        input(topic)

    start = content.find(topic)
    start = content.find("\n", start)
    if "\n[" in content[start:]:
        end = content.find("\n[", start+1)
    else:
        end = content.find("\n**[", start+1)
    aim = content[start+1:end]

    return locals().get("aim", None)

def extractAllTopcis(content):
    sub = content[:]
    topics = []
    while "[" in sub:
        start = sub.index("[")
        end = sub.index("]", start)
        topic = sub[start+1:end]
        topics.append(topic)
        sub = sub[end+1:]
    while ":\n" in sub and not any(topics):
        end = sub.index(":\n")
        start = sub[end::-1].index("\n")
        input(sub[len(sub[end::-1])+start:end])
        topic = sub[start+1:end]
        topics.append(topic)
        sub = sub[end+1:]
    return topics

def contains(text, aim):
    aim = u'{}'.format(aim.lower())
    return unidecode(aim) in text.lower()

def translator(
        *message: str,
        to: str = "EN-GB",
        origin: str = None,
        formality: str = "more",
        apiKey: str = None
        ) -> (str):
    if apiKey is None:
        auth_key = os.environ.get("DEEPL_API_KEY", None)
        if auth_key is None:
            return message
    translator = deepl.Translator(auth_key)

    try:
        translation = translator.translate_text(
            message, target_lang=to, formality=formality,
            source_lang=origin
            )
    except deepl.exceptions.DeepLException:
        translation = translator.translate_text(
            message, target_lang=to, source_lang=origin
            )

    translations = [trans.text for trans in translation]

    if len(translations) == 1:
        translations = translations[0]

    return translations

def detectLanguage(
        text: str,
        apiKey: str = None
        ) -> (str):
    if apiKey is None:
        auth_key = os.environ.get("DEEPL_API_KEY", None)
        if auth_key is None:
            return message
    translator = deepl.Translator(auth_key)
    translation = translator.translate_text(
        text, target_lang="EN", formality="less"
        )
    return translation.detected_source_lang

"""
================
TO MODULE UPDATE
================
export PYAGET_VERSION=1.0.9 && python3 uploadPackageInPypi.py
"""

def alreadyProduced(fucname: str, path: str):
    found = False
    for file in os.listdir("./output/"):
        if "_".join(fuc.split("_")[1:]) in file:
            found = True
            break
    return found

OFFLINE_MODE = False
COMPACT_MODE = False

FUC_INFO = {
    # UCs de CIBER
    "Fundamentos de Sistemas Operativos e Administracao de Sistemas": ("CIB010101", "Fundamentals of Operating Systems and Systems Administration", "Ciencias Computacionais", 1, 50, 6),
    "Fundamentos de Programacao": ("CIB010102", "Programming Fundamentals", "Ciencias Computacionais", 1, 50, 6),
    "Algebra Linear e Geometria Analitica": ("CIB010103", "Linear Algebra and Analytical Geometry", "Matematica", 1, 50, 6),
    "Sistemas Digitais, Microprocessadores e Arquitetura de Computadores": ("CIB010104", "Digital Systems, Microprocessors and Computer Architecture", "Ciencias Computacionais", 1, 50, 6),
    "Fundamentos de Ciberseguranca": ("CIB010105", "Cybersecurity Fundamentals", "Ciencias Computacionais", 1, 50, 6),
    "Programacao para a Web": ("CIB010201", "Programming for the Web", "Ciencias Computacionais", 1, 50, 6),
    "Algoritmos e Estruturas de Dados": ("CIB010202", "Algorithms and Data Structures", "Ciencias Computacionais", 1, 50, 6),
    "Fundamentos de Sistemas de Informacao e Bases de Dados": ("CIB010203", "Information Systems and Database Fundamentals", "Ciencias Computacionais", 1, 50, 6),
    "Fundamentos de Redes de Computadores": ("CIB010204", "Fundamentals of Computer Networks", "Ciencias Computacionais", 1, 50, 6),
    "Matematica": ("CIB010205", "Maths", "Matematica", 1, 50, 6),
    "Programacao para Dispositivos Moveis": ("CIB020101", "Programming for Mobile Devices", "Ciencias Computacionais", 2, 50, 6),
    "Criptografia": ("CIB020102", "Cryptography", "Ciencias Computacionais", 2, 50, 6),
    "Vulnerabilidades em Aplicacoes Web": ("CIB020103", "Vulnerabilities Web Applications", "Ciencias Computacionais", 2, 50, 6),
    "Probabilidades e Estatistica": ("CIB020104", "Probability and Statistics", "Matematica", 2, 50, 6),
    "Empreendedorismo Tecnologico e Inovacao I": ("CIB020105", "Technological Entrepreneurship and Innovation I", "Ciencias Computacionais", 2, 30, 3),
    "Direito de Privacidade em Seguranca de Informacao": ("CIB030206", "Privacy Law in Information Security", "Direito", 2, 30, 3),
    "Vulnerabilidades em Aplicacoes Mobile": ("CIB030202", "Vulnerabilities Mobile Applications", "Ciencias Computacionais", 2, 50, 6),
    "Tecnologias de Sistemas de Informacao e Bases de Dados": ("CIB020202", "Information Systems and Database Technologies", "Ciencias Computacionais", 2, 50, 6),
    "Tecnologias de Redes de Computadores": ("CIB020203", "Programming for Mobile Devices", "Ciencias Computacionais", 2, 50, 6),
    "Tecnologias de Sistemas Operativos e Administracao de Sistemas": ("CIB020204", "Operating Systems Technologies and Systems Administration", "Ciencias Computacionais", 2, 50, 6),
    "Empreendedorismo Tecnologico e Inovacao II": ("CIB020201", "Technological Entrepreneurship and Innovation II", "Ciencias Computacionais", 2, 30, 3),
    "Metodologia do Trabalho Cientifico": ("CIB020106", "Methodology of Scientific Work", "Ciencias Sociais", 2, 30, 3),
    "Fundamentos de Inteligencia Artificial": ("CIB020206", "Artificial Intelligence Fundamentals ", "Ciencias Computacionais", 3, 50, 6),
    "Vulnerabilidades em Sistemas Informaticos": ("CIB030101", "Vulnerabilities in Computer Systems", "Ciencias Computacionais", 3, 50, 6),
    "Seguranca de Equipamento Ativo de Rede": ("CIB030102", "Security of Active Network Equipment", "Ciencias Computacionais", 3, 50, 6),
    #"Projeto Aplicado ": ("CIB030000", "Applied Project / Internship", "Ciencias Computacionais", 3, 50, 6),
    "Fundamentos de Machine Learning": ("CIB030201", "Machine Learning Fundamentals", "Ciencias Computacionais", 3, 50, 6),
    "Seguranca por Monitorizacao": ("CIB030203", "Security by Monitoring", "Ciencias Computacionais", 3, 50, 6),
    "Ataques de Engenharia Social": ("CIB030204", "Social Engineering Attacks", "Ciencias Computacionais", 3, 50, 6),
    "Epistemologia das Ciencias e Pensamento Critico": ("CIB030205", "Epistemology of Science and Critical Thinking", "Humanisticas", 3, 40, 2),
    "Etica, Privacidade, Responsabilidade e Confiabilidade em Tecnologias Digitais": ("CIB030206", "Ethics, Privacy, Responsibility and Reliability in Cybersecurity", "Etica", 2, 30, 2),
    "Fundamentos de Internet das Coisas": ("CIB010201", "Fundamentals of the Internet of Things", "Ciencias Computacionais", 1, 50, 6),

    # UCs de IA
    "Logica e Conjuntos": ("IA010101", "Logic and Sets", "Matematica", 1, 50, 6),
    "Fundamentos de Programacao": ("IA010102", "Programming Fundamentals", "Ciencias Computacionais", 1, 50, 6),
    "Algebra Linear e Geometria Analitica": ("IA010103", "Linear Algebra and Analytic Geometry", "Matematica", 1, 50, 6),
    "Fundamentos de Inteligencia Artificial": ("IA010104", "Fundamentals of Artificial Intelligence", "Ciencias Computacionais", 1, 50, 6),
    "Psicologia e Cognicao": ("IA010105", "Psychology and Cognition", "Psicologia", 1, 50, 6),
    "Representacao do Conhecimento": ("IA010201", "Knowledge Representation", "Ciencias Computacionais", 1, 50, 6),
    "Fundamentos de Ciencia de Dados": ("IA010202", "Fundamentals of Data Science (Visualization, Communication and Analysis)", "Ciencias Computacionais", 1, 50, 6),
    "Algoritmos e Estruturas de Dados": ("IA010203", "Algorithms and Data Structures", "Ciencias Computacionais", 1, 50, 6),
    "Matematica": ("IA010204", "Mathematics", "Matematica", 1, 50, 6),
    "Processamento de Linguagem Natural": ("IA010205", "Natural Language Processing", "Ciencias Computacionais", 1, 50, 6),
    "Aprendizagem Computacional I": ("IA020101", "Machine Learning I", "Ciencias Computacionais", 2, 50, 6),
    "Gestao de Sistemas de Informacao": ("IA020102", "Information Systems Management", "Ciencias Computacionais", 2, 50, 6),
    "Raciocinio Automatico": ("IA020103", "Automated Reasoning", "Ciencias Computacionais", 2, 50, 6),
    "Probabilidades e Estatistica": ("IA020104", "Probability and Statistics", "Matematica", 2, 50, 6),
    "Aprendizagem Computacional II": ("IA020201", "Machine Learning II", "Ciencias Computacionais", 2, 50, 6),
    "Modelos Linguisticos de Grande Dimensao": ("IA020202", "Large Language Models", "Ciencias Computacionais", 2, 50, 6),
    "Midias Sociais e Inteligencia Artificial": ("IA020203", "Social Media and Artificial Intelligence", "Ciencias Computacionais", 2, 50, 6),
    "Planeamento Automatico": ("IA030102", "Automatic Planning", "Ciencias Computacionais", 3, 50, 6),
    "Introducao aos Sistemas Inteligentes e Autonomos": ("IA030201", "Introduction to Intelligent and Autonomous Systems", "Ciencias Computacionais", 3, 50, 6),
    "Analise Exploratoria de Dados": ("IA030103", "Exploratory Data Analysis", "Matematica", 3, 50, 6),
    "AR & VR": ("IA030106", "AR & VR", "Ciencias Computacionais", 3, 50, 6),
    "Exploracao de Texto": ("IA030109", "Text Exploration", "Ciencias Computacionais", 3, 50, 6),
    "Base de Dados": ("IA030104", "Database", "Ciencias Computacionais", 3, 50, 6),
    "Visao Computacional I": ("IA030107", "Computer Vision I", "Ciencias Computacionais", 3, 50, 6),
    "Interpretacao e Causalidade": ("IA030110", "Interpretability and Causality", "Ciencias Computacionais", 3, 50, 6),
    "Processamento de Dados Audiovisuais": ("IA030105", "Audiovisual Data Processing", "Ciencias Computacionais", 3, 50, 6),
    "Producao de Meios de Comunicacao Digitais": ("IA030108", "Digital Media Production", "Ciencias Computacionais", 3, 50, 6),
    "Web Semantica": ("IA030111", "Semantic Web", "Ciencias Computacionais", 3, 50, 6),
    "Data Warehousing e Big Data": ("IA030202", "Data Warehousing and Big Data", "Ciencias Computacionais", 3, 50, 6),
    "Visao Computacional II": ("IA030204", "Computer Vision II", "Ciencias Computacionais", 3, 50, 6),
    "Sistemas de Apoio a Decisao": ("IA030206", "Decision Support Systems", "Ciencias Computacionais", 3, 50, 6),
    "Estatistica Aplicada (Metodos Numericos)": ("IA030203", "Applied Statistics (Numerical Methods)", "Matematica", 3, 50, 6),
    "Concecao e Desenvolvimento de Jogos": ("IA030205", "Game Design and Development", "Ciencias Computacionais", 3, 50, 6),
    "Exploracao de Dados": ("IA030207", "Data Mining", "Ciencias Computacionais", 3, 50, 6),
}

if __name__ != "__main__":
    from .chatMessagesVersions import UserInterface
    from .pyle import readFile

else:
    from chatMessagesVersions import UserInterface
    from pyle import readFile

    sliceChoice = 1
    openai_key_choice = 4
    openai_key = {
        1: os.environ["OPENAI_API_KEY"], # GPT 4 @GMAIL
        2: os.environ["OPENAI_API_KEY_2"], # GPT 3.5 PT@GMAIL
        3: os.environ["OPENAI_API_KEY_3"], # GPT 3.5 
        4: os.environ["OPENAI_API_KEY_4"], # GPT 3.5 @PIAGET
        5: os.environ["OPENAI_API_KEY_5"], # GPT 3.5 @IST
    }[openai_key_choice]

    gptModelChoice = 2
    gptModel = {
        1: "gpt-3.5-turbo",
        2: "gpt-4"
    }[gptModelChoice]

    fucsPathChoice = 1
    fucsPath = {
        1: "./fucs/syllabus/",
        2: "./fucs/ia",
        3: "./fucs/ciber",
        4: "./output",
        5: "./output/revisedEN",
        6: "./fucs/FUCS_ATUAIS"
    }[fucsPathChoice]

    exportTypeChoice = 1
    exportType ={
        1: "txt",
        2: "json"
    }[exportTypeChoice]

    slices = {
        1: slice(None,None,None),
        2: slice(0,12),
        3: slice(12,24),
        4: slice(24,36),
        5: slice(36,48),
        6: slice(48,58),
    }[sliceChoice]

    txtFiles = [
        name
            for name in os.listdir(fucsPath)
            if name.endswith(".txt") and name != "questions.txt"
    ]

    from pyidebug import debug
    import pandas as pd
    plano = {
        "IA": pd.read_csv("/home/natanael/Documents/IA_CE.csv"),
        "CIBER": pd.read_csv("/home/natanael/Documents/CIBER_CE.csv"),
        "MARKETING": pd.read_csv("/home/natanael/Documents/MARKETING_CE.csv"),
    }
    IA = plano["IA"]
    CIB = plano["CIBER"]
    MKT = plano["MARKETING"]

    IA.fillna("", inplace=True)
    CIB.fillna("", inplace=True)
    MKT.fillna("", inplace=True)

    def getContactHours(table, data, by):
        aimRow = table[table[by].str.contains(data)]
        tipology = {
            T: (int(aimRow[T].iloc[0]) if any(aimRow[T]) else 0)
                for T in ["T","TP","PL","TC","S","E","OT"]
        }
        return tipology

    def splitContactHours(hours: dict[str:int]):
        if hours["T"] > 0:
            output = (hours.pop("T"),)
        elif hours["TP"] > 0:
            output = (hours.pop("TP"),)
        else:
            output = (0,)
        output += (sum(hours.values()),)

        output = [int(o) for o in output]
        return output

    def getDocentes(table, data, by):
        contactHours = getContactHours(table, data, by)
        contactHoursSplit = splitContactHours(contactHours)
        docentes = getData(table, "Docente", data, by)
        docentesHours = zip(docentes, contactHoursSplit)
        return docentesHours

    def getData(table, column, data, by):
        columns = [
            col
                for col in table.columns
                if column.upper() in col.upper()
        ]
        aimRow = table[table[by].str.contains(data)]
        output = [
            (aimRow[col].iloc[0] if any(aimRow[col]) else None)
                for col in columns
        ]
        return output

    for fuc in txtFiles[slices]:
        if "Software" not in fuc and "copy" not in fuc:
            continue
        # if not any(input("")):
        #     continue
        # if "_PT" in fuc or "copy" in fuc:
        #     continue
        # print(f"{fuc = }")
        # input()
        #fucName = " ".join(fuc.split("_")[1:])
        fucName = fuc
        fucName, ext = fucName.split(".")
        _fucName = fucName.replace("_", " ")
        # if alreadyProduced(fuc, "./output/"):
        #     continue

        #input(f"Generate the follow FUC '{_fucName}'? (ENTER)")
        (fucCode, fucNameEN, fucArea, fucYear,
        fucContactHours, fucECTS) = FUC_INFO.get(unidecode(_fucName), 6*(None,))

        fucECTS = 6
        fucContactHours = 45
        fucNameEN = _fucName
        fucArea = "Ciências Computacionais"\
            if "PT" in fuc\
            else "Computational Science"
        fucYear = 3

        # if fucCode is None:
        #     print("Fail!")
        #     input(unidecode(_fucName))

        if fucCode is None or "CIB" in fucCode:
            db = CIB
        elif "IA" in fucCode:
            db = IA
        else:
            db = MKT

        fucLead, fucAuxiliary = getDocentes(
            db, _fucName, by="Unidade Curricular"
            )

        print(
            f"UC: {_fucName}",
            "Regente: {} ({} hours)".format(*fucLead),
            "Auxiliar: {} ({} hours)".format(*fucAuxiliary),
            sep="\n"
        )

        fucYear = {
            1: "first",
            2: "second",
            3: "last"
        }.get(fucYear, None)
        expertise = {
            "IA": "Digital Technologies and Artificial Intelligence",
            "CIB": "Digital Technologies and Cibersecurity",
            "MKT": "Marketing"
        }.get(fuc.split("_")[0], None)
        fucWorkingHours = fucECTS*25 if fucECTS is not None else None

        fucName = fucName.replace(" ", "_")

        with open(f"{fucsPath}/{fuc}", "r", encoding="utf-8") as file:
            fucContent = file.read().replace("  ","")
        syllabus = fucContent

        # if "None" in fuc:
        #     continue

        print("Syllabus:", syllabus, sep="\n")

        message = f"Generating FUC to {fucName.title()}"
        delim = len(message)*"="
        print(delim, message, delim, sep="\n", end="\n\n")
        interface = UserInterface(
            1.4, syllabus, fucNameEN, fucContactHours, fucWorkingHours, fucECTS,
            expertise, fucNameEN, fucYear, fucArea, fucLead, fucAuxiliary,
            compactMode=COMPACT_MODE, apiKey=openai_key, showQuestions=False,
            offline=OFFLINE_MODE, gptModel=gptModel
            )

        print(interface.answers["All"])
        input()

        interface._UserInterface__translateAnswersToPT()

        print(interface.translations["All"])
        input()

        # interface.exportQuestions(
        #     f"questions", "txt", "./output"
        #     )
        interface.exportAnswers(
            f"./output/{fuc}", exportType, "./output"
            )
        interface.exportTranslations(
            f"{fucCode}_{fucName}_PT", exportType, "./output"
        )
        # interface.exportFucTemplate(
        #     f"{fucCode}_{fucName}", exportType, "./output"
        #     )

        #interface._UserInterface__translateAnswersToPT()
        #interface.showTranslations()
        # interface.exportTranslations(
        #     f"{fucCode}_{fucName}_translation", exportType, "./output"
        # )

        # interface.exportAnswersTranslations("fullText", "txt")

        # interface.sendByEmail(
        #     "answers.txt",
        #     send_from="natanael.quintino@ipiaget.pt",
        #     send_to="natanael.quintino@ipiaget.pt"
        #     )

# import docx2txt
# import docx

# def getText(filename):
#     doc = docx.Document(filename)
#     fullText = []
#     for para in doc.paragraphs:
#         fullText.append(para.text)
#         input(para.style)
#     return '\n'.join(fullText)