"""
FUC maker chat messages versions
"""

# =========================
# Suggestion to assessments
# =========================
# The distribution of assessments over the course should be structured as follows:
# - Two exams, each accounting for 15% of the total grade, to assess understanding of digital representation of information, logical functions, architecture of a processor, arithmetic circuits, and memory system.
# - Weekly quizzes, contributing 5% each to the final grade, to evaluate knowledge on internal organization of a computer, study of a didactic architecture, sequential circuits, and input/output peripherals.
# - Bi-weekly individual assignments, worth 10% each, focused on practical applications and problem-solving related to the topics covered.

SHOW_ORDER = [
    "nome",
    "name",
    "area cientifica",
    "duracao",
    "horas de trabalho",
    "horas de contato",
    "percentagem de horas de contato",
    "ECTS",
    "observacao",
    "docente",
    "outros docentes",
    "OA",
    "ILO",
    "conteudo programatico",
    "syllabus",
    "coerenciaILO_S",
    "coherenceILO_S",
    "metodologia",
    "mehotdology",
    "avaliacoes",
    "assessments",
    "coerenciaAvaliacoes",
    "coherenceAvaliacoes",
    "bibliografia"
    ]

CONTACT_HOURS_REQUIREMENTS = [
    "divide the ideal contact hours into teaching typologies that cover the entire curricular unit",
    "tutorial hours (TO) should be less than 5 hours",
    "display it on table",
    "Not showing the hours spent by topic"
    "optimize your answer and display it on table",
    # "estimate the number of hours of each tipology to each syllabus topics",
    # "optimize your answer and display it on table, shorten the syllabus topics description"
]

ILO_REQUIREMENTS = [
    "a) Intended Learning Outcomes (ILOs) can be: a1) Knowledge‐based ILOs are often the most common type of outcome and describe the set of knowledge that students are expected to acquire; a2) Subject Specific Cognitive Skills ‐ These are application‐based outcomes which describe the kindsof application or transformation students are expected to make to the knowledge they acquire. These typically require students to apply knowledge or engage with it critically to, for example, evaluate, appraise, analyse, synthesise, or debate it. a3) Subject Specific Practical Skills ‐ These are skills‐based outcomes which describe the subject related skills students are expected to develop alongside knowledge acquisition. These are typically the skills that are likely to be required for employment within the subject discipline. a4)  Key Transferable Skills ‐ These are skills‐based outcomes which describe the generic and broader (non‐subject specific) skills students are expected to develop alongside knowledge acquisition. These are typically the general skills that are required for graduate employment.",
    "b) Relate the ILOs to what, as a minimum, students need to know, understand and be able to do upon completion of the Module;",
    "c) Relate the outcomes to the relevant bachelor’s in Digital Technologies Cybersecurity outcomes.",
    "d) Precede the ILOs with “On successful completion of this module, students should be able to…”;",
    "e) Follow the above with a suitable, specific and measurable action verb, according to Bloom's taxonomy  (e.g. identify; describe; explain; evaluate; plan; etc), avoiding vague or ambiguous verbs (e.g. appreciate; show awareness of).",
    "f) Write in short clear sentences and avoid putting too much or too many verbs into a single ILO",
    "g) display answer in a list such as ILO<number>",
    "h) review and optimize your answer review and optimize your answer and based on the syllabus topics, but not necessarily a 1-2-1 relation with Syllabus Teaching Topics;",
    "recall a) instructions",
    "optimize and rewrite to reduce the number of words to fit the character limit"
]

COHERENCE_ILO_SYLLABUS = [
    "build a narrative that demonstrates how a student will learn throughout the Module",
    "ILO topics must be relate with syllabus topics, building a narrative that demonstrates how they interconnect throughout the module",
    "attach to your answer a summary using only letters and numbers, like this: S<syllabus topic number> and ILO<ILO number>, display it as ILO<number> -> S<number> in a vertical bullet list",
    "optimize and rewrite to reduce the number of words to fit the character limit"
]

TMS_REQUIREMENTS = [
    "the teaching and learning methodologies must be indicated in detail and precisely, as well as the correspondence between the methodologies and the type of contact hours allocated to the course;",
    # "priority should be given to diversifying the methodologies used in each course, and this should be made clear in this section;",
    "teaching methodologies planned to facilitate student participation in scientific activities should be included in this section.",
    #"consider the total contact hours and the syllabus topics",
    #"specify the best teaching methodologies for each teaching tipology",
    "tutorial hours (TO) should be less than 5 hours",
    "specify how students can perform self-study and peer and group learning, beyond the contact hours",
    "specify digital technology applications that could be used in TMs by the lecturer",
    "refer each syllabus topics to specific learning",
    "display answer in a list like this: TM<number>: <content>",
    "review and optimize your answer",
    #"optimize and rewrite to reduce the number of words to fit the character limit"
    "adjust your answer to the character limit"
]

ASSESSMENTS_REQUIREMENTS = [
    "explain all the moments and activities included in the continuous assessment process, and the respective weight of each one in the final assessment;",
    "and linking to the previous points, each of these moments should be associated with the number of contact hours planned and their type. Examples: Group work, 10% of the final grade, 1 contact hour T; Individual presentation, 15% of the final grade, 1 contact hour TP; Written test, 60% of the final grade, 2 contact hours T;",
    "if the course cannot be assessed by a final written exam, this must be expressly stated.",
    "between the types: exams, tests, quizzes, individual, group work, debates and others, which are the most suitable for this curricular unit",
    "articulate with the teaching tipology",
    #"based on suggested ILOs, distribute weight (percentage) to each assessments; group assessments must not exceed 40%", "specifying how the lecturer should distribute assessments over the course",
    "highlight whether or not a final write exam is recommended, taking into account the practical aspects of the course",
    "summarize your answer in a bullet list",
    "optimize and rewrite to reduce the number of words to fit the character limit"
]

COHERENCE_ILO_ASS_TMS_REQUIREMENTS = [
    "a) Specify objectively and clearly how the methodologies: a1) of teaching allow the learning objectives defined for the UC to be achieved; a2) assessment methodologies make it possible to assess whether each student has achieved the objectives set for the course.",
    "b) If the course is practical, for example, the teaching methodologies presented should reflect this and this should be demonstrated in this point;",
    "c) The same applies to assessment methodologies;",
    # "build a narrative that demonstrates how the TM and assessments will ensure that the student has acquired the ILOs throughout the Module",
    # "TMs and assessments must be relate with ILO topics, building a narrative that demonstrates how they interconnect throughout the module",
    "display answer in a bullet list",
    # "attach to your answer a summary using only letters and numbers, like this: ILO<topic number> -> TM<TM number>",
    # "how assessments confirm student learning",
    "optimize and rewrite to reduce the number of words to fit the character limit"
]

BIBLIOGRAPHY_REQUIREMENTS = [
    # "display bibliography in APA style",
    # "give priority to books by Portuguese authors",
    "sort bibliographies by relevancy",
    "split bibliographies in fundamentals and complementary",
    "consider only two complementary bibliographies",
    "add at least one Portuguese book in module area if it exists",
    "indicate the topics of the syllabus that each book covers in a new line of its bibliography",
    "don't describe book content neither the author",
    "display bibliography in APA style",
    "optimize and rewrite to reduce the number of words to fit the character limit"
]

OBSERVATIONS_REQUIREMENTS =[
    "how  digital competencies are nurtured through this module?",
    "how the module can contribute, if applicable, \
        to micro-credentials provided by technology players such as\
        Microsoft, Cisco, Palo Alto and Huawei,\
        with whom the Polytechnical Institute have a partnership",
    "optimize and rewrite to reduce the number of words to fit the character limit"
]

PEDAGOGICAL_MODEL = " ".join([
    "Polytechnic Institute with a 3 years BACHELOR DEGREE,",
        "180 ECTS total in '{expertise}'.",
    "Consider the following <Module>: '{fucName}'",
    "with {contactHours} hours,",
    "and {ECTS} ECTS,",
    "and the estimated total student working hours are {workingHours},",
    "that will occur in the {fucYear} year of the bachelor degree",
    "Consider the teaching typologies: theoretical (T), theoretical-practical (TP), laboratory (LP), and tutorial(TO)."
])

#"PARA FUCs 1º NA: Mencionar Supera-te. Metodologias Ativas: Aprendizagem cooperativa. "

PROMPT_DEFAULT = {
    # "system": "You are world class technical documentation writer.\
    #     Optimize your answer like a Engenieer.\
    #     Review your text grammar with Grammarly web tool.\
    #     Display answer in bullet list whenever possible.\
    #     Avoid using line breaks in your answer.",
    "system": " ".join([
        "You are a knowledgeable and helpful person,",
            "expert university professor,",
            "who can answer any question.",
        "Optimize your answer like a Engenieer.",
        "Review your text grammar with Grammarly web tool.",
        "Display answer in bullet list whenever possible.",
        "Avoid using break line in your answer."
    ]),
    "user": "{input}",
}


CHAT_MESSAGES = {
    1.43: {
        "importantTopics": [
            ("All",
                ),
        ],

        "messageRoot": """
        Translate the [content] to PT-PT using Deepl and after review you text grammar with Flip. Preserve the content structure. Don't display your personal notes. Don't use bold or italic text.
        [content]
        {syllabus}
        """,

        "characterLimits": [1,],
    },
    1.42: {
        "importantTopics": [
            ("All",
                ),
        ],

        "messageRoot": """
        Turn [bibliography] into APA style, search in web to include the respective year & publisher if not in the [bibliography]. Don't use bold or italic text. Don't display your notes in output.
        [bibliography]
        {syllabus}
        """,

        "characterLimits": [1,],
    },
    1.41: {
        "importantTopics": [
            ("All",
                ),
        ],

        "messageRoot": """
        Fit the [syllabus] number of characters to 1000 character. Preserve the topic and subtopic structures and numbering.
        [syllabus]
        {syllabus}
        """,

        "characterLimits": [1,],
    },
    1.4: {
        "importantTopics": [
            ("All",
                ),
        ],

        "messageRoot": """
            Consider for context a European Polytechnic Institute with a 3 years BACHELOR DEGREE, 180 ECTS total in 'Digital Technologies'. Consider the following <Module>: '{fucName}' with {contactHours} hours, and {ECTS} ECTS,  and the estimated total student working hours are {workingHours} hours, that will occur in the {fucYear} year of the bachelor degree. Use web search to provide a better response.

            Your answer to this question is going to be long, so I want you to divide it up into topics such as "[<answer topic>]".

            [Syllabus]
            Develop a text about the topic 'Syllabus', reviewing the corresponding <Syllabus Topics>, making it understandable and coherent, reordering it, summarising it, and aligning it with the relation with the <Intended Learning Outcomes>, searching in Web on European Polithecnic Institutes similar references. Fit the syllabus into 1000 characters, but don't too short or it won't be understandable. Replace words and expressions in topic descriptions by acronyms known worldwide. Replace indentation by 1 white space.
            If it isn't already, Distribute into enumerable topics and subtopics, such as "1." and "1.1.".

            <Syllabus Topics>
            {syllabus}

            [Intended Learning Outcomes]
            Develop a text about the topic 'Intended learning outcomes (ILOs)', considering the following requirements:
            a) Intended Learning Outcomes (ILOs) can be: a1) Knowledge‐based ILOs are often the most common type of outcome and describe the set of knowledge that students are expected to acquire; a2) Subject Specific Cognitive Skills ‐ These are application‐based outcomes which describe the kinds of application or transformation students are expected to make to the knowledge they acquire. These typically require students to apply knowledge or engage with it critically to, for example, evaluate, appraise, analyze, synthesize, or debate it.
            a3) Subject-Specific Practical Skills ‐ These are skills‐based outcomes which describe the subject-related skills students are expected to develop alongside knowledge acquisition. These are typically the skills that are likely to be required for employment within the subject discipline. a4) Key Transferable Skills ‐ These are skills‐based outcomes which describe the generic and broader (non‐subject specific) skills students are expected to develop alongside knowledge acquisition. These are typically the general skills that are required for graduate employment. b) Relate the ILOs to what, as a minimum, students need to know, understand and be able to do upon completion of the Module; c) Relate the outcomes to the relevant bachelor's in Digital Technologies. d) Precede the ILOs with "On successful completion of this module, students should be able to…"; e) Follow the above with a suitable, specific and measurable action verb, according to Bloom's taxonomy (e.g. identify, describe, explain; evaluate; plan; etc), avoiding vague or ambiguous verbs (e.g. appreciate; show awareness of). f) Write in short, clear sentences and avoid putting too many or too many verbs into a single ILO g) Display the answer in a list such as ILO<number> h) review and optimize your answer review and optimize your answer and based on the <Syllabus Topics> but not necessarily a 1-2-1 relation with <Syllabus Topics>.

            [Evidence of the Syllabus Topics coherence with the intended learning outcomes]
            Develop a text about 'Evidence of the Syllabus Topics coherence with the intended learning outcomes', considering the following requirements: build a narrative that demonstrates how a student will learn throughout the <Module>; [Intended Learning Outcomes] topics must relate with <Syllabus Topics>, building a narrative that demonstrates how they interconnect throughout the <Module> with the [Intended Learning Outcomes (ILOs)]. Attach to your answer a summary using the notation ILO<number> -> S<number> in a vertical bullet list and based on the <Syllabus Topics> to illustrate this relation.

            [Teaching Methodologies]
            Develop a text about 'Teaching Methodologies (TMs) and specific learning of this curricular unit', consulting the following requirements: 1) total contact hours is {contactHours} hours, (distributed these hours by theoretical (T), theoretical-practical (TP), laboratory practices (LP) and tutorial (TO) tipologies) into "Contact Hours Distribution" topic in bullet list, associating TM<number> to each tipology; rule the tutorial hours (TO) should be less than 5 hours; and the following guidance: Theoretical (T): Typically involves lectures where fundamental concepts are introduced and explained; Theoretical-Practical (TP): Combines lectures with problem-solving sessions, providing a hands-on approach to applying theoretical knowledge; Laboratory Practices (LP): Involves practical sessions where students conduct experiments or apply concepts learned in theoretical classes; Tutorial (TO) / Guided Tutorial (GT): Provides individual or small group guidance, aiding in understanding complex topics, critical analysis of cases, or scientific articles. It should contain content and activities to support the achievement of learning objectives and should align with the [Assessments].
            Ensure that the [Teaching Methodologies] relate to <Syllabus Topics> reflects a learner-centred perspective, focusing on students needs and engagement. Emphasize methodologies that prepare students for professional practice since it is a polytechnical university. Specify how students can perform self-study and peer and group learning beyond the contact hours into 'Self Study' subtopic; specify wich digital technology applications that could be used by students in self study, using the brand names in parenthesis preceded by "e.g., "; relate the [Teaching Methodologies] to the [Intended Learning Outcomes] in paragraphs containing when suitable the "TM<number>: TM tipology (<ILO reference>)", don't forget it. Be coherent and not redundant. Check if the total of the hours distributed is {contactHours}, if not, redistribute the hours preserving the reasoning used. Don't quote the related ILOs.
            Fit your text into 2500 characters: review and rewrite to optimize if need.

            [Assessments]
            Develop a text about the 'Assessments' considering the following requirements: between types: exams, tests, quizzes, individual, group work, debates and others; select the ones most suitable for the <Module> and the <Syllabus Topics>; articulate your answer with the pedagogical model; based on the [Intended Learning Outcomes], distribute weight (percentage) to each Assessment type; Only to your reasoning; Group assessments must not exceed 40% of the Assessment total; Explain how the lecturer should distribute assessments over the <Module> focusing on students engagement; summarize your answer in a bullet list such as "A<number>: description (<weight>%)". Be inspired by the [Intended Learning Outcomes] and [Teaching Methodologies]. Don't quote the related ILOs.
            Your text must be less than 2500 characters: review and rewrite to optimize if need.

            [Final Write Exam]
            Determine if a final write exam is recommended or not and highlighting such as "Final Write Exam: Recommended or Not" (don't forget this instruction), considering the practical aspects of the <Module>, or if only continuous evaluation is suitable.

            [Evidence of Teaching Methodologies and assessments suggestions coherence with the ILO topics]
            Develop a text about the 'Evidence of all Teaching Methodologies and assessments coherence with the entire ILO topics', considering the following requirements: relate [Intended Learning Outcomes] to the respective [Teaching Methodologies] and [Assessments], display the answer in a summarized list, attach to your answer a summary using only letters and numbers, like that "ILO<topic numbers> -> TM<TM numbers>; A<Asessment numbers>". Based on the <Syllabus Topics>.
            Your text must be less than 2500 characters: review and optimize your answer to fit this target.

            [Bibliography]
            Develop a text about 'Suggest current and relevant bibliography for this curricular unit', considering the following requirements: display the bibliography in enumerated APA style and based on the <Syllabus Topics>, with the full referencing; sort the references by relevancy; split references into "Fundamentals" and "Complementary", and consider only two complementary bibliographies if possible. Fundamental references are that which cover all <Syllabus Topics>. Complmementary references are that which cover at least one <Syllabus Topic> already covered by any Fundamental reference. Include at least one relevant Portuguese book in <Module> area if it exists; Don't forget, display the bibliography in APA style and the author surnames in capital letters; searching in web the year and publisher of each books. Check if each book exists. A book exists if you find this book in E-commerce web site and find the respective Publisher. Don't suggest journal papers and websites.
            Your text must be less than 700 characters: review and optimize your answer to fit this target.

            [Syllabus in Bibliography]
            Show me a bullet list with which of these books in [Bibliography] each <Syllabus Topics> are found; cite book by bibliography numbering such as "B<number>" and syllabus topics by syllabus numbering such as "S<number>". If any <Syllabus Topics> is found exclusively in a complementary bibliography, then it should go to "Fundamental" category. If there aren't books in the "Complementary" category, then don't split [Bibliography] in categories.
            Your text must be less than 300 characters: review and optimize your answer to fit this target.

            [Microcedentials]
            Develop a text about the topic 'Microcredentials', considering the following requirements: The Polytechnical Institute is focusing on <Module> that can relate <Syllabus Topics> with the certifications offered by Microsoft, Cisco, and Palo Alto, which are Polytechnical Institute's partners, leveraging The Polytechnical Institute's CERTIPORT certified lab for digital exams.
            Preparing for micro-credentials can include being directly awarded module completion certificates or digital badges if students succeed in class testing, preparing for other micro-credentials that students self-learn and can later apply to exams in the Polytechnic Institute, or achieving a step into a complete credential issued by that Tech player.
            Identify which <Syllabus Topics> can relate to preparing students for microcredentials, digital badges, training paths, and other similar digital competencies that Microsoft, Cisco, and Palo Alto can recognize.
            Your text must be less than 700 characters: review and optimize your answer to fit this target.

            [Final Check Rules]
            The following rules should only be considered at the end of your reasoning, make sure to apply them:

            1. Analyse and review the [Intend Learning Outcome] set to ensure clear learning objectives outlining specific skills, knowledge, and competencies students are expected to gain;
            2. Analyze the topics and concepts covered in the <Syllabus Topics>;
            3. Compare the [Intended Learning Outcomes] with the <Syllabus Topics> to ensure that they are aligned;
            4. Make adjustments to the [Intended Learning Outcomes] to ensure alignment with the <Syllabus Topics>;
            5. Make adjustments to the <Syllabus Topics>, if necessary, to ensure a better match with the [Intended Learning Outcomes].
            6. Assess whether the <Syllabus Topics> provides the knowledge and skills needed to achieve the [Intended Learning Outcomes];
            7. Assess and review the [Teaching Methodologies] in order to guarantee that they are aligned with the [Intended Learning Outcomes];
            8. Assess if the [Teaching Methodologies] effectively align with [Assessments];
            9. Make adjustments to the [Assessment], if necessary, to ensure a better match with the [Intended Learning Outcomes];
            10. Don't display your personalized notes;
            11. Remember subdivide <Syllabus Topics> in topics and subtopics such as 1. and 1.1;
            12. Fix the text grammar with Grammarly web tool;
            13. Don't use any footnotes;
            14. Don't show [Final Check Rules] in answer.

            Order that you should be display your answer topics:
            **Curricular Unit**
                {fucName}

            **Scientific area**
                {fucArea}
            
            **Duration**
                Half-yearly
            
            **Working Hours**
                {workingHours}
            
            **Contact Hours**
                {contactHours}
            
            **ECTS**
                {ECTS} (So, how is it)
            
            **Responsible Teaching Staff**
                {fucLead} (So, how is it)
            
            **Others Teaching Staff**
                {fucAuxiliary} (So, how is it)
            
            **Intended Learning Outcomes (ILOs)**
                [Intended Learning Outcomes]
            
            **Syllabus**
                [Syllabus] (Don't add personal notes, add only the syllabus)
            
            **Evidence ILO with Syllabus**
                [Evidence of the Syllabus Topics 
            coherence with the intended learning outcomes]
            
            **Teaching Methodology (TMs)**
                [Teaching Methodologies]
            
            **Assessments (A)**
                "There are two types of assessment: Continuous or by examination." (So, how is it without the '"' delimiters, if [Final Write Exam] is Recommended. Don't forget it.)
                
                "Continuous assessment consists of:" (So, how is it without the '"' delimiters. Don't forget it.)

                [Assessments]

                "To pass the course, the average final mark must not be less than 9.5." (So, how is it without the '"' delimiters. Don't forget it.)

                Final Write Exam: [Final Write Exam].

                "The assessment by final examination accounts for 100% of the final grade and is carried out in accordance with the regulations in force." (So, how is it without the '"' delimiters, if the [Final Write Exam] is Recommended. Don't forget it.)
            
            **Evidence TMs & A with ILOs**
                [Evidence of Teaching Methodologies and assessments suggestions coherence with the ILO topics]
            
            **Bibliography**
                [Bibliography]
            
            **Syllabus in Bibliography**
                [Syllabus in Bibliography]
            
            **Observations**
                [Microcredentials]
            """.replace("  ", "").replace("<lead>", ""),#(CE["IA"]),
            #Optimize your answer characters to must than {chars} characters.

        "characterLimits": [1,],
    },
    1.3: { # NOT TESTED
        "importantTopics": [

            ("Contact hours",
                *CONTACT_HOURS_REQUIREMENTS),

            ("Intended learning outcomes (ILOs)",
                *ILO_REQUIREMENTS) +

            ("Attach to answer the evidence of the syllabus topics coherence with the (ILOs)",
                *COHERENCE_ILO_SYLLABUS),

            ("Teaching Methodologies (TMs) and specific learning of this curricular unit",
                *TMS_REQUIREMENTS) +

            ("Attach to answer the best assessments to this TMs",
                *ASSESSMENTS_REQUIREMENTS),

            ("Evidence of TM and assessments coherence with the ILOs",
                *COHERENCE_ILO_ASS_TMS_REQUIREMENTS),

            ("Suggest current and relevant books to this curricular unit",
                *BIBLIOGRAPHY_REQUIREMENTS),

            ("Observations",
                *OBSERVATIONS_REQUIREMENTS),
        ],

        "messageRoot": """
            Develop a text about the topic '{importantTopic}', considering the follow requirements: {requirements}, based on the syllabus topics:
            {syllabus}
            Fit the characters in the answer to a maximum of {chars} characters
            Calculate and show the number of characters in your displayed answer including whitespaces, punctuations and breaklines.
            Considering the pedagogical model: \n%s
            """.lstrip(" ").replace("  ", "")%PEDAGOGICAL_MODEL,
            #Optimize your answer characters to must than {chars} characters.

        "characterLimits": [1000, 2000, 6000, 3000, 1000, 1000],
    },
    1.2: {
        "importantTopics": [

            ("Contact hours",
                "divide the idealized contact hours into teaching typologies that cover the whole curricular unit",
                "tutorial hours (TO) should be less than 5 hours",
                "optimize your answer and display it on table",
                "specify the number of hours spent teaching in each typology and display it on table",
                "Not showing the hours spent by topic"
                # "estimate the number of hours of each tipology to each syllabus topics",
                # "optimize your answer and display it on table, shorten the syllabus topics description"
                ),

            ("Syllabus (Compacted)",
                "shorten the syllabus to fit the character limit",
                "preserve the syllabus numbering",
                "show in numeric list",
                "don't show the character count neither the pedagogical model"),

            ("Intended learning outcomes (ILOs)",
                *ILO_REQUIREMENTS,
                "optimize and rewrite to reduce the number of words to fit the character limit",
                ) +
            ("After your answer, evidence of the Syllabus Topics coherence with the Module's (ILOs)",
                "build a narrative that demonstrates how a student will learn throughout the Module",
                "ILO topics must be relate with syllabus topics, building a narrative that demonstrates how they interconnect throughout the module",
                "attach to your answer a summary using only letters and numbers, like this: S<syllabus topic number> and ILO<ILO number>, display it as ILO<number> -> S<number> in a vertical bullet list",
                "optimize and rewrite to reduce the number of words to fit the character limit"),

            ("Teaching Methodologies (TMs) and specific learning of this curricular unit",
                *TMS_REQUIREMENTS,
                "consider the total contact hours and the syllabus topics",
                "specify the best teaching methodologies for each teaching tipology",
                "tutorial hours (TO) should be less than 5 hours",
                "specify how students can perform self-study and peer and group learning, beyond the contact hours",
                "specify digital technology applications that could be used in TMs by the lecturer",
                "refer each syllabus topics to specific learning",
                "display answer in a list like this: TM<number>: <content>",
                "review and optimize your answer",
                "optimize and rewrite to reduce the number of words to fit the character limit") +
            ("Attach to answer the best assessments to this TMs",
                *ASSESSMENTS_REQUIREMENTS,
                "between the types: exams, tests, quizzes, individual, group work, debates and others, which are the most suitable for this curricular unit",
                "articulate with the teaching tipology", "based on suggested ILOs, distribute weight (percentage) to each assessments; group assessments must not exceed 40%", "specifying how the lecturer should distribute assessments over the course",
                "highlight whether or not a final exam is recommended, taking into account the practical aspects of the course",
                "summarize your answer in a bullet list",
                "optimize and rewrite to reduce the number of words to fit the character limit"),

            ("Evidence of TM and assessments coherence with the ILOs",
                *COHERENCE_ILO_ASS_TMS_REQUIREMENTS,
                "build a narrative that demonstrates how the TM and assessments will ensure that the student has acquired the ILOs throughout the Module",
                "TMs and assessments must be relate with ILO topics, building a narrative that demonstrates how they interconnect throughout the module",
                # "relate each ILO to the respective TM, and vice-versa",
                # "how assessments confirm student learning",
                "display answer in a bullet list",
                # "attach to your answer a summary using only letters and numbers, like this: ILO<topic number> -> TM<TM number>",
                "optimize and rewrite to reduce the number of words to fit the character limit"),

            ("Suggest current and relevant books to this curricular unit",
                # "display bibliography in APA style",
                # "give priority to books by Portuguese authors",
                "sort these bibliographies by relevancy",
                "split bibliographies in fundamentals and complementary",
                "consider only two complementary bibliographies",
                "add at least one Portuguese book in module area if it exists",
                "indicate the topics of the syllabus that each book covers in a new line of its bibliography",
                "don't describe book content neither the author",
                "display bibliography in APA style",
                "optimize and rewrite to reduce the number of words to fit the character limit"
                ),

            ("Observations",
                # "how can we integrate applied psychology in this curricular unit, and where is it in the syllabus?",
                "how  digital competencies are nurtured through this module?",
                "how the module can contribute, if applicable, to micro-credentials provided by technology players such as Microsoft, Cisco, Palo Alto and Huawei, with whom the Polytechnical Institute have a partnership",
                "optimize and rewrite to reduce the number of words to fit the character limit"),

        ],

        "messageRoot": """
            Develop a text about the topic '{importantTopic}', considering the follow requirements: {requirements}, based on the syllabus topics:
            {syllabus}
            Fit the characters in the answer to a maximum of {chars} characters
            Calculate and show the number of characters in your displayed answer including whitespaces, punctuations and breaklines.
            Considering the pedagogical model: \n%s
            """.lstrip(" ").replace("  ", "")%PEDAGOGICAL_MODEL,
            #Optimize your answer characters to must than {chars} characters.

        "characterLimits": [1000, 1000, 1000, 1000, 3000, 3000, 3000, 1000, 1000],
    },
    1.1: {
        "importantTopics": [
            # ("Syllabus",
            #     "If able, provide optimization of the the syllabus program",
            #     "in numeric list"),

            ("Contact hours",
                "divide the contact hours into teaching typologies",
                "tutorial hours (TO) should be less than 5 hours",
                "specify the number of hours spent teaching in each typology and display it on table",
                "estimate the number of hours of each tipology to each syllabus topics",
                "optimize your answer and display it on table, shorten the syllabus topics description"),

            ("Intended learning outcomes (ILOs)",
                "use the Bloom's taxonomy to develop your answer without quoting it directly", "display answer in a list such as ILO<number>:", "don't quote syllabus topic", "don't quote verbs", "relate when possible, ILO with more than one syllabus topic", "try to join the topics of the same category", "review and optimize your answer"),

            ("Evidence of the each syllabus topics and subtopics coherence with the ILOs topics",
                "think hard and relate each ILOs topics to one or multiple syllabus topics and each syllabus topic to one or multiple ILO topics", "use verbs such as connect, relate, correspond and link; be brief and coherent", "don't quote syllabus topics description", "review and optimize your answer citing only respective topics numbers", "attach to your answer a summary using only letters and numbers like this: S<topic number> and ILO<ILO number>", "display it as ILO<number> -> S<number> in a vertical bullet list"),

            ("Teaching Methodologies (TMs) and specific learning of this curricular unit",
                "consider the total contact hours and the syllabus", "specify the best TM for each teaching tipology", "tutorial hours (TO) should be less than 5 hours", "specify how students can perform self-study and peer and group learning, beyond the contact hours", "cite some digital technology applications that could be used in TMs by the lecturer", "refer syllabus topics to specific learning", "display answer in a list like this: TM<number>: <content>", "review and optimize your answer"),

            ("Assessments",
                "between the types: exams, tests, quizzes, individual, group work, debates and others, which are the most suitable for this curricular unit",
                "articulate with the teaching tipology", "based on suggested ILOs, distribute weight (percentage) to each assessments; group assessments must not exceed 40%", "specifying how the lecturer should distribute assessments over the course", "tell me if final exam is recommended or not, considering the practical aspects of the course", "summarize your answer in a bullet list"),

            ("Evidence of TM and assessments coherence with the ILO topics suggestion",
                "relate each ILO to the respective TM, and vice-versa", "how assessments confirm student learning", "display answer in a bullet list, attach to your answer a summary using only letters and numbers, like this: ILO<topic number> -> TM<TM number>"),

            ("Suggest current and relevant books to this curricular unit",
                # "display bibliography in APA style",
                # "give priority to books by Portuguese authors",
                "sort these bibliographies by relevancy", "split bibliographies in fundamentals and complementary", "consider two complementary bibliographies", "indicate which syllabus topics each book cover in a new line his biography", "don't describe book content neither the author", "display bibliography in APA style"),

            ("Observations",
                "how can we integrate applied psychology in this curricular unit, and where is it in the syllabus?",
                "how  digital competencies are nurtured through the course?",
                "how the course can contribute, if applicable, to micro-credentials provided by technology players such as Microsoft, Cisco, Palo Alto and Huawei, with whom the Polytechnical Institute have a partnership"),

        ],

        "messageRoot": """
            Develop a text about the topic '{importantTopic}', considering the follow requirements: {requirements}, based on the syllabus:
            {syllabus}
            Optimize your answer to must than {chars} characters.
            Considering the pedagogical model: \n%s
            """.lstrip(" ").replace("  ", "")%PEDAGOGICAL_MODEL,

        "characterLimits": [1000, 1000, 1000, 3000, 3000, 3000, 1000, 1000],
    },
    1.0: {# ILO and Evidence OK, but Teaching Methodologies nope
        "importantTopics": [
            # ("Syllabus",
            #     "provide optimization of the the syllabus program",
            #     "in a bullet list",
            #     "If able, to "),

            ("Contact hours",
                "divide the contact hours into the following teaching typologies:\
                theoretical (T), theoretical-practical (TP), laboratory (LP), and tutorial(TO).",
                "specify number of hours to teaching typologies and display it on table",
                # "estimate the number of hours of each tipologies to each syllabus topics",
                # "optimize your answer and display it on table (shorten the syllabus topics description)"
                ),

            ("Intended learning outcomes (ILOs)",
                "use the Bloom's taxonomy to develop your answer in a hidden way",
                "display answer in a list such as ILO<number>: ",
                "don't quote syllabus topic",
                "don't quote verbs",
                #"be brief",
                "review and optimize your answer",
                "join the topics of the same category",
                "review and optimize your answer"),

            ("Evidence of the each syllabus topics and subtopics coherence with the ILOs topics",
                "think hard and relate each ILOs topics to, one or multiple, syllabus topics and each syllabus topics to, one or multiple, ILOs topics",
                "use verbs such as connect, relate, correspond and link",
                "be brief and coherent in your words",
                "don't quote syllabus topics description",
                #"show answer in a bullet list",
                "review and optimize your answer citing only respective topics numbers",
                #"cover necessarily all ILOs",
                #"display answer in summarized bullet list",
                "attach to your answer a summary using only letters and numbers",
                "like that S<topic number> and ILO<ILO number>",
                "display it as ILO<number> -> S<number> in a vertical bullet list"),

            ("Teaching Methodologies (TMs) and specific learning of this curricular unit",
                "include TMs for the tipologies: theoretical (T), theoretical-practical (TP), laboratory (LP) and tutorial(TO) to contact lecturer and student and specify how to",
                #"specify how for autonomous student time to study and ",
                "specify how students can study independently, complementing lessons with the teacher",
                "cite digital technology applications that could be used in TMs by lecturer",
                "associate syllabus topics to your specifc learning",
                "display answer in a list such as TM<number>: <content>",
                "review and optimize your answer"),

            ("Assessments",
                "Between types: exams, tests, quizzes, individual, group work, debates and others, which are the most suitable for this curricular unit",
                "Articulate your answer with the pedagogical model",
                "Based on syllabus",
                "Distribute percents to each assessment",
                "Group assessments must not exceed 40% of the assessment total",
                "Specifying how to lecturer distribute assessments over the course",
                "Tell me if final exam is recommended or not",
                "Summarize your answer in a bullet list"),

            ("Evidence of TM and assessments suggestions coherence with the ILO topics suggestion",
                "relate each ILOs to respective TM and assessment",
                #"optimize your answer quoting ILOs numbers",
                "display answer in a summarized bullet list",
                "attach to your answer a summary using only letters and numbers",
                "like that ILO<topic number> and TM<TM number>",
                #"display it as ILO<number> -> S<number> in a vertical bullet list",
                ),

            ("Suggest current and relevant books to this curricular unit",
                "display bibliography in APA style",
                "sort this bibliographies by relevancy",
                "split bibliographies in fundamentals and complementary",
                "Consider until two complementary bibliographies",
                "After your bibliography suggestion, show me a bullet list with which of these books the each syllabus topics are found, quoting only the author book surname in parenthesis.",
                "Don't forget: display bibliography in APA style",),

            # ("Observations",
            #     # "Summary of key Concepts/topics of the course; reference to ECTS,  Pedagogical Model, the aim to equip students with the ability to achieve to ILOs.",
            #     # "highlight the practical applications that contribute to the development of desired skills or outcomes.",
            #     # "highlight the course emphasises and the use of pegagogial model, including tools and methods, to foster students for challenges in the field of work of the Bachelor Degree.",
            #     # "quote the ultimate goal for students"
            #     "Tell if have some curricular unit as pre-requisite"),

            # ("Suggestions",
            #     "How we can integrate applied psychology in this curricular unit and where in the syllabus?"),
        ],
        "messageRoot": """
            Develop a text about the topic '{importantTopic}', considering the follow requirements: {requirements}, based on the syllabus:
            {syllabus}
            Your text must be less than {chars} characters.
            Considering the pedagogical model: \n%s
            """.lstrip(" ")%PEDAGOGICAL_MODEL
            #After optimize and summarize your text.
        ,

        "characterLimits": [1000, 1000, 1000, 3000, 3000, 3000, 1000, 1000],
    },
    0.9: {# ILO and Evidence OK, but Teaching Methodologies nope
        "importantTopics": [
            ("Intended learning outcomes (ILOs)",
                "using the Bloom's taxonomy verbs",
                "in a numeric list",
                "do not quote syllabus topic",
                "do not explain it"),

            # ("Evidence of the each syllabus topic coherence with the previous ILOs",
            #     "linking each ILOs topics to respective syllabus topic numbers",
            #     "optimize your answer quoting syllabus by numbers",
            #     "in a summarized bullet list"),

            # ("Optimized Teaching Methodologies (TMs) and specific learning of the curricular unit",
            #     "articulated with the pedagogical model teorethical and pratical",
            #     "including autonomous student time to study",
            #     "quote digital technology applications to integrate to TMs",
            #     "quote previous syllabus topics"),

            # ("Suggest assessments to ensure that students are learning what they know",
            #     "articulated with the pedagogical model teorethical and pratical"),

            # ("Evidence of the each syllabus topic coherence with the previous ILOs",
            #     "linking each ILOs topics to respective syllabus topic numbers",
            #     "optimize your answer quoting syllabus by numbers",
            #     "in a summarized bullet list"),

            # ("Suggest current and relevant books to this curricular unit",
            #     "show this bibliograthies in APA style",
            #     "sort descending this bibliographies by year"),
        ],
        "messageRoot": """
            Develop a text about the topic '{importantTopic}', considering the follow requirements: {requirements} and based on the syllabus:
            {syllabus}
            Your text must be less than {chars} characters.
            Review your text grammar with Grammarly web tool.
            """.lstrip(" ")
            #After optimize and summarize your text.
        ,
        "characterLimits": [1000, 1000, 3000, 1000, 1000, 1000],
    },
}

import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from os.path import basename

from pyidebug import debug
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import deepl

try:
    from .pyle import createFolder
except Exception:
    from pyle import createFolder

class Verbose:
    __endPrint = "..."
    __endMessage = "Done"

    def __init__(self: object, enable: bool):
        self._enable = enable
        return None

    def beginProcess(self: object, msg: str) -> (None):
        if self._enable:
            print(msg, end=self.__endPrint)
        return None

    def endProcess(self: object) -> (None):
        if self._enable:
            print(self.__endMessage)
        return None


class UserInterface(Verbose):
    
    def __init__(
            self: object,
            version: int,
            syllabus: str,
            fucName: str,
            contactHours: int,
            workingHours: int,
            ECTS: int,
            expertise: str,
            fucNameEN: str,
            fucYear: str,
            fucArea: str,
            fucLead: str,
            fucAuxiliary: str,
            *,
            message: str = None,
            prompt: dict[str:str] = PROMPT_DEFAULT,
            apiKey: str = None,
            verbose: bool = True,
            translateTo: str = None,
            animated: bool = False,
            questions: dict[str:str] = None, # Edit Important Topics manually
            showQuestions: bool = False,
            offline: bool = False,
            compactMode: bool = False,
            gptModel: str = "gpt-4"
            ) -> (None):

        super(UserInterface, self).__init__(verbose)

        self._importantTopics = [
            topic[0] for topic in CHAT_MESSAGES.get(version, {}).get("importantTopics", [])
        ]
        self._syllabus = syllabus
        self._version = version
        self._message = message
        self._questions = questions
        self._fucNamePT = fucName
        self._contactHours = contactHours
        self._workingHours = workingHours
        self._ECTS = ECTS
        self._expertise = expertise
        #self._fucName = translator(self._fucNamePT, to="EN-GB")
        self._fucName = fucNameEN
        self._fucYear = fucYear
        self._fucArea = fucArea
        self._fucLead = fucLead
        self._fucAuxiliary = fucAuxiliary
        self._offline = offline

        #self._syllabusPT = translator(syllabus, to="PT-PT")
        self.__filePath = None
        self._ilo = None
        self._json = {}
        self._jsonPT = {}
        self._tagMap = {
            "Syllabus": "syllabus",
            "Contact Hours": "contactHours",
            "Assessments": "assessment",
            "Intended Learning Outcomes (Ilos)": "learningOutcome",
            "Evidence Of The Each Syllabus Topics And Subtopics Coherence With The Ilos Topics": "coherenceOutcomes",
            "Teaching Methodologies (Tms) And Specific Learning Of This Curricular Unit": "methodology",
            "Evidence Of Tm And Assessments Suggestions Coherence With The Ilo Topics Suggestion": "coherenceAssessment",
            "Suggest Current And Relevant Books To This Curricular Unit": "bibliography",
        }
        self._tagMapPT = {
            "Syllabus": "conteudoProgramatico",
            "Contact Hours": "contactHours",
            "Assessments": "avaliacao",
            "Intended Learning Outcomes (Ilos)": "objetivoAprendizagem",
            "Evidence Of The Each Syllabus Topics And Subtopics Coherence With The Ilos Topics": "coerenciaObjetivos",
            "Teaching Methodologies (Tms) And Specific Learning Of This Curricular Unit": "metodologia",
            "Evidence Of The Your Tm And Assessments Suggestions Coherence With You Ilo Topics Suggestion": "coerenciaAvaliacao",
            "Suggest Current And Relevant Books To This Curricular Unit": "bibliography"
        }

        self.beginProcess("Formatting the chat messages")
        self.__generateChatMessage(version, message, verbose, compactMode)
        self.endProcess() if verbose else None

        if apiKey is None:
            raise ValueError("You need an Openai api key!")

        self.beginProcess("Connecting to chat gpt")
        self.__openChat(
            apiKey,
            prompt,
            gptModel
            )
        self.endProcess()

        self._answers = {}
        self._translations = {}
        self._file = None

        if showQuestions:
            print(40*"=",*self._chatMessage, sep="\n", end="\n"+40*"="+"\n")

        self.ask(animated=animated)

        if translateTo is not None:
            self.__translateAnswers(language=translateTo)

        return None

    def __translateAnswers(
            self: object,
            language: str = "PT-PT",
            tool: str = "DeepL",
            grammar: str = "LanguageTool"
            ) -> (list[str]):

        translations = []
        for i, (tag, answer) in enumerate(self._answers.items()):
            translation = self.__ask(
                f"Translate follow text, using a web translator {tool}, to {language} and check your text grammar using the web tool {grammar}: \n\n{answer}",
                suffix=f"(Translations of the '{self._importantTopics[i]}')"
            )
            translations[tag+"_translate"] = translation

        self._translations = translations

        return translations

    def __translateAnswersToPT(
            self: object,
            tool: str = "DeepL",
            grammar: str = "Flip"
            ) -> (list[str]):

        translations = {}
        try:
            for i, (tag, answer) in enumerate(self._answers.items()):
                translation = self.__ask(
                    f"Translate follow text, using a web translator {tool}, to PT-PT and check your text grammar using the Flip: \n\n{answer}\nDon't translate bibliography content. \nTranslate 'Intended Learning Outcomes (ILOs)' to 'Objetivos de Parendizagem (OAs)'. Review the [Syllabus] translation and rewrite it to fit into 1000 characters, use portuguese acronyms and synonyms if need in this task.",
                    suffix=f"(Translations of the '{self._importantTopics[i]}')"
                )
                translations[tag] = translation

        except KeyboardInterrupt:
            pass

        self._translations = translations

        return translations

    def __generateChatMessage(
            self: object,
            version: int,
            message: str = None,
            verbose: bool = False,
            compactMode: bool = False,
        ):

        if self._questions is None and message is None:
            _message = CHAT_MESSAGES.get(version)
        elif self._questions is not None:
            _message = self._questions
        else:
            _message = message

        if _message is not None and not compactMode:
            _chatMessage = ChatMessage(
                self._syllabus, **_message,
                ECTS=self._ECTS, contactHours=self._contactHours,
                workingHours=self._workingHours, expertise=self._expertise,
                fucName=self._fucName, fucYear=self._fucYear,
                fucArea=self._fucArea, fucLead=self._fucLead,
                fucAuxiliary=self._fucAuxiliary,
                verbose=verbose
                ) if type(_message) is dict\
                  else ChatMessage(None, _message, verbose=verbose)
            self._chatMessage = _chatMessage.getChatMessage()
        # elif _message is not None:
        #     self._chatMessage = [
        #         MESSAGE_1.format(
        #             fucName=self._fucName,
        #             syllabus=self._syllabus,
        #             contactHours=self._contactHours,
        #             workingHours=self._workingHours,
        #             ECTS=self._ECTS,
        #             ),
        #         MESSAGE_2,
        #         MESSAGE_3
        #     ]
        else:
            self._chatMessage = None
            raise ValueError(f"Version '{version}' not found. Available versions {list(d.keys())}")

        return None

    def __openChat(
            self: object,
            apiKey: str,
            prompt: dict[str:str],
            gptModel: str
            ) -> (None):

        self._chat = Chat(apiKey, prompt, gptModel, self._enable)

        return None

    @property
    def syllabus(self: object):
        return self._syllabus

    @property
    def answers(self: object):
        return self._answers

    @property
    def translations(self: object):
        return self._translations

    @property
    def prompt(self: object):
        return self._prompt

    def getSyllabus(self: object):
        return self._syllabus

    def getAnswers(self: object):
        return self._answers

    def getTranslations(self: object):
        return self._translations

    def getPrompt(self: object):
        return self._prompt

    def setPrompt(self: object, prompt: dict[str:str]):
        self._chat.setPrompt(prompt)
        return None

    def __ask(self: object, msg: str, suffix: str = "") -> (str):
        answer = self._chat.invoke(msg, suffix).content
        return answer

    def showAnswers(self: object, animated: bool = False) -> (None):
        print(
            *[f"{k}:\n{v}" for k, v in self._answers.items()],
            sep="\n\n"
        )
        return None

    def showTranslations(self: object, animated: bool = False) -> (None):
        print(
            *[f"{k}:\n{v}" for k, v in self._translations.items()],
            sep="\n\n"
        )
        return None

    def ask(
            self: object,
            showAnswer: bool = False,
            animated: bool = False
            ) -> (list[str]):

        answers = {}
        total = len(self._chatMessage)
        try:
            for i, message in enumerate(self._chatMessage):
                message.format(ilo=self._ilo)
                topic = self._importantTopics[i]
                if not self._offline:
                    answer = self.__ask(message, suffix=f"{i+1}/{total} ({self._importantTopics[i]})")
                    if "ILO" in topic:
                        self._ilo = answer
                else:
                    answer = "Teste"

                answers[topic] = answer
        except KeyboardInterrupt:
            pass

        except Exception as err:
            print(
                "\n",
                "============",
                "OpenAi Error",
                "============",
                f'''   Type: "{err.body['type']}"''',
                f'''Message: "{err.body['message']}"''',
                sep="\n",
                end="\n\n"
            )
            input("Run script again")

        if showAnswer and animated:
            botprint(*answers.values(), sep="\n")
        elif showAnswer:
            self.showAnswers(animated)

        self._answers = answers

        return answers

    def __fileExist(self: object, filePath: str) -> (str):
        filepath, extension = os.path.splitext(filePath)
        filename = os.path.basename(filepath)
        path = filepath[:-len(filename)-1]
        extension = extension[1:]

        candidate = filename

        candidatePath = f"{path}/{candidate}.{extension}"

        # fileAmount = filePath.split("_")
        # fileAmount = int(fileAmount)\
        #     if fileAmount.isdigit()\
        #     else None
        amount = 1
        while os.path.exists(candidatePath):
            if f"_{amount-1}" in candidate:
                candidate = candidate.replace(
                    f"_{amount-1}",
                    f"_{amount}"
                    )
            else:
                candidate = f"{candidate}_{amount}"
            candidatePath = f"{path}/{candidate}.{extension}"
            amount += 1
        return candidatePath

    def __exportTxt(
            self: object,
            text: str,
            filename: str,
            path: str = ".",
            dontClose: bool = False
            ) -> (str):
        # Create the path folder
        createFolder(f"{path.strip('/')}/")

        # Turn to lower case
        filename = filename#.lower()

        # Remove the filename accents and white spaces
        filename = removeAccents(filename)
        filename = removeWhitespaces(filename)

        if self._file is None or filename not in self._file.name:
            filePath = f"{path.strip('/')}/{filename}.txt"

            if filename != "questions":
                filePath = self.__fileExist(filePath)

                self._file = open(filePath, "x", encoding="utf-8")
            else:
                self._file = open(filePath, "w", encoding="utf-8")

            self.__filePath = filePath

        self._file.write(text)
        self._file.flush()

        if not dontClose:
            self._file.close()

        return self.__filePath

    def __exportJson(
            self: object,
            text: str,
            filename: str,
            path: str = ".",
            dontClose: bool = False,
            tag: str = None
            ) -> (str):

        # Add tag to json dict
        self._json[tag] = text

        if not dontClose:
            # Create the path folder
            createFolder(f"{path.strip('/')}/")

            # Turn to lower case
            filename = filename.lower()

            # Remove the filename accents and white spaces
            filename = removeAccents(filename)
            filename = removeWhitespaces(filename)

            # Set the output file path
            filePath = f"{path.strip('/')}/{filename}.json"

            # Verify if file exists and rename it
            self.__filePath = filePath = self.__fileExist(filePath)

            debug(globals(), locals())

            import json

            with open(filePath, "x", encoding='latin-1') as file:
                json.dump(self._json, file, indent=2)

        return self.__filePath

    def __export(
            self: object,
            text: str,
            filename: str,
            extension: str = "txt",
            path: str = ".",
            dontClose: bool = False,
            tag: str = None
            ) -> (str):

        if extension == "txt":
            filePath = self.__exportTxt(
                text, filename, path, dontClose
                )

        elif extension == "json":
            filePath = self.__exportJson(
                text, filename, path, dontClose, tag
                )

        return locals().get("filePath", None)

    def __exportParam(
            self: object,
            param: str,
            filename: str,
            extension: str = "txt",
            path: str = "./",
            ) -> (str):

        if param == "translations" and not any(self._translations):
            # Translate to portuguese
            self.__translateAnswersToPT()

        tagMap = self._tagMapPT\
            if param == "translations"\
            else self._tagMap

        _param = {
            "questions": self._chatMessage.copy(),
            "answers": self._answers.copy(),
            "translations": self._translations.copy(),
            "answers & translations": self._answers | self._translations
        }[param]

        total = len(_param)

        filePath = None # Set default value

        if param == "questions":
            content = "\n".join(_param)
            filePath = self.__export(
                content,
                filename,
                extension,
                path,
                dontClose=False
            )
        else:
            for tag in ["Contact hours", "Observations"]:
                if tag not in _param:
                    continue
                content = _param.pop(tag)
                _del = len(tag)*"="
                title = "\n{}\n{}\n{}\n".format(
                    _del, tag.title(), _del
                    ) if "Compacted" not in tag.title()\
                            and "All" not in tag.title else ""
                if extension == "txt":
                    filePath = self.__export(
                        title + content,
                        filename,
                        extension,
                        path,
                        dontClose=True
                    )
                elif extension == "json":
                    filePath = self.__export(
                        content,
                        filename,
                        extension,
                        path,
                        dontClose=True,
                        tag=tagMap[tag.title()]
                    )
                total -= 1

            for i, (tag, content) in enumerate(_param.items()):
                _del = len(tag)*"="
                title = "\n{}\n{}\n{}\n".format(
                    _del, tag.title(), _del
                    ) if "Compacted" not in tag.title()\
                            and "All" not in tag.title() else ""
                if extension == "txt":
                    filePath = self.__export(
                        title + content,
                        filename,
                        extension,
                        path,
                        dontClose=i<(total-1)
                            # if "Intended Learning Outcomes (Ilos)" not in title
                            # else True
                    )
                elif extension == "json":
                    filePath = self.__export(
                        content,
                        filename,
                        extension,
                        path,
                        dontClose=True,
                        tag=tagMap[tag.title()]
                    )

        return filePath

    def __exportContent(self: object) -> (None):
        for k, v in self._answers:
            pass
        return None

    def exportAnswers(
            self: object,
            filename: str,
            extension: str = "txt",
            path: str = "./",
            tag: str = None
            ) -> (str):

        filePath = self.__exportParam(
            "answers", filename, extension, path
        )

        return filePath

    def exportQuestions(
            self: object,
            filename: str,
            extension: str = "txt",
            path: str = "./"
            ) -> (str):

        filePath = self.__exportParam(
            "questions", filename, extension, path
        )

        return filePath

    def exportTranslations(
            self: object,
            filename: str,
            extension: str = "txt",
            path: str = "./"
            ) -> (str):

        filePath = self.__exportParam(
            "translations", filename, extension, path
        )

        return filePath

    def exportAnswersTranslations(
            self:object,
            filename: str,
            extension: str = "txt",
            path: str = "./"
            ) -> (str):

        filePath = self.__exportParam(
            "answers & translations", filename, extension, path
            )

        return filePath


    def __startServer(self: object, email: str) -> (None):
        import getpass
        self.__server = server = smtplib.SMTP(
            #host='smtp.outlook.com', port=587
            host="smtp.office365.com", port=587
            #host='smtp.gmail.com', port=587
            )
        server.starttls()
        while True:
            try:
                server.login(
                    email,
                    getpass.getpass(f"\n\nOUTLOOK ACCESS\nlogin: {email}\npassword: ")
                )
            except smtplib.SMTPAuthenticationError as err:
                print(err)
            else:
                break
        return None

    def sendByEmail(
            self: object,
            *filename: str,
            send_from: str = "natanael.quintino@ipiaget.pt",
            send_to: str = "natanael.quintino@ipiaget.pt"
            ) -> (None):
        self.__startServer(send_from)
        subject = f'''FUC "{', '.join(filename)}" finished'''
        bodyMessage = f'''Caro(a), A(s) FUC(s) "{', '.join(filename)}" foi(ram) concluida(s). Meus cordiais cumprimentos, Pyaget FUC Generator'''
        send_mail(
            send_from,
            send_to,
            subject,
            bodyMessage,
            filename,
            self.__server
            )

        return None


class Chat(Verbose):

    __defaultApiKey = None

    def __init__(
            self: object,
            apiKey: str = None,
            prompt: dict[str: str] = PROMPT_DEFAULT,
            gptModel: str = "gpt-3.5-turbo",
            verbose: bool = False
            ) -> (None):

        super(Chat, self).__init__(verbose)

        self.__apiKey = apiKey\
            if apiKey is not None\
            else self.__defaultApiKey

        try:
            self._chat = ChatOpenAI(
                model=gptModel,
                openai_api_key=self.__apiKey
            )
        except Exception:
            self._chat = ChatOpenAI(
                openai_api_key=self.__apiKey
            )
        if prompt is not None:
            self.__generatePrompt(prompt)

        return None

    def __generatePrompt(
            self: object,
            prompt: dict[str:str]
            ) -> (None):

        self._prompt = ChatPromptTemplate.from_messages(
            prompt.items() if prompt is not None
                           else ("user", "{input}")
        )

        # Chainning prompt to char
        self._chain = self._prompt | self._chat

        return None

    def setPrompt(
            self: object,
            prompt: dict[str:str]
            ) -> (None):
        self.__generatePrompt(prompt)
        return None

    def invoke(
            self: object,
            userMessage: str,
            suffix: str = ""
            ) -> (str):

        self.beginProcess(f"Asking to ChatGPT {suffix}")
        answer = self._chain.invoke(
            {"input": userMessage},
        )
        self.endProcess()

        return answer


class ChatMessage(Verbose):

    def __init__(
            self: object,
            syllabus: str,
            messageRoot: str,
            importantTopics: list[str] = None,
            characterLimits: list[int] = None,
            contactHours: int = None,
            workingHours: int = None,
            ECTS: int = None,
            expertise: str = None,
            fucName: str = None,
            fucYear: str = None,
            fucArea: str = None,
            fucLead: str = None,
            fucAuxiliary: str = None,
            verbose: bool = False
            ) -> (None):
        self._messageRoot = messageRoot
        self._syllabus = syllabus
        self._importantTopics = importantTopics
        self._characterLimits = characterLimits
        self._contactHours = contactHours
        self._workingHours = workingHours
        self._ECTS = ECTS
        self._expertise = expertise
        self._fucName = fucName
        self._fucYear = fucYear
        self._fucArea = fucArea
        self._fucLead = fucLead
        self._fucAuxiliary = fucAuxiliary

        super(ChatMessage, self).__init__(verbose)

        if importantTopics is not None and characterLimits is not None:
            self.__formatMessage()
        else:
            self._chatMessage = self._messageRoot

        return None

    def __formatMessage(
            self: object,
            ) -> (None):

        if self._syllabus is None:
            self._chatMessage = None
            return None

        self._chatMessage = []
        for i, topic in enumerate(self._importantTopics):
            message = self._messageRoot.format(
                importantTopic=topic[0],
                requirements=', '.join(topic[1:]),
                chars=int(self._characterLimits[i]*0.6),
                syllabus=self._syllabus,
                contactHours=self._contactHours,
                workingHours=self._workingHours,
                ECTS=self._ECTS,
                expertise=self._expertise,
                fucName=self._fucName,
                fucYear=self._fucYear,
                fucArea=self._fucArea,
                fucLead="{} ({} hours)".format(*self._fucLead)
                    if self._fucLead is not None else "n.a.",
                fucAuxiliary="{} ({} hours)".format(*self._fucAuxiliary)
                    if self._fucAuxiliary is not None else "n.a.",
            ).strip("\t ")

            if len(topic) == 1:
                message.replace(
                    ", considering the follow requirements: and",
                    ""
                )

            self._chatMessage.append(message)

        return None

    @property
    def chatMessage(self: object):
        return self._chatMessage

    def getChatMessage(self: object):
        return self._chatMessage


import sys
import time
def botprint(
        *text: str,
        sep: str = "",
        end: str = "\n",
        delay_time: float = .01
        ) -> (None):
    for _text in text:
        for character in _text:
            sys.stdout.write(character)
            sys.stdout.flush()
            #print(character, end="")
            if character not in "\n\t ":
                time.sleep(delay_time)
    return None


def send_mail(send_from, send_to, subject, text, files=None,
              server="127.0.0.1"):

    if type(send_to) is not list:
        send_to = [send_to]

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    print ('Sending email to outlook', end="...")
    server.sendmail(send_from, send_to, subject, text)
    # smtp = smtplib.SMTP(server)
    # smtp.sendmail(send_from, send_to, msg.as_string())
    print("Done")
    server.quit()
    #smtp.close()
    return None


def removeAccents(text: str) -> (str):
    accentsMap = zip("áéíóúàèìòùäëïöüãẽĩõũâêîôûçñ", 5*"aeiou"+"cñ")
    withoutAccents = text
    for old, new in accentsMap:
        if old not in text:
            continue
        withoutAccents = withoutAccents.replace(old, new)
    return withoutAccents


def removeWhitespaces(text: str) -> (str):
    return text.replace(" ","_")


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


# [Suggestions]
# Develop a text about the topic 'Suggestions', subdivide in "Interdisciplinarity" and "Digital Competencies", considering the following requirements: 1) How can we integrate strong interdisciplinarity with Polytechnic University's additional areas of knowledge and research, such as AI, Digital Marketing, Digital Technologies Applied Psychology in this <Module>, if suitable. 2) How digital competencies are nurtured through the course, considering the European Commission, particularly All Digital and DIGComp.