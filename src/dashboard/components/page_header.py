"""Reusable page header component for all dashboard pages."""

def get_page_header_html(page_title, subtitle=""):
    """
    Generate consistent page header HTML with Vortex logo and branding.
    
    Args:
        page_title: The main title of the page (e.g., "Dashboard Summary", "Sales Analytics")
        subtitle: Optional subtitle text
    
    Returns:
        HTML string for the page header
    """
    # Build subtitle HTML only if subtitle is provided
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""<p style='font-size: 1.2rem; font-family: "Inter", sans-serif; color: #00d4ff; font-weight: 300; letter-spacing: 0.05em; margin-top: 0.5rem;'>{subtitle}</p>"""
    
    # Create a unique gradient ID for this page
    gradient_id = f"pageLogoGradient-{page_title.replace(' ', '-')}"
    
    # Build the complete HTML in one clean string
    html = f"""<style>
@keyframes vortexRotate {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
}}
.vortex-logo {{
    animation: vortexRotate 20s linear infinite;
    filter: drop-shadow(0 0 15px rgba(123, 47, 247, 0.5));
}}
</style>
<div style='text-align: center; margin-bottom: 2rem; padding: 2rem 0; background: rgba(0, 212, 255, 0.02); border-bottom: 1px solid rgba(0, 212, 255, 0.1); border-radius: 12px;'>
<svg class="vortex-logo" viewBox="0 0 60 60" style="width: 60px; height: 60px; margin: 0 auto; display: block;">
<defs>
<linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#00d4ff;stop-opacity:1" />
<stop offset="50%" style="stop-color:#7b2ff7;stop-opacity:1" />
<stop offset="100%" style="stop-color:#f026ff;stop-opacity:1" />
</linearGradient>
</defs>
<circle cx="30" cy="30" r="28" fill="none" stroke="url(#{gradient_id})" stroke-width="2" opacity="0.3"/>
<circle cx="30" cy="30" r="22" fill="none" stroke="url(#{gradient_id})" stroke-width="2" opacity="0.5"/>
<circle cx="30" cy="30" r="16" fill="none" stroke="url(#{gradient_id})" stroke-width="2" opacity="0.7"/>
<path d="M 30 14 L 38 30 L 30 46 L 22 30 Z" fill="url(#{gradient_id})" opacity="0.8"/>
<circle cx="30" cy="30" r="4" fill="#00d4ff"/>
<circle cx="30" cy="30" r="2" fill="#ffffff"/>
</svg>
<h1 style='font-family: "Orbitron", sans-serif; font-size: 3rem; font-weight: 900; color: #00d4ff; margin: 1rem 0 0.5rem 0; letter-spacing: 4px;'>VORTEX</h1>
<h2 style='font-family: "Orbitron", sans-serif; font-size: 1.8rem; color: #00d4ff; font-weight: 700; margin: 0.5rem 0 0.5rem 0; letter-spacing: 2px;'>{page_title}</h2>
{subtitle_html}
</div>"""
    
    return html

