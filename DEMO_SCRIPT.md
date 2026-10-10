# Demo Script

Follow this script to demonstrate the core capabilities of **Commitment Radar** during the hackathon judging process. This script is designed to run entirely locally with or without the external APIs configured.

## 1. Introduction (30 seconds)
"Hi, this is Commitment Radar. We make promises in conversations and meetings every day. Too often, we double-book ourselves or forget details. Commitment Radar listens to transcripts—like from an Omi wearable—and proactively surfaces conflicts before you drop the ball. It also uses Qloo to help you plan lifestyle commitments intelligently."

## 2. Walkthrough: The Dashboard (30 seconds)
1. Open the dashboard at `http://127.0.0.1:8000`.
2. Point out the **Memory status** and **Agent workflow** badges at the top right. 
3. *If you haven't configured API keys, emphasize:* "We built this to be robust. Because we haven't plugged in our API keys right now, it gracefully shifts to local fallback rules for parsing and memory, remaining fully functional!"

## 3. Ingesting a Promise (45 seconds)
1. In the **Quick Capture** text box, paste the following transcript:
   > "I promised John I would send the quarterly report by tomorrow."
2. Click **Analyze commitment**.
3. **Show the result:** Point to the newly added commitment on the left. It successfully extracted the task ("I would send the quarterly report by tomorrow"), the person ("John"), and inferred the deadline.

## 4. Demonstrating AI Conflict Detection (1 minute)
1. Now paste a conflicting transcript into the capture box:
   > "I will be travelling out of town all day tomorrow and won't have internet."
2. Click **Analyze commitment**.
3. **Show the result:**
   - Under **Conflict Radar**, a new high-severity alert appears.
   - It detected that you promised a deliverable tomorrow, but are now traveling without internet.
   - Highlight the **Draft Message**: The system drafted a polite follow-up message to send to John asking for an extension.

## 5. Qloo Lifestyle Suggestions (1 minute)
1. Next, let's ingest a lifestyle promise. Paste:
   > "I will take Sarah out to a nice restaurant for dinner on Friday."
2. Click **Analyze commitment**.
3. **Show the result:** 
   - A new commitment is tracked. 
   - A **Suggestion (PLACE)** appears on the right. 
   - *If Qloo is live:* Point out the actual restaurant recommendations pulled from Qloo.
   - *If Qloo is in fallback:* Show how the system correctly categorized the intent ("Place") but explains that the integration is unavailable.

## 6. Privacy & Conclusion (15 seconds)
1. Emphasize that memory is entirely under user control.
2. Click the **Forget all memory** button on the bottom left.
3. Show how the dashboard instantly clears, proving that vectors and logs are destroyed safely.
4. "That's Commitment Radar—turning everyday conversations into reliable accountability."

