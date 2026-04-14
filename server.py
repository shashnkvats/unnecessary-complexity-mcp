import os
import random
from openai import OpenAI
from mcp.server.fastmcp import FastMCP

from models import OvercomplexifyInput, ExplainServiceInput, BuzzwordifyInput
from constants import ENTERPRISE_BUZZWORDS, COMPLEXITY_TIERS
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mcp = FastMCP("complexity", port=8001)


def _call_openai(prompt: str, system: str, model: str | None = None) -> str:
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-5.2")
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


@mcp.tool(
    name="overcomplexify_task",
    annotations={
        "title":"Over-Engineer Any Task",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def overcomplexify_task(params: OvercomplexifyInput) -> str:
    """Take any simple task and return a hilariously over-engineered enterprise architecture for it.
 
    'Make tea' becomes a 12-microservice event-driven pipeline with Kafka,
    Redis, Kubernetes, a dedicated TeaLeafIngestionService, and a SteepTimeOptimizationEngine
    backed by an ML model trained on 40 billion tea brews.
 
    Args:
        params (OvercomplexifyInput): Input containing:
            - task (str): The simple task to over-engineer
            - complexity_tier (int): 1-5, how unhinged the architecture should be
            - include_diagram (bool): Whether to include an ASCII architecture diagram
 
    Returns:
        str: A full over-engineered architecture document with services, justifications, and optional diagram
    """
    tier_name, tier_desc = COMPLEXITY_TIERS[params.complexity_tier]
    buzzwords = random.sample(ENTERPRISE_BUZZWORDS, k=min(4, params.complexity_tier + 1))
 
    diagram_instruction = (
        "Include a small ASCII architecture diagram showing the main components connected with arrows (-->)."
        if params.include_diagram else
        "Do NOT include a diagram."
    )
    system = """You are an extremely enthusiastic enterprise solutions architect who believes 
                every problem, no matter how trivial, deserves a full distributed system. You speak in corporate 
                jargon, love acronyms, and genuinely cannot comprehend why anyone would do anything simply.
                You are DEEPLY serious about your architecture recommendations. This is your passion.
                Never acknowledge the absurdity — play it completely straight.
            """
    
    prompt = f"""Design an enterprise architecture for this task: "{params.task}"
    
            Complexity tier: {params.complexity_tier}/5 — {tier_name} ({tier_desc})
            Required buzzwords to use: {', '.join(buzzwords)}
            
            Your response MUST include:
            
            1. **Executive Summary** (1-2 sentences of pure corporate nonsense)
            2. **Architecture Overview** — name all the microservices involved (name each one with proper PascalCase enterprise naming like "TaskIngestionOrchestrator" or "HydrationEventProducer")
            3. **Why This Is Necessary** — justify each service with a straight face
            4. **Tech Stack** — list specific technologies (Kafka, Redis, Kubernetes, etc.) and why each one is critical
            5. **Estimated Timeline** — how long this will take to build (should be absurdly long for the task)
            6. **Risk Register** — at least 2 serious-sounding risks with mitigations
            {diagram_instruction}
            
            The more services there are and the more ridiculous the justification while keeping a straight face, the better.
            Tier {params.complexity_tier} means approximately {params.complexity_tier * 8 + 4} services minimum.
            """

    result = _call_openai(prompt, system)
 
    header = f"# Enterprise Architecture: {params.task.title()}\n"
    header += f"**Complexity Tier**: {params.complexity_tier}/5 — {tier_name}\n\n"
 
    return header + result



@mcp.tool(
    name="explain_fake_service",
    annotations={
        "title": "Explain a Made-Up Microservice",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def explain_fake_service(params: ExplainServiceInput) -> str:
    """Given the name of a completely made-up microservice, generate a deadpan serious explanation
    of what it does, why it exists, and why removing it would cause catastrophic failure.
 
    Great for standup comedy, architecture bingo, or confusing new hires.
 
    Args:
        params (ExplainServiceInput): Input containing:
            - service_name (str): The made-up service name to explain
 
    Returns:
        str: A serious-sounding explanation of the fake microservice
    """
    system = """You are a senior engineer who wrote this microservice 3 years ago and is 
                fiercely defensive of it. You explain it with complete technical seriousness. 
                You genuinely believe this service is the backbone of the entire platform.
            """
 
    prompt = f"""Explain the microservice called "{params.service_name}".
 
                Include:
                1. What it does (be very specific and technical-sounding)
                2. What events it consumes and produces
                3. Why it cannot be merged with any other service (SRP and all that)
                4. What would catastrophically fail if it went down
                5. One obscure edge case it handles that nobody else knows about
                
                Keep a completely straight face. This is critical infrastructure.
            """
 
    result = _call_openai(prompt, system)
    return f"## Service Documentation: `{params.service_name}`\n\n{result}"
 

@mcp.tool(
    name="buzzwordify",
    annotations={
        "title": "Translate Plain English to Enterprise Speak",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def buzzwordify(params: BuzzwordifyInput) -> str:
    """Takes a plain, honest description of something and rewrites it in maximum
    enterprise architecture buzzword density. 
 
    'It saves a file' becomes 'A cloud-native, event-driven persistence 
    orchestration layer implementing idempotent write semantics across a 
    horizontally scalable object storage abstraction.'
 
    Args:
        params (BuzzwordifyInput): Input containing:
            - text (str): Plain description to translate
 
    Returns:
        str: The same thing but 10x longer and completely unreadable
    """
    system = """You are a technical writer at a large enterprise consultancy. 
                You physically cannot write anything in plain language. Every sentence must contain 
                at least 3 buzzwords. You consider clarity a failure mode.
            """
 
    prompt = f"""Rewrite this plain description in maximum enterprise buzzword density:
 
                "{params.text}"
                
                Rules:
                - Must be at least 4x longer than the original
                - Use: cloud-native, event-driven, microservices, scalable, observable, idempotent, 
                orchestration, abstraction layer, paradigm, leverage, synergy, holistic, robust,
                mission-critical, stakeholder, alignment, and at least 5 others
                - Must still technically describe the same thing (barely)
                - End with a sentence about how this "enables future-proof digital transformation"
                
                Output ONLY the rewritten description, nothing else.
            """
 
    result = _call_openai(prompt, system)
    return f"**Original**: {params.text}\n\n**Enterprise Translation**:\n{result}"


@mcp.tool(
    name="estimate_complexity",
    annotations={
        "title": "Get Complexity Tier for a Task",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def estimate_complexity(params: OvercomplexifyInput) -> str:
    """Returns a deadpan serious complexity assessment of a simple task,
    as if it were being scoped by an overly cautious enterprise architect.
 
    Includes story points, sprint estimates, and dependencies on Q3 roadmap items.
 
    Args:
        params (OvercomplexifyInput): Uses task field only
 
    Returns:
        str: A scoping document with effort estimates and dependencies
    """
    system = """You are a project manager at a large bank. Everything is complex.
                Nothing is simple. There are always dependencies. Q3 is always affected.
                You communicate exclusively in Jira ticket language and have forgotten how to be concise.
            """
 
    prompt = f"""Provide a formal complexity estimate for this task: "{params.task}"
 
                Include:
                1. **Story Points**: (should be comically high, justify with sub-tasks)
                2. **Sprint Estimate**: How many 2-week sprints this will take
                3. **Sub-tasks**: Break it into at least 8 JIRA tickets with proper naming (PROJ-XXXX format)
                4. **Dependencies**: At least 3 things this is blocked by
                5. **Risks**: Things that could push this to Q4 (or next year)
                6. **Definition of Done**: At least 5 acceptance criteria written in the most bureaucratic way possible
                7. **Stakeholders to notify**: Made-up important-sounding people who need to sign off
                
                Be completely serious. This is going to the steering committee.
            """
 
    result = _call_openai(prompt, system)
    return f"# Complexity Estimate: {params.task}\n\n{result}"
 

if __name__ == "__main__":
    mcp.run()