import json

from base_watsonx.wxai import WXAIProcessor
from base_watsonx.discovery import WDProcessor


class AndromedaNews():
    def __init__(self):
        self._wx_instance = WXAIProcessor()
        self._wd_instance = WDProcessor()
        self._model_id = 'mistralai/mixtral-8x7b-instruct-v01'

    @property
    def model_id(self):
        return self._model_id

    @model_id.setter
    def model_id(self, value):
        avail_ids = self.wx_instance.get_model_names()
        if not isinstance(value, str) or not value:
            raise ValueError("Invalid model ID: must be a non-empty string.")
        if value not in avail_ids:
            raise ValueError("Invalid model ID: Model not supported")
        self._model_id = value
        print(f"Model ID set to: {self._model_id}")


    #  Along with the most key information, entities and events.
    def get_summary(self, article):
        title = article.get("title")
        prompt = '''You are tasked to read through the below news article and provide the summary of it. Make sure you retain the key information, entities and events while summarizing it. Now go through the below news article and summarize it:

        news article:
        %s
        
        Summary:
        '''%(article.get("text")[0].strip())

        model = self._wx_instance.get_model(self._model_id, "greedy", 1, 2000, 1)
        model_res = self._wx_instance.generate_text(model, prompt)

        summary = model_res.get("results")[0].get("generated_text").strip()
        # enriched_text = article.get("enriched_text")
        # url = article.get("metadata").get("source").get("url")
        # ingest_datetime = article.get("metadata").get("ingest_datetime")
        document_id = article.get("document_id")
        
        lst_meta = [document_id, title, summary] #, enriched_text
        
        return lst_meta
    # i=1
    # get_summary(result.get("results")[i:i+1][0])

    def t_translate(self, headline: str):
        prompt = '''go through the below news headline and translate it into English.
        news headline:
        %s

        Also, identify the language of the news headline from Arabic, Russian, English, Chinese, French, Indonesian.
        
        Respond in following JSON format:
        {
        "News headline language": "text", 
        "English translation": "text"
        }
        '''%(headline)

        # model_id = 'meta-llama/llama-3-1-8b-instruct'
        # model_id = 'mistralai/mixtral-8x7b-instruct-v01'
        model = self._wx_instance.get_model(self._model_id, "greedy", 1, 500, 1)
        model_res = self._wx_instance.generate_text(model, prompt)
        res = model_res.get("results")[0].get("generated_text")
        return res.strip()
    # t_translate(result.get("results")[5].get("title"))
    # json.loads(t_translate(result.get("results")[4].get("title")))

    # 2. If two or more countries are not being discussed in the article_body, you can answer with "Not relevant"
    # If two or more countries are not being discussed in the below article, you must respond saying {"Category":"Match not found"}.
    # Now please review the article below and Identify the Primary Countries. Determine if the relationship between Primary Countries fits into any of the categories mentioned above in the definition json.
    # "Article Analysis":"brief analysis while answering all the wh questions and events"

    def insights(self, article):
        definition = '''{
            "Diplomatic Interaction": [
                {
                    "Definition": "Diplomatic Interaction refers to any formal communication, negotiation, or engagement between representatives of two or more sovereign states. This includes official meetings, dialogue, exchange of messages, and any form of interaction aimed at managing relationships, resolving disputes, or discussing mutual concerns."
                },
                {
                    "Key Indicators": "Mentions of ambassadors, foreign ministers, diplomatic talks, official visits, negotiations, or statements issued by government officials."
                }
            ],
            "Cooperation between Countries": [
                {
                    "Definition": "Cooperation between Countries involves joint efforts, agreements, or partnerships between two or more sovereign states aimed at achieving shared objectives. This can include economic, military, environmental, scientific, or cultural collaborations, where countries work together to address common challenges or promote mutual interests."
                },
                {
                    "Key Indicators": "References to treaties, agreements, joint initiatives, alliances, bilateral or multilateral partnerships, shared projects, and collaborative efforts in areas such as trade, defense, research, or humanitarian aid."
                }
            ],
            "Territorial Dispute": [
                {
                    "Definition": "A conflict between two or more states over the ownership, control, or sovereignty of a specific geographical area. This type of dispute typically involves competing claims to land, maritime boundaries, or other territory, often resulting in diplomatic tensions, militarized confrontations, or legal proceedings."
                },
                {
                    "Key Indicators": "References to contested borders, competing territorial claims, specific geographic locations, and diplomatic or military actions related to territory."
                }
            ],
            "Interstate Conflict": [
                {
                    "Definition": "A conflict between two or more recognized sovereign states involving military, economic, or political hostilities. These conflicts often include formal declarations of war, large-scale military operations, or significant diplomatic tensions between governments."
                },
                {
                    "Key Indicators": "Mention of state actors (e.g., countries or governments), military engagements, international treaties, alliances, or sanctions, and involvement of international organizations (e.g., United Nations)."
                }
            ],
            "Civil War": [
                {
                    "Definition": "An armed conflict within a single country between organized groups, typically involving the government and one or more factions seeking to challenge the state’s authority, control, or policies. Civil wars are characterized by prolonged violence, significant casualties, and attempts to change the government or territorial control."
                },
                {
                    "Key Indicators": "Internal divisions within a country, mention of government forces versus rebel or insurgent groups, references to regime change, secessionist movements, or large-scale internal violence."
                }
            ]
        }'''

        prompt = '''You are an International Relations Specialist and working on identifying relationship using the following definition JSON.

        definition JSON:
        %s

        Follow the below instructions:
        1. Please review the article below and identify the primary recognized sovereign nations. Then, assess whether the relationships between these nations align with any of the categories outlined in the above definition JSON.
        2. If two or more countries are not being discussed in the below article, you must categorize it under "Match not found".
        article:
        %s

        Respond in the below JSON format: 
        {
            "Category": "Match not found",
            "Primary Countries": ["Israel", "Palestine"],
            "Sentiment":"Neutral",
            "Organization":["Hamas"],
            "Person": ["Hassan Nasrallah"],
            "Analysis":"brief analysis of an article while answering all the wh questions and events under 100 words"
        }

        JSON Response:
        '''%(definition, article)

        # model_id = 'ibm/granite-13b-instruct-v2'          #7, 6
        # model_id = 'mistralai/mixtral-8x7b-instruct-v01' #7,10 
        # model_id = 'mistralai/mistral-large'                
        # model_id = 'meta-llama/llama-3-1-70b-instruct'    #9, 46 
        # model_id = 'meta-llama/llama-3-405b-instruct'     #26. 29
        # model_id = 'meta-llama/llama-3-70b-instruct'      #14,9
        # model_id = 'meta-llama/llama-3-8b-instruct'       #11, 14
        # model_id = 'meta-llama/llama-3-1-8b-instruct'
        model = self._wx_instance.get_model(self._model_id, "greedy", 1, 1000, 1)
        model_res = self._wx_instance.generate_text(model, prompt)

        # print(model_res.get("results")[0].get("generated_text"))
        try:
            res = json.loads(model_res.get("results")[0].get("generated_text"))
        except Exception as e:
            print("Err",e,"=Err-"*10)
            res = model_res.get("results")[0].get("generated_text")
        return res
    # output = insights(definition, lst_meta_agg[1][2])

    def doc_info_by_doc_id(self, doc_id, project_id=None, collection_ids=None):
        wd_query = f'(document_id:{doc_id})'
        discovery_article = self._wd_instance.query_docs(wd_query, project_id, collection_ids)
        res = discovery_article.get("results")[:][0]

        # Extracting and formatting desired fields
        doc_info = { "data": {
            "document_id": res.get("document_id", "Field 'document_id' tidak ada pada dokumen ini"),
            "title": res.get("title", "Field 'title' tidak ada pada dokumen ini"),
            "text": res.get("text", "Field 'text' tidak ada pada dokumen ini")[:600],  
            "ingest_datetime": res.get("metadata", {}).get("ingest_datetime", "-"),
            "URL": res.get("metadata", {}).get("source", {}).get("url", "-")
            }
        }

        return doc_info

    def extract_by_doc_id(self, doc_id, project_id=None, collection_ids=None):
        wd_query = f'(document_id:{doc_id})'
        discovery_article = self._wd_instance.query_docs(wd_query, project_id, collection_ids)
        lst_meta = self.ai_extraction(discovery_article, 1)
        doc_analysis = {
            "data":{
                "analysis": lst_meta[0][11]
            }
        }
        return doc_analysis
    
    def extract_by_ingest_datetime(self, date):

        # date = datetime.now() - timedelta(days=1)
        date_str = date.strftime('%Y-%m-%dT%H:%M:%SZ')

        wd_query = f'(metadata.ingest_datetime:{date_str[:10]})'
        discovery_article = self._wd_instance.query_docs(wd_query)
        lst_meta_agg = self.ai_extraction(discovery_article)
        return lst_meta_agg

    def ai_extraction(self, discovery_articles, count: int = 1000):
        lst_meta_agg =[]
        n=0
        for i in discovery_articles.get("results")[:]:
            if n >= count or n >= len(discovery_articles.get("results")):
                break
            # print(i)
            try:
                lst_meta = self.get_summary(i)
                output = self.insights(lst_meta[2])
                # print(output)
                Category = output.get("Category")
                Counties = output.get("Primary Countries")
                Counties_ = (lambda lst: ', '.join(lst) if isinstance(lst, list) else "-")(Counties)
                Sentiment = output.get("Sentiment")
                Organization = output.get("Organization")
                Organization_ = (lambda lst: ', '.join(lst) if isinstance(lst, list) else "-")(Organization)
                Person = output.get("Person")
                Analysis = output.get("Analysis")
                translation = json.loads(self.t_translate(lst_meta[1]))
                Language = translation.get("News headline language")
                Headline = translation.get("English translation")
                insight = "<div><h2>News Analysis:</h2><p><strong>Title:</strong> {}</p><p><strong>News Type:</strong> {}</p><p><strong>Analysis:</strong> {}</p><h3>Entities:</h3><p><strong>Affected country(s):</strong> {}</p><p><strong>Organizations Involved:</strong> {}</p><p><strong>News Sentiment:</strong> {}</p></div>".format(Headline, Category, Analysis,Counties_,Organization_, Sentiment)
                # print("Analysis",Analysis)
                lst_meta.extend([Headline, Language, Category, Counties, Sentiment, Organization, Person, Analysis, insight])
                lst_meta_agg.append(lst_meta)
                # print("--",lst_meta_agg)

            except Exception as e:
                print("=Err=",n, e,"=Err="*10)
            n+=1
                
        return lst_meta_agg


# a = AndromedaNews()
# c = a.doc_info_by_doc_id("web_crawl_eca4b5da-bb56-5df4-a8d3-b4f7ff34b1d2")
# print(c.keys())
# b = a.extract_by_doc_id("web_crawl_eca4b5da-bb56-5df4-a8d3-b4f7ff34b1d2")
# print(b[10])

##13 33 40 minutes



    