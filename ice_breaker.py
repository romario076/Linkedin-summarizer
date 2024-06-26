from typing import Tuple
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from chains.custom_chains import (
    get_summary_chain,
    get_interests_chain,
    get_ice_breaker_chain,
)
from third_parties.linkedin import scrape_linkedin_profile

from third_parties.twitter import scrape_user_tweets
from output_parsers import (
    summary_parser,
    topics_of_interest_parser,
    ice_breaker_parser,
    Summary,
    IceBreaker,
    TopicOfInterest,
)


#API_KEY_OPENAI = "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"
#API_KEY_PROXY = "VS0Jm8Lf2jLirLKU6g2WAw"
#load_dotenv()

def ice_break_with(name: str) -> Tuple[Summary, IceBreaker, TopicOfInterest, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, manual=True)

    use_twitter = False
    if use_twitter:
        twitter_username = twitter_lookup_agent(name=name)
        tweets = scrape_user_tweets(username=twitter_username)
    else:
        twitter_username = ""
        tweets = ""

    summary_chain = get_summary_chain(use_twitter=use_twitter)
    summary_and_facts = summary_chain.run(information=linkedin_data, twitter_posts=tweets)
    summary_and_facts = summary_parser.parse(summary_and_facts)

    interests_chain = get_interests_chain(use_twitter=use_twitter)
    interests = interests_chain.run(information=linkedin_data, twitter_posts=tweets)
    interests = topics_of_interest_parser.parse(interests)

    ice_breaker_chain = get_ice_breaker_chain(use_twitter=use_twitter)
    ice_breakers = ice_breaker_chain.run(information=linkedin_data, twitter_posts=tweets)
    ice_breakers = ice_breaker_parser.parse(ice_breakers)

    return (
        summary_and_facts,
        interests,
        ice_breakers,
        linkedin_data.get("profile_pic_url"),
    )
