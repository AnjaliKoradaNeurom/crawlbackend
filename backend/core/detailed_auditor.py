"""
Detailed auditor for generating comprehensive website audit results
"""

import logging
from typing import Dict, Any, List, Optional
from models.schemas import AuditDetails, DetailedRecommendation

logger = logging.getLogger(__name__)

class DetailedAuditor:
    """
    Generates detailed audit results for various website aspects based on real-time analysis
    """
    
    def __init__(self):
        logger.info("🔍 Detailed auditor initialized")
    
    def _create_error_audit(self, error_message: str = "Analysis failed. Website could not be crawled.") -> AuditDetails:
        """Create a standardized error audit result for failed crawls"""
        return AuditDetails(
            status="error",
            details=error_message,
            recommendations=[]
        )
    
    def generate_crawlability_details(self, features: Dict[str, Any], crawl_result: Optional[Dict] = None, analysis_failed: bool = False) -> AuditDetails:
        """Generate crawlability audit details based on actual crawl data"""
        try:
            # Check if analysis failed (score=0, confidence=0)
            if analysis_failed:
                return self._create_error_audit("Analysis failed. Website could not be crawled.")
            
            status_code = features.get('status_code', 200)
            page_load_time = features.get('page_load_time', 0)
            html_size = features.get('html_size', 0)
            word_count = features.get('word_count', 0)
            compression_enabled = features.get('compression_enabled', False)
            
            issues = []
            recommendations = []
            
            # Analyze HTTP status
            if status_code != 200:
                issues.append(f"HTTP {status_code} status code")
                recommendations.append(DetailedRecommendation(
                    title="Fix HTTP Status Code",
                    description=f"Website returns HTTP {status_code}. This prevents search engines from accessing your content.",
                    impact="Critical - Search engines cannot index inaccessible pages",
                    effort="High - Requires server configuration or content fixes",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/http-network-errors",
                        f"https://httpstatuses.com/{status_code}"
                    ]
                ))
            
            # Analyze page load time
            if page_load_time > 5.0:
                issues.append(f"Very slow load time ({page_load_time:.1f}s)")
                recommendations.append(DetailedRecommendation(
                    title="Critical Speed Optimization Needed",
                    description=f"Page loads in {page_load_time:.1f} seconds, which is extremely slow. Search engines may crawl less frequently.",
                    impact="High - Severely impacts crawl budget and user experience",
                    effort="High - Comprehensive performance optimization required",
                    priority="high",
                    resources=[
                        "https://developers.google.com/speed/docs/insights/rules",
                        "https://web.dev/performance/"
                    ]
                ))
            elif page_load_time > 3.0:
                issues.append(f"Slow load time ({page_load_time:.1f}s)")
                recommendations.append(DetailedRecommendation(
                    title="Improve Page Load Speed",
                    description=f"Page loads in {page_load_time:.1f} seconds. Optimize for faster loading to improve crawlability.",
                    impact="Medium - May affect crawl frequency",
                    effort="Medium - Image optimization, caching, CDN implementation",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/speed/docs/insights/rules"
                    ]
                ))
            
            # Analyze HTML size
            if html_size > 2 * 1024 * 1024:  # 2MB
                issues.append(f"Very large HTML size ({html_size / 1024 / 1024:.1f}MB)")
                recommendations.append(DetailedRecommendation(
                    title="Reduce HTML Size Significantly",
                    description=f"HTML size is {html_size / 1024 / 1024:.1f}MB, which is extremely large and may cause crawling issues.",
                    impact="High - Large pages may timeout during crawling",
                    effort="High - Code refactoring and content optimization",
                    priority="high",
                    resources=[
                        "https://developers.google.com/speed/docs/insights/MinifyHTML"
                    ]
                ))
            elif html_size > 1024 * 1024:  # 1MB
                issues.append(f"Large HTML size ({html_size / 1024:.0f}KB)")
                recommendations.append(DetailedRecommendation(
                    title="Optimize HTML Size",
                    description=f"HTML size is {html_size / 1024:.0f}KB. Consider reducing for faster crawling.",
                    impact="Medium - May slow down crawling process",
                    effort="Medium - Remove unnecessary code, optimize content",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/speed/docs/insights/MinifyHTML"
                    ]
                ))
            
            # Analyze content quality
            if word_count < 100:
                issues.append(f"Very thin content ({word_count} words)")
                recommendations.append(DetailedRecommendation(
                    title="Add Substantial Content",
                    description=f"Page has only {word_count} words. Search engines prefer pages with substantial, valuable content.",
                    impact="High - Thin content may not be indexed or ranked well",
                    effort="High - Content creation and optimization",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/fundamentals/creating-helpful-content"
                    ]
                ))
            elif word_count < 300:
                issues.append(f"Limited content ({word_count} words)")
                recommendations.append(DetailedRecommendation(
                    title="Expand Content",
                    description=f"Page has {word_count} words. Consider adding more valuable content for better SEO.",
                    impact="Medium - More content can improve search visibility",
                    effort="Medium - Content expansion and optimization",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/search/docs/fundamentals/creating-helpful-content"
                    ]
                ))
            
            # Analyze compression
            if not compression_enabled and html_size > 50000:  # 50KB
                issues.append("No compression enabled")
                recommendations.append(DetailedRecommendation(
                    title="Enable Compression",
                    description="Enable gzip or brotli compression to reduce transfer size and improve crawling efficiency.",
                    impact="Medium - Faster page delivery improves crawl efficiency",
                    effort="Low - Server configuration change",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/speed/docs/insights/EnableCompression"
                    ]
                ))
            
            # Determine overall status
            if any("HTTP" in issue for issue in issues) or any("Very" in issue for issue in issues):
                status = "fail"
            elif issues:
                status = "warning"
            else:
                status = "pass"
            
            # Create details message
            if issues:
                details = f"Crawlability issues detected: {', '.join(issues)}."
            else:
                details = f"Website is crawlable. Load time: {page_load_time:.1f}s, Size: {html_size / 1024:.0f}KB, Content: {word_count} words."
            
            return AuditDetails(
                status=status,
                details=details,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error generating crawlability details: {e}")
            return self._create_error_audit("Unable to analyze crawlability due to technical error.")
    
    def generate_indexability_details(self, features: Dict[str, Any], analysis_failed: bool = False) -> AuditDetails:
        """Generate indexability audit details based on actual meta robots and robots.txt analysis"""
        try:
            if analysis_failed:
                return self._create_error_audit("Analysis failed. Website could not be crawled.")
            
            meta_robots_noindex = features.get('meta_robots_noindex', False)
            robots_txt_blocks_crawling = features.get('robots_txt_blocks_crawling', False)
            robots_txt_exists = features.get('robots_txt_exists', False)
            status_code = features.get('status_code', 200)
            canonical_tag_present = features.get('canonical_tag_present', False)
            
            issues = []
            recommendations = []
            
            # Check meta robots noindex
            if meta_robots_noindex:
                issues.append("Meta robots noindex directive blocks indexing")
                recommendations.append(DetailedRecommendation(
                    title="Remove Noindex Directive",
                    description="Page has meta robots noindex tag preventing search engine indexing.",
                    impact="Critical - Page will not appear in search results",
                    effort="Low - Remove or modify meta robots tag",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag"
                    ]
                ))
            
            # Check robots.txt blocking
            if robots_txt_blocks_crawling:
                issues.append("Robots.txt blocks crawling")
                recommendations.append(DetailedRecommendation(
                    title="Update Robots.txt Configuration",
                    description="Robots.txt file is blocking search engine access to this page.",
                    impact="Critical - Search engines cannot crawl blocked content",
                    effort="Low - Edit robots.txt file",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt"
                    ]
                ))
            
            # Check HTTP status for indexability
            if status_code == 404:
                issues.append("Page not found (404)")
                recommendations.append(DetailedRecommendation(
                    title="Fix 404 Error",
                    description="Page returns 404 Not Found, making it unindexable.",
                    impact="Critical - 404 pages cannot be indexed",
                    effort="High - Fix broken links or restore content",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/http-network-errors"
                    ]
                ))
            elif status_code == 301 or status_code == 302:
                issues.append(f"Page redirects ({status_code})")
                recommendations.append(DetailedRecommendation(
                    title="Review Redirect Configuration",
                    description=f"Page returns {status_code} redirect. Ensure this is intentional for SEO.",
                    impact="Medium - Redirects may affect indexing",
                    effort="Medium - Review redirect strategy",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/301-redirects"
                    ]
                ))
            elif status_code >= 500:
                issues.append(f"Server error ({status_code})")
                recommendations.append(DetailedRecommendation(
                    title="Fix Server Error",
                    description=f"Server returns {status_code} error, preventing indexing.",
                    impact="Critical - Server errors block indexing",
                    effort="High - Server troubleshooting required",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/http-network-errors"
                    ]
                ))
            
            # Check for missing canonical (only recommend if no blocking issues)
            if not canonical_tag_present and not meta_robots_noindex and not robots_txt_blocks_crawling and status_code == 200:
                recommendations.append(DetailedRecommendation(
                    title="Add Canonical Tag",
                    description="Consider adding a canonical tag to prevent duplicate content issues.",
                    impact="Low - Helps consolidate page authority",
                    effort="Low - Add canonical link tag",
                    priority="low",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls"
                    ]
                ))
            
            # Determine status
            if any("Critical" in rec.impact for rec in recommendations):
                status = "fail"
            elif issues:
                status = "warning"
            else:
                status = "pass"
            
            # Create details
            if issues:
                details = f"Indexability issues found: {', '.join(issues)}."
            else:
                indexable_status = "indexable" if status_code == 200 and not meta_robots_noindex and not robots_txt_blocks_crawling else "may have indexing issues"
                details = f"Page is {indexable_status}. Status: {status_code}, Robots.txt: {'exists' if robots_txt_exists else 'not found'}."
            
            return AuditDetails(
                status=status,
                details=details,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error generating indexability details: {e}")
            return self._create_error_audit("Unable to analyze indexability due to technical error.")
    
    def generate_site_structure_details(self, features: Dict[str, Any], analysis_failed: bool = False) -> AuditDetails:
        """Generate site structure audit details based on actual HTML heading and link analysis"""
        try:
            if analysis_failed:
                return self._create_error_audit("Analysis failed. Website could not be crawled.")
            
            h1_count = features.get('h1_count', 0)
            h2_count = features.get('h2_count', 0)
            h3_count = features.get('h3_count', 0)
            internal_links_count = features.get('internal_links_count', 0)
            external_links_count = features.get('external_links_count', 0)
            h1_text = features.get('h1_text', '')
            
            issues = []
            recommendations = []
            
            # Analyze H1 structure
            if h1_count == 0:
                issues.append("Missing H1 heading")
                recommendations.append(DetailedRecommendation(
                    title="Add H1 Heading",
                    description="Page is missing an H1 heading tag, which is important for SEO and accessibility.",
                    impact="High - H1 helps search engines understand page topic",
                    effort="Low - Add H1 tag with descriptive content",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/appearance/structured-data"
                    ]
                ))
            elif h1_count > 1:
                issues.append(f"Multiple H1 headings ({h1_count})")
                recommendations.append(DetailedRecommendation(
                    title="Use Single H1 Tag",
                    description=f"Page has {h1_count} H1 tags. Use only one H1 per page for better SEO structure.",
                    impact="Medium - Multiple H1s can confuse search engines",
                    effort="Low - Consolidate into one H1, use H2-H6 for subheadings",
                    priority="medium",
                    resources=[
                        "https://www.w3.org/WAI/tutorials/page-structure/headings/"
                    ]
                ))
            elif len(h1_text.strip()) < 10:
                issues.append("H1 text too short")
                recommendations.append(DetailedRecommendation(
                    title="Improve H1 Content",
                    description=f"H1 text is very short ('{h1_text[:50]}...'). Make it more descriptive.",
                    impact="Medium - Descriptive H1s improve SEO",
                    effort="Low - Expand H1 text to be more descriptive",
                    priority="medium",
                    resources=[
                        "https://moz.com/learn/seo/title-tag"
                    ]
                ))
            
            # Analyze heading hierarchy
            if h3_count > 0 and h2_count == 0:
                issues.append("Poor heading hierarchy (H3 without H2)")
                recommendations.append(DetailedRecommendation(
                    title="Fix Heading Hierarchy",
                    description="Page uses H3 tags without H2 tags, breaking proper heading structure.",
                    impact="Medium - Proper hierarchy improves accessibility and SEO",
                    effort="Low - Restructure headings in logical order",
                    priority="medium",
                    resources=[
                        "https://www.w3.org/WAI/tutorials/page-structure/headings/"
                    ]
                ))
            
            # Analyze internal linking
            if internal_links_count == 0:
                issues.append("No internal links")
                recommendations.append(DetailedRecommendation(
                    title="Add Internal Links",
                    description="Page has no internal links, missing opportunities for better site navigation and SEO.",
                    impact="High - Internal links help search engines discover content",
                    effort="Medium - Add contextual links to related pages",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/links-crawlable"
                    ]
                ))
            elif internal_links_count < 3:
                issues.append(f"Limited internal linking ({internal_links_count} links)")
                recommendations.append(DetailedRecommendation(
                    title="Improve Internal Linking",
                    description=f"Page has only {internal_links_count} internal links. Add more to improve navigation and SEO.",
                    impact="Medium - More internal links improve site structure",
                    effort="Medium - Add contextual internal links",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/links-crawlable"
                    ]
                ))
            elif internal_links_count > 100:
                issues.append(f"Too many internal links ({internal_links_count})")
                recommendations.append(DetailedRecommendation(
                    title="Reduce Internal Links",
                    description=f"Page has {internal_links_count} internal links, which may dilute link equity.",
                    impact="Low - Too many links can reduce individual link value",
                    effort="Medium - Prioritize most important links",
                    priority="low",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/links-crawlable"
                    ]
                ))
            
            # Analyze external linking
            if external_links_count > 50:
                recommendations.append(DetailedRecommendation(
                    title="Review External Links",
                    description=f"Page has {external_links_count} external links. Ensure they're all necessary and valuable.",
                    impact="Low - Too many external links may affect user experience",
                    effort="Low - Review and remove unnecessary external links",
                    priority="low",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/links-crawlable"
                    ]
                ))
            
            # Determine status
            critical_issues = ["Missing H1", "No internal links"]
            if any(issue for issue in issues if any(critical in issue for critical in critical_issues)):
                status = "fail"
            elif issues:
                status = "warning"
            else:
                status = "pass"
            
            # Create details
            if issues:
                details = f"Site structure issues: {', '.join(issues)}."
            else:
                details = f"Good site structure. H1: {h1_count}, H2: {h2_count}, H3: {h3_count}, Internal links: {internal_links_count}, External links: {external_links_count}."
            
            return AuditDetails(
                status=status,
                details=details,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error generating site structure details: {e}")
            return self._create_error_audit("Unable to analyze site structure due to technical error.")
    
    def generate_robots_txt_details(self, features: Dict[str, Any], analysis_failed: bool = False) -> AuditDetails:
        """Generate robots.txt audit details based on actual robots.txt analysis"""
        try:
            if analysis_failed:
                return self._create_error_audit("Analysis failed. Website could not be crawled.")
            
            robots_txt_exists = features.get('robots_txt_exists', False)
            robots_txt_blocks_crawling = features.get('robots_txt_blocks_crawling', False)
            sitemap_exists = features.get('sitemap_exists', False)
            
            issues = []
            recommendations = []
            
            if not robots_txt_exists:
                recommendations.append(DetailedRecommendation(
                    title="Create Robots.txt File",
                    description="No robots.txt file found. Adding one helps guide search engine crawling behavior.",
                    impact="Low - Helps provide crawling instructions to search engines",
                    effort="Low - Create and upload robots.txt file",
                    priority="low",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt",
                        "https://www.robotstxt.org/"
                    ]
                ))
                status = "warning"
                details = "No robots.txt file found. Consider adding one to guide search engine crawling."
            elif robots_txt_blocks_crawling:
                issues.append("Robots.txt blocks crawling")
                recommendations.append(DetailedRecommendation(
                    title="Update Robots.txt Directives",
                    description="Robots.txt file is blocking search engine access to this page or important resources.",
                    impact="Critical - Blocked content cannot be indexed",
                    effort="Low - Edit robots.txt file to allow crawling",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt"
                    ]
                ))
                status = "fail"
                details = "Robots.txt is blocking search engine crawling of this page."
            else:
                # Robots.txt exists and allows crawling
                if not sitemap_exists:
                    recommendations.append(DetailedRecommendation(
                        title="Add Sitemap Reference to Robots.txt",
                        description="Consider adding your XML sitemap URL to robots.txt for better crawl discovery.",
                        impact="Low - Helps search engines find your sitemap",
                        effort="Low - Add sitemap line to robots.txt",
                        priority="low",
                        resources=[
                            "https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap"
                        ]
                    ))
                
                status = "pass"
                details = f"Robots.txt exists and allows proper crawling. {'Sitemap referenced.' if sitemap_exists else 'No sitemap reference found.'}"
            
            return AuditDetails(
                status=status,
                details=details,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error generating robots.txt details: {e}")
            return self._create_error_audit("Unable to analyze robots.txt due to technical error.")
    
    def generate_canonical_issues_details(self, features: Dict[str, Any], analysis_failed: bool = False) -> AuditDetails:
        """Generate canonical issues audit details based on actual canonical tag analysis"""
        try:
            if analysis_failed:
                return self._create_error_audit("Analysis failed. Website could not be crawled.")
            
            canonical_tag_present = features.get('canonical_tag_present', False)
            url = features.get('url', '')
            
            recommendations = []
            
            if not canonical_tag_present:
                recommendations.append(DetailedRecommendation(
                    title="Add Canonical Tag",
                    description="Page is missing a canonical link tag. This helps prevent duplicate content issues and consolidates page authority.",
                    impact="Medium - Prevents duplicate content penalties and consolidates SEO value",
                    effort="Low - Add canonical link tag to HTML head section",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls"
                    ]
                ))
                status = "warning"
                details = "No canonical tag found. Adding one helps prevent duplicate content issues and consolidates page authority."
            else:
                # Canonical tag exists - could add more specific checks here
                status = "pass"
                details = "Canonical tag is present, helping prevent duplicate content issues."
                
                # Optional: Add recommendation for HTTPS canonical if URL is HTTP
                if url.startswith('http://'):
                    recommendations.append(DetailedRecommendation(
                        title="Use HTTPS in Canonical URL",
                        description="Ensure your canonical tag points to the HTTPS version of the page for better SEO.",
                        impact="Low - HTTPS canonical URLs are preferred",
                        effort="Low - Update canonical tag to use HTTPS",
                        priority="low",
                        resources=[
                            "https://developers.google.com/search/docs/crawling-indexing/https"
                        ]
                    ))
            
            return AuditDetails(
                status=status,
                details=details,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error generating canonical issues details: {e}")
            return self._create_error_audit("Unable to analyze canonical issues due to technical error.")
    
    def generate_core_web_vitals_details(self, features: Dict[str, Any], analysis_failed: bool = False) -> AuditDetails:
        """Generate Core Web Vitals audit details based on actual performance metrics"""
        try:
            if analysis_failed:
                return self._create_error_audit("Analysis failed. Website could not be crawled.")
            
            page_load_time = features.get('page_load_time', 0)
            html_size = features.get('html_size', 0)
            images_count = features.get('images_count', 0)
            lazy_loading_images = features.get('lazy_loading_images', 0)
            external_scripts_count = features.get('external_scripts_count', 0)
            compression_enabled = features.get('compression_enabled', False)
            
            issues = []
            recommendations = []
            
            # Analyze LCP (Largest Contentful Paint) - approximated from load time
            if page_load_time > 4.0:
                issues.append(f"Poor LCP (estimated {page_load_time:.1f}s)")
                recommendations.append(DetailedRecommendation(
                    title="Improve Largest Contentful Paint (LCP)",
                    description=f"Page load time of {page_load_time:.1f}s indicates poor LCP. Target under 2.5s for good user experience.",
                    impact="Critical - Poor LCP affects search rankings and user experience",
                    effort="High - Optimize images, reduce server response time, eliminate render-blocking resources",
                    priority="high",
                    resources=[
                        "https://web.dev/lcp/",
                        "https://developers.google.com/speed/docs/insights/LCP"
                    ]
                ))
            elif page_load_time > 2.5:
                issues.append(f"Needs improvement LCP (estimated {page_load_time:.1f}s)")
                recommendations.append(DetailedRecommendation(
                    title="Optimize Largest Contentful Paint (LCP)",
                    description=f"Page load time of {page_load_time:.1f}s needs improvement. Target under 2.5s.",
                    impact="High - LCP affects Core Web Vitals score",
                    effort="Medium - Image optimization, caching improvements",
                    priority="high",
                    resources=[
                        "https://web.dev/lcp/"
                    ]
                ))
            
            # Analyze resource optimization
            if html_size > 1024 * 1024 and not compression_enabled:  # 1MB without compression
                issues.append(f"Large uncompressed resources ({html_size / 1024 / 1024:.1f}MB)")
                recommendations.append(DetailedRecommendation(
                    title="Enable Compression and Optimize Resources",
                    description=f"Page size is {html_size / 1024 / 1024:.1f}MB without compression. This severely impacts loading performance.",
                    impact="High - Large resources slow down all Core Web Vitals",
                    effort="Medium - Enable compression, optimize images and code",
                    priority="high",
                    resources=[
                        "https://developers.google.com/speed/docs/insights/EnableCompression"
                    ]
                ))
            
            # Analyze image optimization
            if images_count > 0:
                lazy_percentage = (lazy_loading_images / images_count) * 100 if images_count > 0 else 0
                if lazy_percentage < 50 and images_count > 5:
                    issues.append(f"Poor image optimization ({lazy_percentage:.0f}% lazy loaded)")
                    recommendations.append(DetailedRecommendation(
                        title="Implement Lazy Loading for Images",
                        description=f"Only {lazy_percentage:.0f}% of {images_count} images use lazy loading. This can improve LCP and CLS.",
                        impact="Medium - Lazy loading improves initial page load",
                        effort="Low - Add loading='lazy' attribute to images",
                        priority="medium",
                        resources=[
                            "https://web.dev/lazy-loading-images/"
                        ]
                    ))
            
            # Analyze external scripts
            if external_scripts_count > 10:
                issues.append(f"Too many external scripts ({external_scripts_count})")
                recommendations.append(DetailedRecommendation(
                    title="Reduce External Scripts",
                    description=f"Page loads {external_scripts_count} external scripts, which can impact performance.",
                    impact="Medium - External scripts can block rendering and affect FID",
                    effort="Medium - Audit and remove unnecessary scripts, use async/defer",
                    priority="medium",
                    resources=[
                        "https://web.dev/efficiently-load-third-party-javascript/"
                    ]
                ))
            
            # Determine status based on performance
            if page_load_time > 4.0 or any("Critical" in rec.impact for rec in recommendations):
                status = "fail"
            elif page_load_time > 2.5 or issues:
                status = "warning"
            else:
                status = "pass"
            
            # Create details
            if issues:
                details = f"Core Web Vitals issues: {', '.join(issues)}."
            else:
                details = f"Good Core Web Vitals performance. Load time: {page_load_time:.1f}s, Size: {html_size / 1024:.0f}KB."
            
            return AuditDetails(
                status=status,
                details=details,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error generating Core Web Vitals details: {e}")
            return self._create_error_audit("Unable to analyze Core Web Vitals due to technical error.")
    
    def generate_mobile_friendliness_details(self, features: Dict[str, Any], analysis_failed: bool = False) -> AuditDetails:
        """Generate mobile friendliness audit details based on actual viewport and responsive analysis"""
        try:
            if analysis_failed:
                return self._create_error_audit("Analysis failed. Website could not be crawled.")
            
            viewport_configured = features.get('viewport_configured', False)
            mobile_friendly = features.get('mobile_friendly', False)
            images_count = features.get('images_count', 0)
            
            issues = []
            recommendations = []
            
            # Check viewport configuration
            if not viewport_configured:
                issues.append("Missing viewport meta tag")
                recommendations.append(DetailedRecommendation(
                    title="Add Viewport Meta Tag",
                    description="Page is missing the viewport meta tag, which is essential for mobile responsiveness.",
                    impact="Critical - Without viewport tag, page won't display properly on mobile devices",
                    effort="Low - Add viewport meta tag to HTML head",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing"
                    ]
                ))
            
            # Check mobile friendliness
            if not mobile_friendly:
                issues.append("Not mobile-friendly")
                recommendations.append(DetailedRecommendation(
                    title="Implement Responsive Design",
                    description="Page is not mobile-friendly. With mobile-first indexing, this significantly impacts SEO.",
                    impact="Critical - Mobile-unfriendly sites rank poorly in mobile search",
                    effort="High - Implement responsive CSS and mobile-friendly design",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/mobile-sites/",
                        "https://web.dev/responsive-web-design-basics/"
                    ]
                ))
            
            # Check for responsive images if mobile-friendly but has images
            if mobile_friendly and images_count > 0:
                # This would need more detailed image analysis in a real implementation
                recommendations.append(DetailedRecommendation(
                    title="Optimize Images for Mobile",
                    description=f"Ensure all {images_count} images are optimized for mobile devices with appropriate sizes and formats.",
                    impact="Medium - Optimized images improve mobile performance",
                    effort="Medium - Implement responsive images with srcset",
                    priority="medium",
                    resources=[
                        "https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images"
                    ]
                ))
            
            # Determine status
            if not viewport_configured or not mobile_friendly:
                status = "fail"
            elif issues:
                status = "warning"
            else:
                status = "pass"
            
            # Create details
            if issues:
                details = f"Mobile friendliness issues: {', '.join(issues)}."
            else:
                details = f"Page is mobile-friendly with proper viewport configuration. {images_count} images detected."
            
            return AuditDetails(
                status=status,
                details=details,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error generating mobile friendliness details: {e}")
            return self._create_error_audit("Unable to analyze mobile friendliness due to technical error.")
    
    def generate_https_security_details(self, features: Dict[str, Any], analysis_failed: bool = False) -> AuditDetails:
        """Generate HTTPS security audit details based on actual security analysis"""
        try:
            if analysis_failed:
                return self._create_error_audit("Analysis failed. Website could not be crawled.")
            
            https_enabled = features.get('https_enabled', False)
            ssl_certificate_valid = features.get('ssl_certificate_valid', True)
            mixed_content_issues = features.get('mixed_content_issues', 0)
            security_headers_count = features.get('security_headers_count', 0)
            external_scripts_count = features.get('external_scripts_count', 0)
            
            issues = []
            recommendations = []
            
            # Check HTTPS
            if not https_enabled:
                issues.append("HTTPS not enabled")
                recommendations.append(DetailedRecommendation(
                    title="Enable HTTPS",
                    description="Website is not using HTTPS. This is a ranking factor and security requirement.",
                    impact="Critical - HTTPS is required for modern web security and SEO",
                    effort="Medium - Obtain SSL certificate and configure server",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/https",
                        "https://letsencrypt.org/"
                    ]
                ))
            
            # Check SSL certificate validity
            if https_enabled and not ssl_certificate_valid:
                issues.append("Invalid SSL certificate")
                recommendations.append(DetailedRecommendation(
                    title="Fix SSL Certificate",
                    description="SSL certificate is invalid or expired, causing security warnings.",
                    impact="Critical - Invalid certificates cause browser warnings and trust issues",
                    effort="Medium - Renew or fix SSL certificate configuration",
                    priority="high",
                    resources=[
                        "https://developers.google.com/web/fundamentals/security/encrypt-in-transit/enable-https"
                    ]
                ))
            
            # Check mixed content
            if mixed_content_issues > 0:
                issues.append(f"{mixed_content_issues} mixed content issues")
                recommendations.append(DetailedRecommendation(
                    title="Fix Mixed Content Issues",
                    description=f"Found {mixed_content_issues} mixed content issues (HTTP resources on HTTPS page).",
                    impact="High - Mixed content reduces security and may cause browser warnings",
                    effort="Medium - Update all resource URLs to use HTTPS",
                    priority="high",
                    resources=[
                        "https://developers.google.com/web/fundamentals/security/prevent-mixed-content"
                    ]
                ))
            
            # Check security headers
            if security_headers_count < 3:
                issues.append(f"Missing security headers ({security_headers_count}/7)")
                recommendations.append(DetailedRecommendation(
                    title="Add Security Headers",
                    description=f"Only {security_headers_count} of 7 important security headers are present.",
                    impact="Medium - Security headers protect against various attacks",
                    effort="Low - Configure server to send security headers",
                    priority="medium",
                    resources=[
                        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#Security",
                        "https://securityheaders.com/"
                    ]
                ))
            
            # Check external script security
            if external_scripts_count > 5 and https_enabled:
                recommendations.append(DetailedRecommendation(
                    title="Review External Script Security",
                    description=f"Page loads {external_scripts_count} external scripts. Ensure they're from trusted sources.",
                    impact="Medium - External scripts can introduce security vulnerabilities",
                    effort="Medium - Audit external scripts, implement CSP",
                    priority="medium",
                    resources=[
                        "https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP"
                    ]
                ))
            
            # Determine status
            if not https_enabled or not ssl_certificate_valid or mixed_content_issues > 0:
                status = "fail"
            elif security_headers_count < 3:
                status = "warning"
            else:
                status = "pass"
            
            # Create details
            if issues:
                details = f"Security issues detected: {', '.join(issues)}."
            else:
                details = f"Good security implementation. HTTPS enabled, {security_headers_count} security headers present."
            
            return AuditDetails(
                status=status,
                details=details,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error generating HTTPS security details: {e}")
            return self._create_error_audit("Unable to analyze HTTPS security due to technical error.")
    
    def generate_broken_links_details(self, features: Dict[str, Any], analysis_failed: bool = False) -> AuditDetails:
        """Generate broken links audit details based on actual link analysis"""
        try:
            if analysis_failed:
                return self._create_error_audit("Analysis failed. Website could not be crawled.")
            
            broken_links_count = features.get('broken_links_count', 0)
            internal_links_count = features.get('internal_links_count', 0)
            external_links_count = features.get('external_links_count', 0)
            
            recommendations = []
            
            if broken_links_count > 0:
                recommendations.append(DetailedRecommendation(
                    title="Fix Broken Links",
                    description=f"Found {broken_links_count} broken links that return errors or don't exist.",
                    impact="Medium - Broken links hurt user experience and waste crawl budget",
                    effort="Medium - Check and update or remove broken links",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/search/docs/crawling-indexing/links-crawlable"
                    ]
                ))
                status = "fail"
                details = f"Found {broken_links_count} broken links out of {internal_links_count + external_links_count} total links."
            else:
                status = "pass"
                total_links = internal_links_count + external_links_count
                if total_links > 0:
                    details = f"No broken links detected. All {total_links} links ({internal_links_count} internal, {external_links_count} external) are working properly."
                else:
                    details = "No links found on the page to analyze."
                    recommendations.append(DetailedRecommendation(
                        title="Add Internal Links",
                        description="Page has no links. Adding internal links improves navigation and SEO.",
                        impact="Medium - Internal links help search engines discover content",
                        effort="Medium - Add contextual links to related pages",
                        priority="medium",
                        resources=[
                            "https://developers.google.com/search/docs/crawling-indexing/links-crawlable"
                        ]
                    ))
            
            return AuditDetails(
                status=status,
                details=details,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error generating broken links details: {e}")
            return self._create_error_audit("Unable to analyze broken links due to technical error.")
    
    def generate_meta_tags_headers_schema_details(self, features: Dict[str, Any], analysis_failed: bool = False) -> AuditDetails:
        """Generate meta tags, headers, and schema audit details based on actual HTML analysis"""
        try:
            if analysis_failed:
                return self._create_error_audit("Analysis failed. Website could not be crawled.")
            
            title_tag_present = features.get('title_tag_present', False)
            title_length = features.get('title_length', 0)
            meta_description_present = features.get('meta_description_present', False)
            meta_description_length = features.get('meta_description_length', 0)
            structured_data_present = features.get('structured_data_present', False)
            open_graph_present = features.get('open_graph_present', False)
            open_graph_tags_count = features.get('open_graph_tags_count', 0)
            twitter_cards_present = features.get('twitter_cards_present', False)
            lang_attribute_present = features.get('lang_attribute_present', False)
            charset_declared = features.get('charset_declared', False)
            
            issues = []
            recommendations = []
            
            # Analyze title tag
            if not title_tag_present:
                issues.append("Missing title tag")
                recommendations.append(DetailedRecommendation(
                    title="Add Title Tag",
                    description="Page is missing a title tag, which is critical for SEO and search result display.",
                    impact="Critical - Title tags are essential for search engine rankings",
                    effort="Low - Add descriptive title tag to HTML head",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/appearance/title-link"
                    ]
                ))
            elif title_length < 30:
                issues.append(f"Title too short ({title_length} characters)")
                recommendations.append(DetailedRecommendation(
                    title="Expand Title Tag",
                    description=f"Title is only {title_length} characters. Aim for 30-60 characters for optimal display.",
                    impact="Medium - Short titles may not be descriptive enough",
                    effort="Low - Expand title with more descriptive content",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/search/docs/appearance/title-link"
                    ]
                ))
            elif title_length > 60:
                issues.append(f"Title too long ({title_length} characters)")
                recommendations.append(DetailedRecommendation(
                    title="Shorten Title Tag",
                    description=f"Title is {title_length} characters, which may be truncated in search results.",
                    impact="Medium - Long titles get cut off in search results",
                    effort="Low - Shorten title to 30-60 characters",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/search/docs/appearance/title-link"
                    ]
                ))
            
            # Analyze meta description
            if not meta_description_present:
                issues.append("Missing meta description")
                recommendations.append(DetailedRecommendation(
                    title="Add Meta Description",
                    description="Page is missing a meta description, which affects search result snippets and click-through rates.",
                    impact="High - Meta descriptions influence click-through rates from search results",
                    effort="Low - Add compelling meta description tag",
                    priority="high",
                    resources=[
                        "https://developers.google.com/search/docs/appearance/snippet"
                    ]
                ))
            elif meta_description_length < 120:
                issues.append(f"Meta description too short ({meta_description_length} characters)")
                recommendations.append(DetailedRecommendation(
                    title="Expand Meta Description",
                    description=f"Meta description is only {meta_description_length} characters. Aim for 120-160 characters.",
                    impact="Medium - Short descriptions may not be compelling enough",
                    effort="Low - Expand meta description with more details",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/search/docs/appearance/snippet"
                    ]
                ))
            elif meta_description_length > 160:
                issues.append(f"Meta description too long ({meta_description_length} characters)")
                recommendations.append(DetailedRecommendation(
                    title="Shorten Meta Description",
                    description=f"Meta description is {meta_description_length} characters, which may be truncated.",
                    impact="Medium - Long descriptions get cut off in search results",
                    effort="Low - Shorten meta description to 120-160 characters",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/search/docs/appearance/snippet"
                    ]
                ))
            
            # Analyze structured data
            if not structured_data_present:
                recommendations.append(DetailedRecommendation(
                    title="Implement Structured Data",
                    description="Page lacks structured data markup, missing opportunities for rich search results.",
                    impact="Medium - Structured data can enhance search result appearance",
                    effort="Medium - Implement JSON-LD or microdata markup",
                    priority="medium",
                    resources=[
                        "https://developers.google.com/search/docs/appearance/structured-data",
                        "https://schema.org/"
                    ]
                ))
            
            # Analyze Open Graph
            if not open_graph_present:
                recommendations.append(DetailedRecommendation(
                    title="Add Open Graph Tags",
                    description="Page is missing Open Graph meta tags for better social media sharing.",
                    impact="Low - Improves appearance when shared on social media",
                    effort="Low - Add basic Open Graph meta tags",
                    priority="low",
                    resources=[
                        "https://ogp.me/",
                        "https://developers.facebook.com/docs/sharing/webmasters"
                    ]
                ))
            elif open_graph_tags_count < 4:
                recommendations.append(DetailedRecommendation(
                    title="Complete Open Graph Implementation",
                    description=f"Only {open_graph_tags_count} Open Graph tags found. Add og:title, og:description, og:image, og:url for complete implementation.",
                    impact="Low - Complete Open Graph improves social sharing",
                    effort="Low - Add missing Open Graph tags",
                    priority="low",
                    resources=[
                        "https://ogp.me/"
                    ]
                ))
            
            # Analyze Twitter Cards
            if not twitter_cards_present and open_graph_present:
                recommendations.append(DetailedRecommendation(
                    title="Add Twitter Card Tags",
                    description="Consider adding Twitter Card meta tags for optimized Twitter sharing.",
                    impact="Low - Improves appearance when shared on Twitter",
                    effort="Low - Add Twitter Card meta tags",
                    priority="low",
                    resources=[
                        "https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards"
                    ]
                ))
            
            # Analyze language and charset
            if not lang_attribute_present:
                issues.append("Missing lang attribute")
                recommendations.append(DetailedRecommendation(
                    title="Add Language Attribute",
                    description="HTML tag is missing the lang attribute, which affects accessibility and SEO.",
                    impact="Medium - Language attribute helps search engines and screen readers",
                    effort="Low - Add lang attribute to HTML tag",
                    priority="medium",
                    resources=[
                        "https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/lang"
                    ]
                ))
            
            if not charset_declared:
                issues.append("Missing charset declaration")
                recommendations.append(DetailedRecommendation(
                    title="Declare Character Encoding",
                    description="Page is missing charset declaration, which can cause text encoding issues.",
                    impact="Medium - Prevents character encoding problems",
                    effort="Low - Add charset meta tag",
                    priority="medium",
                    resources=[
                        "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta#attr-charset"
                    ]
                ))
            
            # Determine status
            critical_issues = ["Missing title tag", "Missing meta description"]
            if any(issue for issue in issues if any(critical in issue for critical in critical_issues)):
                status = "fail"
            elif issues:
                status = "warning"
            else:
                status = "pass"
            
            # Create details
            if issues:
                details = f"Meta tags and schema issues: {', '.join(issues)}."
            else:
                details = f"Good meta implementation. Title: {title_length} chars, Description: {meta_description_length} chars, Structured data: {'Yes' if structured_data_present else 'No'}, Open Graph: {open_graph_tags_count} tags."
            
            return AuditDetails(
                status=status,
                details=details,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error generating meta tags details: {e}")
            return self._create_error_audit("Unable to analyze meta tags and schema due to technical error.")
