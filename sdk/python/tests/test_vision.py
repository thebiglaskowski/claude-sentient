"""Tests for vision.py module."""

import base64
from pathlib import Path
from unittest.mock import patch

import pytest

from claude_sentient.datatypes import ModelTier
from claude_sentient.vision import (
    ScreenshotResult,
    VisualDiff,
    VisionAnalyzer,
    analyze_responsive_layout,
    analyze_screenshot,
    capture_error_screenshot,
    visual_diff,
)


class TestScreenshotResult:
    """Tests for ScreenshotResult dataclass."""

    def test_create_minimal(self):
        """Test creating result with required fields only."""
        result = ScreenshotResult(
            image_path="/path/to/image.png",
            analysis="Test analysis",
            model_used="sonnet",
        )
        assert result.image_path == "/path/to/image.png"
        assert result.analysis == "Test analysis"
        assert result.model_used == "sonnet"
        assert result.elements_found == []
        assert result.issues_detected == []
        assert result.suggestions == []
        assert result.metadata == {}

    def test_create_with_all_fields(self):
        """Test creating result with all fields."""
        result = ScreenshotResult(
            image_path="/path/to/image.png",
            analysis="Test analysis",
            model_used="opus",
            elements_found=[{"type": "button", "text": "Submit"}],
            issues_detected=["Low contrast text"],
            suggestions=["Increase font size"],
            metadata={"viewport": "mobile"},
        )
        assert len(result.elements_found) == 1
        assert result.issues_detected == ["Low contrast text"]
        assert result.suggestions == ["Increase font size"]
        assert result.metadata["viewport"] == "mobile"


class TestVisualDiff:
    """Tests for VisualDiff dataclass."""

    def test_create_minimal(self):
        """Test creating diff with required fields only."""
        diff = VisualDiff(
            before_path="/path/before.png",
            after_path="/path/after.png",
        )
        assert diff.before_path == "/path/before.png"
        assert diff.after_path == "/path/after.png"
        assert diff.differences == []
        assert diff.similarity_score == 0.0
        assert diff.summary == ""
        assert diff.regions_changed == []

    def test_create_with_all_fields(self):
        """Test creating diff with all fields."""
        diff = VisualDiff(
            before_path="/path/before.png",
            after_path="/path/after.png",
            differences=[{"location": "top-left", "type": "added"}],
            similarity_score=0.85,
            summary="Minor layout changes",
            regions_changed=[{"region": "header", "change": "color"}],
        )
        assert len(diff.differences) == 1
        assert diff.similarity_score == 0.85
        assert diff.summary == "Minor layout changes"


class TestVisionAnalyzer:
    """Tests for VisionAnalyzer class."""

    @pytest.fixture
    def analyzer(self):
        """Create a VisionAnalyzer instance."""
        return VisionAnalyzer()

    @pytest.fixture
    def temp_image(self, tmp_path: Path) -> Path:
        """Create a temporary test image."""
        # Create a minimal PNG file (1x1 pixel, red)
        # PNG header + IHDR + IDAT + IEND
        png_data = (
            b"\x89PNG\r\n\x1a\n"  # PNG signature
            b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
            b"\x08\x02\x00\x00\x00\x90wS\xde"  # 1x1, 8-bit RGB
            b"\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x03\x00\x01\x00\x05\xfe\xd4"
            b"\x00\x00\x00\x00IEND\xaeB`\x82"  # End
        )
        image_path = tmp_path / "test.png"
        image_path.write_bytes(png_data)
        return image_path

    def test_init_default_model(self):
        """Test analyzer initializes with default model."""
        analyzer = VisionAnalyzer()
        assert analyzer.default_model == ModelTier.SONNET

    def test_init_custom_model(self):
        """Test analyzer with custom default model."""
        analyzer = VisionAnalyzer(default_model=ModelTier.OPUS)
        assert analyzer.default_model == ModelTier.OPUS

    def test_viewport_sizes(self):
        """Test predefined viewport sizes."""
        assert "mobile" in VisionAnalyzer.VIEWPORT_SIZES
        assert "tablet" in VisionAnalyzer.VIEWPORT_SIZES
        assert "desktop" in VisionAnalyzer.VIEWPORT_SIZES
        assert "wide" in VisionAnalyzer.VIEWPORT_SIZES
        assert VisionAnalyzer.VIEWPORT_SIZES["mobile"] == (375, 667)

    def test_encode_image(self, analyzer: VisionAnalyzer, temp_image: Path):
        """Test encoding an image to base64."""
        encoded = analyzer.encode_image(temp_image)
        assert isinstance(encoded, str)
        # Verify it's valid base64
        decoded = base64.b64decode(encoded)
        assert decoded.startswith(b"\x89PNG")

    def test_encode_image_caching(self, analyzer: VisionAnalyzer, temp_image: Path):
        """Test that image encoding is cached."""
        encoded1 = analyzer.encode_image(temp_image)
        encoded2 = analyzer.encode_image(temp_image)
        assert encoded1 == encoded2
        assert str(temp_image.absolute()) in analyzer._screenshot_cache

    def test_encode_image_not_found(self, analyzer: VisionAnalyzer):
        """Test encoding non-existent image raises error."""
        with pytest.raises(FileNotFoundError):
            analyzer.encode_image("/nonexistent/image.png")

    def test_get_image_media_type_png(self, analyzer: VisionAnalyzer):
        """Test media type detection for PNG."""
        assert analyzer.get_image_media_type("test.png") == "image/png"
        assert analyzer.get_image_media_type("test.PNG") == "image/png"

    def test_get_image_media_type_jpeg(self, analyzer: VisionAnalyzer):
        """Test media type detection for JPEG."""
        assert analyzer.get_image_media_type("test.jpg") == "image/jpeg"
        assert analyzer.get_image_media_type("test.jpeg") == "image/jpeg"

    def test_get_image_media_type_other(self, analyzer: VisionAnalyzer):
        """Test media type detection for other formats."""
        assert analyzer.get_image_media_type("test.gif") == "image/gif"
        assert analyzer.get_image_media_type("test.webp") == "image/webp"

    def test_get_image_media_type_unknown(self, analyzer: VisionAnalyzer):
        """Test media type detection for unknown format defaults to PNG."""
        assert analyzer.get_image_media_type("test.bmp") == "image/png"

    def test_build_vision_prompt(self, analyzer: VisionAnalyzer, temp_image: Path):
        """Test building a vision API prompt."""
        content = analyzer.build_vision_prompt("Analyze this image", temp_image)

        assert len(content) == 2
        assert content[0]["type"] == "image"
        assert content[0]["source"]["type"] == "base64"
        assert content[0]["source"]["media_type"] == "image/png"
        assert content[1]["type"] == "text"
        assert content[1]["text"] == "Analyze this image"

    def test_build_comparison_prompt(self, analyzer: VisionAnalyzer, temp_image: Path):
        """Test building a comparison prompt with two images."""
        content = analyzer.build_comparison_prompt(
            "Compare these images",
            temp_image,
            temp_image,  # Using same image for test
        )

        assert len(content) == 5
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "BEFORE:"
        assert content[1]["type"] == "image"
        assert content[2]["type"] == "text"
        assert content[2]["text"] == "AFTER:"
        assert content[3]["type"] == "image"
        assert content[4]["type"] == "text"
        assert content[4]["text"] == "Compare these images"

    def test_clear_cache(self, analyzer: VisionAnalyzer, temp_image: Path):
        """Test clearing the screenshot cache."""
        analyzer.encode_image(temp_image)
        assert len(analyzer._screenshot_cache) > 0

        analyzer.clear_cache()
        assert len(analyzer._screenshot_cache) == 0

    def test_ui_analysis_prompt(self):
        """Test UI analysis prompt content."""
        prompt = VisionAnalyzer.get_ui_analysis_prompt()
        assert "Layout Issues" in prompt
        assert "Visual Design" in prompt
        assert "Accessibility" in prompt
        assert "JSON" in prompt

    def test_error_analysis_prompt(self):
        """Test error analysis prompt content."""
        prompt = VisionAnalyzer.get_error_analysis_prompt()
        assert "Error Type" in prompt
        assert "probable_cause" in prompt
        assert "JSON" in prompt

    def test_visual_diff_prompt(self):
        """Test visual diff prompt content."""
        prompt = VisionAnalyzer.get_visual_diff_prompt()
        assert "BEFORE" in prompt
        assert "AFTER" in prompt
        assert "similarity_score" in prompt

    def test_accessibility_prompt(self):
        """Test accessibility analysis prompt content."""
        prompt = VisionAnalyzer.get_accessibility_prompt()
        assert "WCAG" in prompt
        assert "Color Contrast" in prompt
        assert "Touch target" in prompt

    def test_text_extraction_prompt(self):
        """Test text extraction prompt content."""
        prompt = VisionAnalyzer.get_text_extraction_prompt()
        assert "Headings" in prompt
        assert "Navigation" in prompt
        assert "text_elements" in prompt


class TestAnalyzeScreenshot:
    """Tests for analyze_screenshot function."""

    @pytest.fixture
    def temp_image(self, tmp_path: Path) -> Path:
        """Create a temporary test image."""
        png_data = (
            b"\x89PNG\r\n\x1a\n"
            b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
            b"\x08\x02\x00\x00\x00\x90wS\xde"
            b"\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x03\x00\x01\x00\x05\xfe\xd4"
            b"\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        image_path = tmp_path / "test.png"
        image_path.write_bytes(png_data)
        return image_path

    @pytest.mark.asyncio
    async def test_analyze_screenshot_ui(self, temp_image: Path):
        """Test screenshot analysis with UI type."""
        result = await analyze_screenshot(temp_image, analysis_type="ui")

        assert result.image_path == str(temp_image)
        assert result.model_used == "sonnet"
        assert result.metadata["analysis_type"] == "ui"

    @pytest.mark.asyncio
    async def test_analyze_screenshot_error(self, temp_image: Path):
        """Test screenshot analysis with error type."""
        result = await analyze_screenshot(temp_image, analysis_type="error")

        assert result.metadata["analysis_type"] == "error"

    @pytest.mark.asyncio
    async def test_analyze_screenshot_accessibility(self, temp_image: Path):
        """Test screenshot analysis with accessibility type."""
        result = await analyze_screenshot(
            temp_image,
            analysis_type="accessibility",
            model=ModelTier.OPUS,
        )

        assert result.metadata["analysis_type"] == "accessibility"
        assert result.model_used == "opus"

    @pytest.mark.asyncio
    async def test_analyze_screenshot_custom_prompt(self, temp_image: Path):
        """Test screenshot analysis with custom prompt."""
        custom_prompt = "Find all buttons in this image"
        result = await analyze_screenshot(temp_image, prompt=custom_prompt)

        assert custom_prompt in result.metadata["prompt_used"]


class TestCaptureErrorScreenshot:
    """Tests for capture_error_screenshot function."""

    @pytest.mark.asyncio
    async def test_capture_with_auto_path(self, tmp_path: Path):
        """Test capturing with auto-generated path."""
        with patch("claude_sentient.vision.Path.mkdir"):
            path = await capture_error_screenshot("http://example.com/error")

        assert "error_" in path
        assert path.endswith(".png")

    @pytest.mark.asyncio
    async def test_capture_with_custom_path(self, tmp_path: Path):
        """Test capturing with custom output path."""
        output = tmp_path / "custom_error.png"
        path = await capture_error_screenshot(
            "http://example.com/error",
            output_path=output,
        )

        assert path == str(output)


class TestVisualDiffFunction:
    """Tests for visual_diff function."""

    @pytest.fixture
    def temp_images(self, tmp_path: Path) -> tuple[Path, Path]:
        """Create temporary test images."""
        png_data = (
            b"\x89PNG\r\n\x1a\n"
            b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
            b"\x08\x02\x00\x00\x00\x90wS\xde"
            b"\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x03\x00\x01\x00\x05\xfe\xd4"
            b"\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        before = tmp_path / "before.png"
        after = tmp_path / "after.png"
        before.write_bytes(png_data)
        after.write_bytes(png_data)
        return before, after

    @pytest.mark.asyncio
    async def test_visual_diff_returns_result(self, temp_images: tuple[Path, Path]):
        """Test visual_diff returns a VisualDiff result."""
        before, after = temp_images
        result = await visual_diff(before, after)

        assert isinstance(result, VisualDiff)
        assert result.before_path == str(before)
        assert result.after_path == str(after)

    @pytest.mark.asyncio
    async def test_visual_diff_with_model(self, temp_images: tuple[Path, Path]):
        """Test visual_diff with custom model."""
        before, after = temp_images
        result = await visual_diff(before, after, model=ModelTier.OPUS)

        assert result.before_path == str(before)
        assert result.after_path == str(after)


class TestAnalyzeResponsiveLayout:
    """Tests for analyze_responsive_layout function."""

    @pytest.mark.asyncio
    async def test_default_viewports(self):
        """Test with default viewports."""
        results = await analyze_responsive_layout("http://example.com")

        assert "mobile" in results
        assert "tablet" in results
        assert "desktop" in results
        assert "wide" not in results  # Not included by default

    @pytest.mark.asyncio
    async def test_custom_viewports(self):
        """Test with custom viewports."""
        results = await analyze_responsive_layout(
            "http://example.com",
            viewports=["mobile", "wide"],
        )

        assert "mobile" in results
        assert "wide" in results
        assert "tablet" not in results

    @pytest.mark.asyncio
    async def test_invalid_viewport_ignored(self):
        """Test that invalid viewports are ignored."""
        results = await analyze_responsive_layout(
            "http://example.com",
            viewports=["mobile", "invalid_viewport"],
        )

        assert "mobile" in results
        assert "invalid_viewport" not in results

    @pytest.mark.asyncio
    async def test_result_metadata(self):
        """Test result metadata includes viewport info."""
        results = await analyze_responsive_layout("http://example.com")

        mobile_result = results["mobile"]
        assert mobile_result.metadata["viewport"] == "mobile"
        assert mobile_result.metadata["size"] == (375, 667)
        assert mobile_result.metadata["url"] == "http://example.com"
