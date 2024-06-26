# -*- coding: utf-8 -*-
"""llm_chain_main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PbNR6v6PDUFjfFOeZvI1wvrLyL70eWOp
"""

from google.colab import drive
drive.mount('/content/gdrive')

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore")

#!pip install openai langchain

import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain,RouterOutputParser
from IPython.display import display, Markdown
from langchain.chains import RetrievalQA
from openai import OpenAI
import pickle

os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI()
retrieve_fine_tuned = client.fine_tuning.jobs.retrieve("ftjob-eFMucjOZST24lrljjLteWie8")

llm_model = retrieve_fine_tuned.fine_tuned_model
gpt_chat = ChatOpenAI(temperature=0, model=llm_model)

pickle_file_path = '/content/gdrive/MyDrive/Conservatives-Official/Vegetation/all_factor_prompts.pkl'
with open(pickle_file_path, 'rb') as file:
    all_factor_prompts = pickle.load(file)

general_prompt = """
          Provide state level policy reccommendations for the given text specifications.
          Consider the future predictions of dependent factors abd yield predictions below.
          Make sure explain how the quantities

          If in case the factor and yield predictions are not available, use the latest similar facts you
          are trained on to give the recommendations.
          but please dont assume anything. Give responses as per the latest available statistics.

          Do not forget to add all the statistical data (specify the numbers and quantities as well) and
          give more technical details

          Factor Predictions:
          {factor_predictions}

          Yield Predictions:
          {yield_predictions}

          Text :
          {text}
          """

main_prompt_template = """
                Generate the modified policy and recommendations by combining the previous responses\
                making it much more specific.\

                Also you need to tell what each factor prediction value signify and \
                what yield prediction value signify. Make sure you explain with the quantities given.\

                Make sure you explain how the quantities affect the yield.\
                Add statistical data and technical details. See the below format.\

                Analyze the actual questions and \
                check what has been asked for and give appropriate responses.

                The implentations should be as per our previous responses and \
                factor predictions not exactly the same as sample output.

                Please use the sample output as a reference.

                Sample Output: \
                {sample_output} \

                Previous Responses: \
                {prev_resp} \

                """

sample_output = """
Factor Prediction Values:

1. Soil Moisture = 0.28 signifies the current level of moisture in the soil, which is crucial for determining the optimal timing and amount of irrigation required for wheat cultivation. A lower soil moisture value indicates that the soil may be dry and in need of irrigation to support healthy crop growth.

2. NDVI Index = 9500 represents the Normalized Difference Vegetation Index, which is a measure of the health and density of vegetation. A higher NDVI value indicates lush and healthy vegetation, which correlates with higher crop yields. Farmers can use this data to assess the overall health of their wheat crop and make adjustments to their farming practices if needed.

3. Surface Temperature = 200 Kelvin indicates the temperature of the soil surface, which can impact various physiological processes in plants, including growth and development. Lower surface temperatures may slow down plant growth, while higher temperatures can lead to stress and reduced yields. Farmers can use this data to adjust irrigation and other management practices to optimize crop growth.

4. Pesticide Content = 100 percent signifies the concentration of pesticides in the soil or on the crop. While pesticides are essential for controlling pests and diseases, excessive use can have negative environmental and health impacts. Farmers can use this data to ensure that pesticide application is done judiciously, following integrated pest management practices to minimize environmental harm.

Yield Prediction Value:

1. Yield = 4 Brussels per acre represents the expected yield of wheat per acre of land. This value is crucial for farmers to estimate their potential income and plan for harvesting and marketing activities. By analyzing factors such as soil moisture, NDVI index, surface temperature, and pesticide content, farmers can make informed decisions to optimize their yield and profitability.

How Quantities Affect Yield:

1. Soil Moisture: Adequate soil moisture is essential for seed germination, root development, and nutrient uptake in wheat plants. Insufficient moisture can lead to stunted growth and reduced yields. By monitoring soil moisture levels and irrigating accordingly, farmers can ensure optimal conditions for crop growth and maximize yield potential.

2. NDVI Index: A high NDVI value indicates healthy and dense vegetation, which is directly correlated with higher wheat yields. Monitoring the NDVI index allows farmers to detect early signs of stress or disease in the crop and take corrective actions to maintain high productivity.

3. Surface Temperature: Wheat plants have an optimal temperature range for growth, and extreme temperatures can negatively impact yield. Monitoring surface temperature helps farmers adjust irrigation schedules, implement heat stress management practices, and optimize planting dates to mitigate the effects of temperature stress on yield.

4. Pesticide Content: While pesticides are necessary for protecting wheat crops from pests and diseases, excessive pesticide use can harm beneficial organisms, contaminate water sources, and lead to pesticide resistance. By monitoring pesticide content and following integrated pest management practices, farmers can minimize environmental impact while effectively controlling pests and maximizing yield.

State Level Policy Recommendations:

1. Invest in Satellite Data Integration and Research: Allocate resources to integrate surface reflectance data, soil moisture, NDVI index, surface temperature, pesticide content, water quality, and surface reflectance data into agricultural models. Partner with satellite data providers and research institutions to access, analyze, and develop predictive models that incorporate this data to forecast wheat supply and demand.

  -Implementation: Invest $2 million in research and development to enhance algorithms and models for predicting yield based on the provided data. This initiative aims to improve the accuracy of forecasting and yield management.

2. Enhance Technological Infrastructure and Data Collection: Develop infrastructure for collecting and analyzing surface temperature and soil moisture data through satellite imagery and ground-based sensors to improve the precision and temporal resolution of data.

  -Implementation: Implement a state-wide soil moisture monitoring program with 75 in-situ sensors to provide real-time information on soil moisture content.

3. Promote Education and Training: Implement programs to educate farmers on the importance of utilizing surface temperature, soil moisture, and other data in wheat yield management. Provide training for farmers on how to interpret and utilize the data for decision-making.

  -Implementation: Develop training programs for 500 farmers on utilizing streamflow data to optimize irrigation and water use in wheat cultivation, with an expected water use efficiency improvement of 20%.

4. Collaborate with Agricultural Community and State Agencies: Foster collaboration between governmental, scientific, and agricultural communities to promote the sharing of knowledge and resources relating to the data. This will lead to a more integrated approach to policy development and agricultural planning.

  -Implementation: Facilitate collaboration between different stakeholders, with the goal of reducing water usage in the agriculture sector by 15% through streamflow data utilization.

5. Policy Incentives and Water Conservation Programs: Develop policy incentives for farmers to adopt innovative technologies and sustainable practices that leverage the provided data for better agricultural planning.

  -Implementation: Provide financial incentives or subsidies for farmers to enroll in water conservation programs. On average, farmers enrolled in these programs should see a reduction in water usage through better water management practices.

"""

def run_chains(llm, input_pts, factor_pred, yield_pred, general_prompt=general_prompt):
    # Initialize an empty list to hold all the chains
    chains_list = []

    # Create a ChatPromptTemplate for each chain using the general_prompt
    # Note: If each chain requires a different prompt, you'll need to customize this part
    prompts = [ChatPromptTemplate.from_template(general_prompt) for _ in range(6)]

    # Define output keys for each chain
    output_keys = ["sr_resp", "st_resp", "sm_resp", "wq_resp", "sd_resp", "pest_resp"]

    # Create and append each chain to the chains_list
    for prompt, output_key in zip(prompts, output_keys):
        chain = LLMChain(llm=llm, prompt=prompt, output_key=output_key)
        chains_list.append(chain)

    # Run each chain and collect responses in a dictionary
    responses = {}
    for chain, inp in zip(chains_list, input_pts):
        # Assuming the 'run' method returns a response directly
        # You may need to adjust this part based on your specific implementation
        response = chain.run({'factor_predictions': factor_pred, 'yield_predictions': yield_pred, 'text': inp})  # This is simplified; your actual call might differ
        responses[chain.output_key] = response

    return chains_list, responses

def generate_main_response(main_prompt_template, llm, previous_responses):
  all_resp = ""
  for key, resp in previous_responses.items():
    all_resp += resp

  main_prompt = ChatPromptTemplate.from_template(main_prompt_template)
  chain = LLMChain(llm=llm, prompt=main_prompt, output_key="main_response")
  response = chain.run({'sample_output': sample_output, 'prev_resp': all_resp})
  #print(response)
  #display(Markdown(response))
  file_path = 'src/policies.txt'

  # Save the response to a text file
  with open(file_path, 'w') as file:
    file.write(main_response)
  return response

def generate_response(llm, input_prompts, factors_pred, yield_pred,
                      general_prompt = general_prompt,
                      main_prompt_template = main_prompt_template):
  chains, responses = run_chains(gpt_chat, input_prompts, factors_pred, yield_pred, general_prompt)
  main_response = generate_main_response(main_prompt_template, gpt_chat, responses)
  return main_response


#sample factor predictions
factors_prediction = " Soil Moisture = 0.28 \
            NDVI Index = 0.5 \
            Surface Temparature = 323 Kelvin\
            Pesticide Content = 12 percent\
            Surface Reflectance = 720 nano meter\
            "

#sample yield predictions
yield_prediction = "Yield = 45 brussels per acre"


main_response = generate_response(gpt_chat, all_factor_prompts, factors_prediction, yield_prediction,
                      general_prompt = general_prompt,
                      main_prompt_template = main_prompt_template)
#display(Markdown(main_response))

