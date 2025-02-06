from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
import streamlit as st
#import streamlit-folium as st_folium
from streamlit_folium import st_folium
from dotenv import load_dotenv
from streamlit_extras.let_it_rain import rain

load_dotenv()

#streamlit_page_config
st.set_page_config(page_title="content researcher and writer, powered by crewai", page_icon="👩🏻", layout="wide")

#title and description
st.title("content researcher and writer, powered by crewai")
st.markdown("Generate blog posts about any topic using Generative AI")


st.snow()

with st.sidebar:
    st.title("blog post generator")
    st.header("content settings")

    topic=st.text_area(
        "Enter your topic",
        height=100,
        placeholder="enter the topic"
    )
    st.markdown("###LLM Settings")
    temperature=st.slider("Temperature",0.0,1.0,0.7)

    st.markdown("___")

    generate_button=st.button("Generate Content",type="primary",use_container_width=True)

    with st.expander("! How to use:"):
        st.markdown("""
        1.Enter your desired content topic,\n
        2.Play with he temperature,\n
        3.Click "generate content" to start,\n
        4.Wait for the AI to generate your article,\n
        5.Download the result as a markdown file
        """
        )
    
def generate_content(topic):
    llm = LLM(
    model="groq/gemma2-9b-it",
    temperature=0.7
    )
    #tool 2
    search_tool=SerperDevTool(n_results=10)

    #Agent 1 Research Analyst

    senior_research_analyst=Agent(
        role="Senior Research Analyst",
        goal=f"research, analyse and syntesize comprehensive information on {topic} from reliable web sources",
        backstory="You're an expert research analyst with advanced web research skills."
                "you excel at finding, analysing, synthesizing information from"
                "accross the internet using search tools. You're skilled at"
                "distinguishing reliable sources from unreliable ones"
                "fact-checking, cross referencing information, and"
                "identifying key patterns and insights. You provide"
                "well-orgainzed research briefs with proper citations"
                "and source verifications. Your analysis include both"
                "raw data and interpreted insights, making complex"
                "information accessible and actionable.",
        tools=[search_tool],
        allow_delegations=False,
        verbose=True,
        llm=llm
    )

    #Agent 2 Content Writer

    content_writer=Agent(
        role="Content Writer",
        goal="Trasform research findings into engaging blog posts while maintaing accuracy",
        backstory="You're a skilled content writer specialized in creating "
                "engaging, accessible content from technical research."
                "You work closely with the Senior Research Analyst and excel at maintaining the perfect "
                "balance between informative and entertaining writing,"
                "while ensuring all facts and citations from the research "
                "are properly incorporated. You have a talent for making "
                "complex topics approachable without oversimplifying them.",
        allow_delegations=False,
        verbose=True,
        llm=llm

    )

    #Research Tasks

    research_tasks=Task(
        description=f"""
                1.Conduct comprehensive research on {topic} including:
                    - Recent developments and news
                    - Key industry trends and innovations
                    - Expert opinions and analyses
                    - Statistical data and market insights
                2.Evaluate source credibility and fact-check all information
                3.Organize findings into a structured research brief
                4.Include all relevant citations and sources                
    """,
        expected_output="""A detailed research report containing:
                    - Executive summary of key findings
                    - Comprehensive analysis of current trends and developments
                    - List of verified facts and statistics
                    - All citations and links t original Sources
                    - Clear categorization of main themes and patterns
                    Pleasa format with clear sections and bullet points for easy reference.""",

        tools=[search_tool],
        agent=senior_research_analyst
        )

    #Task 2 Content Writing

    Writing_task=Task(
        description="""
                using the research brief provided, create an engaging blog post that:
                1. Transfroms technical information into accessible content
                2. Maintain all factual accuracy and citations from the research
                3. Includes:
                    - attention-grabbing introduction
                    - Well-structured body sectons with clear headings
                    - Compelling conclusion
                4. Preserve all sources citations in [Source:URL] format
                5. Includes a reference section at the end
            """,
        expected_output="""A polished blog post in markdown-format that:
                - Engages readers while maintaining accuracy
                - Contains properly structured sections
                - Includes inline citations hyperlinked to the original source url
                - Presents information in a accessible yet informative way
                - Follows proper markdown formatting, use H1 for the title and H3 for the sub-sections""",
        agent=content_writer
    )

    crew=Crew(
        agents=[senior_research_analyst,content_writer],
        tasks=[research_tasks,Writing_task],
        verbose=True
    )


    return crew.kickoff(inputs={"topic":topic})

# main content area
if generate_button:
    with st.spinner("Generating content...this may take a moment"):
        try:
            result=generate_content(topic)
            st.markdown("### Generated Content")
            st.markdown(result)

            st.download_button(
                label="Download content",
                data=result.raw,
                file_name=f"{topic.lower().replace(' ','_')}_article.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f" an error occured: {str(e)}")

#Footer
st.markdown("---")
st.markdown("Built with crewai, streamlit and groq")
































# def example():
#     rain(
#         emoji="🎈",
#         font_size=54,
#         falling_speed=5,
#         animation_length="infinite",
#     )

# example()