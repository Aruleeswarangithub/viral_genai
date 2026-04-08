def generate_brand_text(brand_name: str, persona: str, platform: str, product_brief: str) -> str:
    persona = persona.strip().lower()
    platform = platform.strip().lower()

    intros = {
        "professional": f"{brand_name} introduces a smarter way to experience {product_brief}.",
        "witty": f"{product_brief}, but make it unforgettable. That is the {brand_name} way.",
        "urgent": f"Don’t miss your chance to try {product_brief} from {brand_name} today.",
        "luxury": f"Discover premium craftsmanship with {product_brief} from {brand_name}.",
    }

    platform_cta = {
        "instagram": "Tap in, save this post, and share it with your crew.",
        "linkedin": "Connect with us to explore how this offering creates real value.",
        "facebook": "Comment below and tell us how you would use it.",
        "twitter": "Reply with your take and join the conversation.",
    }

    intro = intros.get(persona, f"{brand_name} presents {product_brief} with a bold new perspective.")
    cta = platform_cta.get(platform, "Explore more and stay connected for updates.")

    body = (
        f"{intro} Designed for people who care about quality, performance, and clarity, "
        f"this campaign highlights benefits in a format tailored for {platform.title()}. {cta}"
    )
    return body


def enhance_prompt(product_brief: str, persona: str, platform: str) -> str:
    tone_map = {
        "professional": "clean commercial composition, modern branding, sharp focus",
        "witty": "playful concept, vibrant colors, eye-catching composition",
        "urgent": "high contrast, bold visual storytelling, dramatic lighting",
        "luxury": "premium studio lighting, elegant composition, refined textures",
    }

    tone = tone_map.get(persona.strip().lower(), "high-quality marketing visual, polished commercial style")

    return (
        f"Create a high-quality social media advertisement for {product_brief}, "
        f"optimized for {platform}. Use {tone}, photorealistic detail, premium design language, "
        f"balanced framing, ad-ready composition, and strong product focus."
    )


def choose_demo_image(persona: str, platform: str) -> str:
    persona = persona.strip().lower()
    platform = platform.strip().lower()

    if persona == "luxury":
        return "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=80"
    if persona == "urgent":
        return "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1200&q=80"
    if platform == "linkedin":
        return "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1200&q=80"
    return "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1200&q=80"
