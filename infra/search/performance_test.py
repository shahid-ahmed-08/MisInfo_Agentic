"""
Performance and Stress Testing
Tests speed, reliability, and edge cases
"""

from dotenv import load_dotenv
load_dotenv()

from infra.search import run_search_pipeline, validate_pipeline
import time
import json

print("=" * 80)
print("PERFORMANCE & STRESS TEST SUITE")
print("=" * 80)

# 1. Component Validation
print("\n1. COMPONENT VALIDATION")
print("-" * 80)
status = validate_pipeline()
for component, working in status.items():
    icon = "✓" if working else "✗"
    print(f"  {icon} {component}: {'Working' if working else 'Failed'}")

# 2. Speed Test
print("\n\n2. SPEED TEST")
print("-" * 80)

test_queries = [
    "COVID vaccine effectiveness",
    "Climate change impacts",
    "Artificial intelligence breakthroughs"
]

total_time = 0
for i, query in enumerate(test_queries, 1):
    print(f"\n  Test {i}: {query}")
    start = time.time()
    result = run_search_pipeline(query)
    elapsed = time.time() - start
    total_time += elapsed
    
    print(f"    Time: {elapsed:.2f}s")
    print(f"    Results: {result['score']['total']}")
    print(f"    Source: {result['source']}")

avg_time = total_time / len(test_queries)
print(f"\n  Average Time: {avg_time:.2f}s")
print(f"  Total Time: {total_time:.2f}s")

# 3. Edge Cases
print("\n\n3. EDGE CASE TESTING")
print("-" * 80)

edge_cases = [
    ("Empty string", ""),
    ("Very short", "Hi"),
    ("Only URLs", "https://example.com https://test.com"),
    ("Only mentions", "@user1 @user2 @user3"),
    ("Only hashtags", "#tag1 #tag2 #tag3"),
    ("Special chars", "!@#$%^&*()"),
    ("Very long text", "This is a very long claim " * 20),
    ("Numbers only", "123 456 789"),
    ("Mixed languages", "Hello مرحبا नमस्ते 你好"),
]

print("\n  Testing edge cases...\n")
passed = 0
failed = 0

for name, text in edge_cases:
    try:
        result = run_search_pipeline(text)
        if 'claim' in result and 'score' in result:
            print(f"  ✓ {name:<20} → Claim: '{result['claim'][:40]}'")
            passed += 1
        else:
            print(f"  ✗ {name:<20} → Invalid result structure")
            failed += 1
    except Exception as e:
        print(f"  ✗ {name:<20} → Error: {str(e)[:40]}")
        failed += 1

print(f"\n  Edge Cases: {passed} passed, {failed} failed")

# 4. Consistency Test
print("\n\n4. CONSISTENCY TEST")
print("-" * 80)
print("  Testing same query 3 times for consistency...\n")

test_query = "Scientists discover water on Mars"
credibility_scores = []

for i in range(3):
    result = run_search_pipeline(test_query)
    credibility_scores.append(result['credibility'])
    print(f"  Run {i+1}: Credibility = {result['credibility']:.2f}, Results = {result['score']['total']}")

# Check if scores are consistent (within 0.1 range)
score_range = max(credibility_scores) - min(credibility_scores)
if score_range < 0.1:
    print(f"\n  ✓ Consistent (range: {score_range:.3f})")
else:
    print(f"\n  ⚠️  Inconsistent (range: {score_range:.3f})")

# 5. Error Handling
print("\n\n5. ERROR HANDLING TEST")
print("-" * 80)

error_tests = [
    ("None input", None),
    ("Dict input", {"test": "value"}),
    ("List input", ["test", "value"]),
    ("Int input", 12345),
]

print("\n  Testing invalid inputs...\n")
error_passed = 0

for name, invalid_input in error_tests:
    try:
        result = run_search_pipeline(invalid_input)
        if 'error' in result or result.get('claim', '') == '':
            print(f"  ✓ {name:<20} → Handled gracefully")
            error_passed += 1
        else:
            print(f"  ⚠️  {name:<20} → Processed unexpectedly")
    except Exception as e:
        print(f"  ✗ {name:<20} → Unhandled exception: {str(e)[:30]}")

print(f"\n  Error Handling: {error_passed}/{len(error_tests)} handled correctly")

# 6. Summary
print("\n\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print(f"\n  Component Validation: {'✓ All working' if all(status.values()) else '✗ Some failed'}")
print(f"  Average Speed: {avg_time:.2f}s per query")
print(f"  Edge Cases: {passed}/{len(edge_cases)} passed")
print(f"  Consistency: {'✓ Good' if score_range < 0.1 else '⚠️  Variable'}")
print(f"  Error Handling: {error_passed}/{len(error_tests)} handled")

# Overall grade
total_tests = len(edge_cases) + len(error_tests)
total_passed = passed + error_passed
grade_pct = (total_passed / total_tests) * 100

print(f"\n  Overall Grade: {grade_pct:.1f}%")

if grade_pct >= 90:
    print("  Rating: ⭐⭐⭐⭐⭐ Excellent")
elif grade_pct >= 75:
    print("  Rating: ⭐⭐⭐⭐ Good")
elif grade_pct >= 60:
    print("  Rating: ⭐⭐⭐ Acceptable")
else:
    print("  Rating: ⭐⭐ Needs improvement")

print("\n" + "=" * 80)
print("✓ PERFORMANCE TEST COMPLETE")
print("=" * 80)
