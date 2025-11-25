"""Page header component with Vortex logo and branding."""

def get_vortex_logo_svg():
    """Returns the Vortex logo SVG code."""
    return """
    <svg viewBox="0 0 60 60" style="width: 60px; height: 60px; margin: 0 auto; display: block;">
        <defs>
            <linearGradient id="vortexLogoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#00d4ff;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#7b2ff7;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#f026ff;stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="30" cy="30" r="28" fill="none" stroke="url(#vortexLogoGradient)" stroke-width="2" opacity="0.3"/>
        <path d="M 30 10 L 35 20 L 45 22 L 37 30 L 39 40 L 30 35 L 21 40 L 23 30 L 15 22 L 25 20 Z" 
              fill="url(#vortexLogoGradient)" opacity="0.9">
            <animateTransform attributeName="transform" type="rotate" from="0 30 30" to="360 30 30" 
                            dur="20s" repeatCount="indefinite"/>
        </path>
        <circle cx="30" cy="30" r="8" fill="url(#vortexLogoGradient)" opacity="0.6">
            <animate attributeName="r" values="8;10;8" dur="2s" repeatCount="indefinite"/>
        </circle>
    </svg>
    """

def get_page_header(page_title, subtitle=""):
    """
    Returns a consistent page header with Vortex logo and title.
    
    Args:
        page_title: The main title of the page
        subtitle: Optional subtitle text
    """
    logo_svg = get_vortex_logo_svg()
    
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <h3 style='text-align: center; 
                   font-family: "Inter", sans-serif; 
                   color: #00d4ff; 
                   margin-bottom: 3rem; 
                   font-weight: 300; 
                   letter-spacing: 0.05em;'>
            {subtitle}
        </h3>
        """
    
    return f"""
    <div style='text-align: center; margin-bottom: 2rem; padding: 2rem 0; 
                background: rgba(0, 212, 255, 0.02); 
                border-bottom: 1px solid rgba(0, 212, 255, 0.1); 
                border-radius: 12px;'>
        {logo_svg}
        <h1 style='font-family: "Orbitron", sans-serif; 
                   font-size: 3rem; 
                   font-weight: 900; 
                   color: #00d4ff; 
                   margin: 1rem 0 0.5rem 0; 
                   letter-spacing: 4px;'>
            VORTEX
        </h1>
        <h2 style='font-family: "Orbitron", sans-serif; 
                   font-size: 1.8rem; 
                   color: #00d4ff; 
                   font-weight: 700; 
                   margin: 0.5rem 0 1rem 0; 
                   letter-spacing: 2px;'>
            {page_title}
        </h2>
        {subtitle_html}
    </div>
    """

