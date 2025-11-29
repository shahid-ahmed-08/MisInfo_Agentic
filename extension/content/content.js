// Misinfo Guardian content script
// Purpose: detect tweets as they appear, wait for sustained visibility ("dwell"),
// send text to backend for verification, and display a verdict badge.

// Attribute used to mark tweets we have processed (or queued for processing)
const PROCESSED_ATTR = "data-misinfo-processed";

// Set up dwell / exposure tracking for a single tweet element.
// Uses IntersectionObserver to determine when a tweet is meaningfully visible.
function setupDwellObserver(tweetEl) {
  let visibleSince = null; // Timestamp when tweet became visible
  let hasSent = false;     // Guard to ensure we only process once

  // IntersectionObserver triggers when ~60% (threshold 0.6) of tweet area is visible.
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.target !== tweetEl) return; // Only handle our tweet

      if (entry.isIntersecting) {
        // Mark start of visibility window
        visibleSince = Date.now();
        // After short dwell window, confirm sustained visibility
        // Use a timeout slightly above the minimum required dwell to filter fast scrolls.
        setTimeout(() => {
          if (!hasSent && visibleSince !== null && (Date.now() - visibleSince) >= 1200) {
            hasSent = true;
            tweetEl.setAttribute(PROCESSED_ATTR, 'sent');
            handleTweet(tweetEl);
          }
        }, 1300); // Slightly longer than threshold to avoid borderline cases
      } else {
        // Visibility lost; reset until next intersect
        visibleSince = null;
      }
    });
  }, { threshold: 0.6 });

  observer.observe(tweetEl);
}

// Handle a tweet that has met dwell criteria (placeholder for sending to backend / analysis)
async function handleTweet(tweetEl) {
  // Extract text content; skip if empty/short.
  const text = extractTweetText(tweetEl);
  if (!text) return;
  console.log('[MisinfoGuardian] verifying tweet text:', text);

  try {
    const res = await fetch('http://localhost:8000/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    if (res.ok) {
      const data = await res.json();
      injectVerdictBadge(tweetEl, data);
    } else {
      console.error('[MisinfoGuardian] backend non-OK status', res.status);
      injectVerdictBadge(tweetEl, { verdict: 'Error', confidence: 0 });
    }
  } catch (err) {
    console.error('[MisinfoGuardian] backend error', err);
    injectVerdictBadge(tweetEl, { verdict: 'Error', confidence: 0 });
  }
}

// Extract visible tweet text from language-marked blocks.
function extractTweetText(tweetEl) {
  const parts = [];
  const textNodes = tweetEl.querySelectorAll('div[lang]');
  textNodes.forEach(node => {
    const t = node.innerText.trim();
    if (t) parts.push(t);
  });
  const combined = parts.join(' ').trim();
  if (!combined || combined.length < 10) return "";
  return combined;
}

// Map verdict to style info (background + emoji)
function verdictStyle(verdict) {
  switch (verdict) {
    case 'Accurate':
      return { bg: '#16a34a', emoji: '✅' };
    case 'Contradicted':
      return { bg: '#dc2626', emoji: '❌' };
    case 'Unverified':
      return { bg: '#facc15', emoji: '⚠️' };
    default:
      return { bg: '#6b7280', emoji: '❓' };
  }
}

// Inject a verdict pill badge into the tweet
function injectVerdictBadge(tweetEl, { verdict, confidence }) {
  try {
    if (tweetEl.querySelector('.misinfo-badge')) return; // Avoid duplicates
    const finalVerdict = verdict || 'Unverified';
    const styleInfo = verdictStyle(finalVerdict);
    const hasNumericConf = typeof confidence === 'number' && !isNaN(confidence);
    const pct = hasNumericConf ? Math.round(confidence * 100) : null;

    const badge = document.createElement('div');
    badge.className = 'misinfo-badge';
    badge.innerText = pct !== null
      ? `${styleInfo.emoji} ${finalVerdict} (${pct}%)`
      : `${styleInfo.emoji} ${finalVerdict}`;

    Object.assign(badge.style, {
      position: 'absolute',
      top: '8px',
      right: '8px',
      padding: '4px 8px',
      borderRadius: '999px',
      backgroundColor: styleInfo.bg,
      color: 'white',
      fontSize: '11px',
      fontWeight: '600',
      zIndex: 9999,
      boxShadow: '0 1px 3px rgba(0,0,0,0.3)',
      pointerEvents: 'none',
      fontFamily: 'system-ui,sans-serif'
    });

    // Ensure tweet positioned for absolute badge
    if (!tweetEl.style.position || tweetEl.style.position === 'static') {
      tweetEl.style.position = 'relative';
    }
    tweetEl.appendChild(badge);
  } catch (e) {
    console.error('[MisinfoGuardian] badge injection failed', e);
  }
}

// Find tweet elements under a given root and mark any unprocessed ones.
function findAndMarkTweets(root = document) {
  const tweets = root.querySelectorAll('article[data-testid="tweet"]');
  tweets.forEach(tweetEl => {
    if (!tweetEl.hasAttribute(PROCESSED_ATTR)) {
      tweetEl.setAttribute(PROCESSED_ATTR, 'pending');
      // Temporary logging to verify detection works.
      console.log('[MisinfoGuardian] New tweet detected', tweetEl);
      setupDwellObserver(tweetEl);
    }
  });
}

// Observe DOM mutations to catch dynamically loaded tweets (infinite scroll, navigation, etc.)
function startMutationObserver() {
  if (!document.body) return; // Safety: wait for body.
  const observer = new MutationObserver(mutations => {
    for (const mutation of mutations) {
      for (const node of mutation.addedNodes) {
        if (node.nodeType === Node.ELEMENT_NODE) {
          findAndMarkTweets(node);
        }
      }
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });
}

// Initial scan for already present tweets.
findAndMarkTweets(document);

// Start observing for future tweets (immediate if body exists, else after DOMContentLoaded).
if (document.body) {
  startMutationObserver();
} else {
  window.addEventListener('DOMContentLoaded', startMutationObserver, { once: true });
}
