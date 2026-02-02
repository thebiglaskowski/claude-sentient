"""Vision API integration for Claude Sentient SDK.

Provides screenshot analysis, error state capture, and visual comparison
capabilities using Claude's vision features.
"""

import base64
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .datatypes import ModelTier


@dataclass
class ScreenshotResult:
    """Result of screenshot analysis."""

    image_path: str
    analysis: str
    model_used: str
    elements_found: list[dict[str, Any]] = field(default_factory=list)
    issues_detected: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualDiff:
    """Result of visual comparison between two screenshots."""

    before_path: str
    after_path: str
    differences: list[dict[str, Any]] = field(default_factory=list)
    similarity_score: float = 0.0  # 0-1, 1 = identical
    summary: str = ""
    regions_changed: list[dict[str, Any]] = field(default_factory=list)


class VisionAnalyzer:
    """Analyze screenshots and visual content using Claude's vision API.

    This class provides methods for:
    - Analyzing screenshots for UI/UX issues
    - Capturing error states for debugging
    - Comparing screenshots for visual regression testing
    - Extracting text and elements from images
    """

    # Standard viewport sizes for responsive testing
    VIEWPORT_SIZES = {
        "mobile": (375, 667),     # iPhone SE
        "tablet": (768, 1024),    # iPad
        "desktop": (1280, 800),   # Laptop
        "wide": (1920, 1080),     # Full HD
    }

    def __init__(self, default_model: ModelTier = ModelTier.SONNET):
        """Initialize the vision analyzer.

        Args:
            default_model: Default model to use for analysis
        """
        self.default_model = default_model
        self._screenshot_cache: dict[str, str] = {}

    def encode_image(self, image_path: str | Path) -> str:
        """Encode an image file to base64.

        Args:
            image_path: Path to the image file

        Returns:
            Base64-encoded image string
        """
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Check cache
        cache_key = str(path.absolute())
        if cache_key in self._screenshot_cache:
            return self._screenshot_cache[cache_key]

        # Read and encode
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        # Cache it
        self._screenshot_cache[cache_key] = encoded
        return encoded

    def get_image_media_type(self, image_path: str | Path) -> str:
        """Get the media type for an image file.

        Args:
            image_path: Path to the image file

        Returns:
            Media type string (e.g., "image/png")
        """
        path = Path(image_path)
        suffix = path.suffix.lower()

        media_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }

        return media_types.get(suffix, "image/png")

    def build_vision_prompt(
        self,
        prompt: str,
        image_path: str | Path,
    ) -> list[dict[str, Any]]:
        """Build a vision API prompt with an image.

        Args:
            prompt: The analysis prompt
            image_path: Path to the image

        Returns:
            List of content blocks for the API
        """
        encoded = self.encode_image(image_path)
        media_type = self.get_image_media_type(image_path)

        return [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": encoded,
                },
            },
            {
                "type": "text",
                "text": prompt,
            },
        ]

    def build_comparison_prompt(
        self,
        prompt: str,
        before_path: str | Path,
        after_path: str | Path,
    ) -> list[dict[str, Any]]:
        """Build a vision API prompt for comparing two images.

        Args:
            prompt: The comparison prompt
            before_path: Path to the "before" image
            after_path: Path to the "after" image

        Returns:
            List of content blocks for the API
        """
        before_encoded = self.encode_image(before_path)
        after_encoded = self.encode_image(after_path)
        before_media = self.get_image_media_type(before_path)
        after_media = self.get_image_media_type(after_path)

        return [
            {
                "type": "text",
                "text": "BEFORE:",
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": before_media,
                    "data": before_encoded,
                },
            },
            {
                "type": "text",
                "text": "AFTER:",
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": after_media,
                    "data": after_encoded,
                },
            },
            {
                "type": "text",
                "text": prompt,
            },
        ]

    # --- Analysis Prompts ---

    @staticmethod
    def get_ui_analysis_prompt() -> str:
        """Get the prompt for UI/UX analysis."""
        return """Analyze this screenshot for UI/UX issues. Focus on:

1. **Layout Issues**
   - Alignment problems
   - Spacing inconsistencies
   - Overflow or clipping

2. **Visual Design**
   - Color contrast (accessibility)
   - Typography issues
   - Visual hierarchy

3. **Usability**
   - Clear call-to-action buttons
   - Form field labels and hints
   - Error state visibility

4. **Accessibility**
   - Text readability
   - Touch target sizes
   - Color-only information

Respond with a structured analysis including:
- Issues found (severity: critical/major/minor)
- Specific locations in the screenshot
- Suggested fixes

Format as JSON with keys: issues, suggestions, accessibility_score (0-100)."""

    @staticmethod
    def get_error_analysis_prompt() -> str:
        """Get the prompt for error state analysis."""
        return """Analyze this screenshot showing an error state. Identify:

1. **Error Type**
   - What kind of error is displayed?
   - Is the error message clear to users?

2. **Error Location**
   - Where on the screen is the error shown?
   - Is it prominently visible?

3. **Error Details**
   - What does the error message say?
   - Are there any error codes visible?

4. **Context**
   - What action likely caused this error?
   - Are there any clues about the root cause?

5. **Recovery Options**
   - Are there clear next steps for the user?
   - Is there a retry or dismiss option?

Respond with structured analysis including:
- error_type
- error_message (exact text if visible)
- probable_cause
- suggested_fix
- user_impact (critical/high/medium/low)

Format as JSON."""

    @staticmethod
    def get_visual_diff_prompt() -> str:
        """Get the prompt for visual comparison."""
        return """Compare these two screenshots (BEFORE and AFTER) and identify all visual differences.

For each difference found, describe:
1. **Location**: Where on the screen (top-left, center, etc.)
2. **Type**: What kind of change (added, removed, modified, moved)
3. **Element**: What UI element changed
4. **Description**: Brief description of the change

Also provide:
- Overall similarity score (0-100, where 100 = identical)
- Summary of changes in one sentence
- Whether changes appear intentional or could be regressions

Format response as JSON with keys:
- differences (list of changes)
- similarity_score
- summary
- potential_regressions (list of concerning changes)"""

    @staticmethod
    def get_accessibility_prompt() -> str:
        """Get the prompt for accessibility analysis."""
        return """Analyze this screenshot for web accessibility compliance. Check for:

1. **Color Contrast**
   - Text contrast ratios (WCAG AA: 4.5:1 normal, 3:1 large)
   - Non-text contrast for UI elements

2. **Text Readability**
   - Font size (minimum 16px body)
   - Line height and spacing
   - Text over images

3. **Interactive Elements**
   - Button/link visibility
   - Touch target size (minimum 44x44px)
   - Focus indicators

4. **Information Conveyance**
   - Color-only information
   - Icons with text alternatives
   - Error identification

5. **Content Structure**
   - Visual heading hierarchy
   - List formatting
   - Table structure

Rate compliance for each WCAG level (A, AA, AAA) and provide:
- compliance_score (0-100)
- critical_issues (must fix)
- recommendations (should fix)
- best_practices (nice to have)

Format as JSON."""

    @staticmethod
    def get_text_extraction_prompt() -> str:
        """Get the prompt for extracting text from screenshots."""
        return """Extract all visible text from this screenshot.

Organize the text by visual hierarchy:
1. **Headings**: Main titles and section headers
2. **Navigation**: Menu items, links, tabs
3. **Content**: Body text, descriptions
4. **Interactive**: Button labels, form labels
5. **System**: Error messages, tooltips, status text

For each text element, provide:
- text: The actual text content
- type: heading/navigation/content/interactive/system
- location: approximate screen position

Format as JSON with key "text_elements" containing the list."""

    def clear_cache(self) -> None:
        """Clear the screenshot cache."""
        self._screenshot_cache.clear()


# Utility functions for common vision operations

async def analyze_screenshot(
    image_path: str | Path,
    prompt: str | None = None,
    analysis_type: str = "ui",
    model: ModelTier = ModelTier.SONNET,
) -> ScreenshotResult:
    """Analyze a screenshot using Claude's vision capabilities.

    Args:
        image_path: Path to the screenshot file
        prompt: Custom analysis prompt (optional)
        analysis_type: Type of analysis - "ui", "error", "accessibility", "text"
        model: Model to use for analysis

    Returns:
        ScreenshotResult with analysis findings

    Note: This function builds the vision prompt but does not call the API directly.
    The caller should use the returned content blocks with Claude's API.
    """
    analyzer = VisionAnalyzer(default_model=model)

    # Select prompt based on analysis type
    if prompt is None:
        prompts = {
            "ui": VisionAnalyzer.get_ui_analysis_prompt(),
            "error": VisionAnalyzer.get_error_analysis_prompt(),
            "accessibility": VisionAnalyzer.get_accessibility_prompt(),
            "text": VisionAnalyzer.get_text_extraction_prompt(),
        }
        prompt = prompts.get(analysis_type, prompts["ui"])

    # Build the vision content blocks
    _content_blocks = analyzer.build_vision_prompt(prompt, image_path)

    # Return a placeholder result - actual API call is done by the caller
    return ScreenshotResult(
        image_path=str(image_path),
        analysis="",  # To be filled by API response
        model_used=model.value,
        metadata={
            "analysis_type": analysis_type,
            "prompt_used": prompt[:100] + "..." if len(prompt) > 100 else prompt,
        },
    )


async def capture_error_screenshot(
    url: str,
    error_element: str | None = None,
    output_path: str | Path | None = None,
) -> str:
    """Capture a screenshot of an error state for analysis.

    Args:
        url: URL showing the error
        error_element: CSS selector for the error element (optional)
        output_path: Where to save the screenshot (auto-generated if not provided)

    Returns:
        Path to the captured screenshot

    Note: Requires puppeteer or browser automation MCP server to be available.
    This function returns the path where the screenshot should be saved.
    """
    from datetime import datetime

    # Generate output path if not provided
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f".claude/state/screenshots/error_{timestamp}.png"

    # Create directory if needed
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Return the path - actual capture is done by the caller via puppeteer MCP
    return str(output_path)


async def visual_diff(
    before: str | Path,
    after: str | Path,
    model: ModelTier = ModelTier.SONNET,
) -> VisualDiff:
    """Compare two screenshots for visual differences.

    Args:
        before: Path to the "before" screenshot
        after: Path to the "after" screenshot
        model: Model to use for analysis

    Returns:
        VisualDiff with comparison results

    Note: This function builds the comparison prompt but does not call the API directly.
    The caller should use the returned content blocks with Claude's API.
    """
    analyzer = VisionAnalyzer(default_model=model)

    # Build the comparison content blocks
    _content_blocks = analyzer.build_comparison_prompt(
        VisionAnalyzer.get_visual_diff_prompt(),
        before,
        after,
    )

    # Return a placeholder result - actual API call is done by the caller
    return VisualDiff(
        before_path=str(before),
        after_path=str(after),
    )


async def analyze_responsive_layout(
    base_url: str,
    viewports: list[str] | None = None,
    model: ModelTier = ModelTier.SONNET,
) -> dict[str, ScreenshotResult]:
    """Analyze a page at multiple viewport sizes.

    Args:
        base_url: URL to analyze
        viewports: List of viewport names ("mobile", "tablet", "desktop", "wide")
        model: Model to use for analysis

    Returns:
        Dict mapping viewport names to analysis results

    Note: Requires browser automation to capture screenshots at each viewport.
    """
    if viewports is None:
        viewports = ["mobile", "tablet", "desktop"]

    results = {}
    for viewport in viewports:
        if viewport in VisionAnalyzer.VIEWPORT_SIZES:
            # Placeholder - actual capture and analysis done by caller
            results[viewport] = ScreenshotResult(
                image_path=f"screenshot_{viewport}.png",
                analysis="",
                model_used=model.value,
                metadata={
                    "viewport": viewport,
                    "size": VisionAnalyzer.VIEWPORT_SIZES[viewport],
                    "url": base_url,
                },
            )

    return results
