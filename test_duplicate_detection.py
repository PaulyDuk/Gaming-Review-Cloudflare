#!/usr/bin/env python
"""
Test duplicate review detection logic
"""

# Mock the Review model for testing
class MockReview:
    def __init__(self, title, slug):
        self.title = title
        self.slug = slug

# Mock the Q object for testing
class MockQ:
    def __init__(self, **kwargs):
        self.filters = kwargs
        
    def __or__(self, other):
        return MockQ(**{**self.filters, **other.filters})

def mock_filter_reviews(title, slug):
    """Mock review filtering logic"""
    existing_reviews = [
        MockReview("The Legend of Zelda: Breath of the Wild", "legend-of-zelda-breath-of-the-wild"),
        MockReview("God of War", "god-of-war"),
        MockReview("Super Mario Odyssey", "super-mario-odyssey"),
    ]
    
    # Check for case-insensitive title match or exact slug match
    for review in existing_reviews:
        if (review.title.lower() == title.lower() or 
            review.slug == slug):
            return review
    return None

def test_duplicate_detection():
    """Test the duplicate review detection logic"""
    print("Testing duplicate review detection...")
    
    test_cases = [
        # (title, expected_result)
        ("The Legend of Zelda: Breath of the Wild", "Found duplicate"),
        ("the legend of zelda: breath of the wild", "Found duplicate"),  # Case insensitive
        ("GOD OF WAR", "Found duplicate"),  # Case insensitive
        ("Super Mario Galaxy", "No duplicate"),  # Similar but different
        ("Halo Infinite", "No duplicate"),  # Completely different
    ]
    
    for title, expected in test_cases:
        from django.utils.text import slugify
        slug = slugify(title)
        
        existing = mock_filter_reviews(title, slug)
        result = "Found duplicate" if existing else "No duplicate"
        
        status = "✓" if result == expected else "✗"
        print(f"{status} '{title}' -> {result} (expected: {expected})")
        
        if existing:
            print(f"    Matched: '{existing.title}' (slug: {existing.slug})")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_duplicate_detection()
