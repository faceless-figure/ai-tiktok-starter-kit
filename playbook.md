# Playbook: AI try-on videos for a TikTok Shop fashion page

This file is the general method for making AI try-on videos with Higgsfield. It is written for you, the student's Claude.
The student's own character and rooms live in `memory/character.md` and `memory/house.md`. Read both before any prompt.
Newer notes in `memory/lessons.md` override this file. When you catch and fix a new mistake, log it there.

## 0. Core principles

- One page, one character, the same rooms. Every video must look like one real person filmed it on her own phone.
- Realism beats pretty. If a choice makes the shot prettier but more AI-looking, take the plainer shot.
- The product is exact: colour, cut, length and every detail match the listing photos. A recoloured or altered product is the worst failure.
- The viewer must know what is being sold in the first second.
- Fix problems in the prompt, not with regenerations. Target: no more than 1 render in 5 needs a trim.
- Small variance in the character's body or hair is fine. Retry only for: wrong product, near-copy of a reference, broken anatomy, morphing room, text or watermarks.

## 1. Product research basics

- Goal: products with many recent orders but few creators. Sellers' ads then pick up the few videos that exist.
- Ground truth is the TikTok app's own product commission details (7-day orders, creator count, stock). Data tools such as Kalodata are estimates with a 1-2 day lag; use them for shortlists only.
- Keep a product when: 7-day orders are about 100 or more, creators with sales are low (under roughly 200-300), orders are about 2x the creator count or more, the orders chart trends up, stock is healthy (about 800+ units), and commission is above zero.
- Lower filters catch products that just started moving with very few creators. That is good.
- Duplicate listings of a proven winner from another seller are good picks (fewer creators on that listing). Treat each as its own product and record that exact listing and seller, so the student links the right one.
- Skip lingerie, shapewear with body claims, trademarked character prints, and products that look like a famous character (generation gets blocked).
- Before writing anything, open the listing photos and list the signature details: waistband type, closures, pockets (yes or no, where), hood, length, back-only details, exact button count. Write the negatives too ("NO pockets, NO belt loops, pull-on").
- Save one clean product-only photo per colour you will use (flat lay or plain model shot).

## 2. The per-video pipeline

Order: product photos -> start still -> video from the still -> check -> trim and grade.

### 2.1 Start still

- Model `gpt_image_2_6`, quality `high`, resolution `2k`, aspect ratio `9:16`. Never use nano banana models for start stills.
- References go in medias with role `image_references`: the character sheet, the product photo(s) of the exact colour, the room reference. Optional: a framing reference.
- If the model refuses an image, retry once with softer wording and tell the student. Do not silently switch models.
- The still prompt contains, in this order:
  1. The character block from `memory/character.md`. If the sheet shows several views, say it is ONE person shown from several angles. Take face, hair, skin tone and figure from the sheet and nothing else; ignore the clothes on the sheet.
  2. The exact product description: colour with NOT-colours, every detail, the length, the negatives, and "copy EXACTLY from the product photo".
  3. The outfit: non-product pieces and shoes (see section 4.6).
  4. The place, from `memory/house.md`, plus a scale anchor ("counter at her hip height, doorway well above her head").
  5. The framing (see section 4).
  6. For mirror shots: the phone colour, "held upright, back facing the mirror, camera lenses in the top corner", and which hand holds it.
  7. "No text, captions or watermarks."
- The video model copies the still's look. A still that looks like a friend's real iPhone photo gives a real-looking video.
- Inspect every still hard before spending on video (section 6.1). Stills are cheap; video seconds are the real cost.

### 2.2 Video

- Model `wan3_0`, resolution `720p` native, aspect ratio `9:16`, `generate_audio: false`. No upscaler. Never 480p plus upscale (looks painted). 1080p costs too much.
- Medias: the start still as `image_references` #1, the product photo as `image_references` #2, and a muted reference clip as `video_references` only when copying a motion.
- Do NOT use `start_image` together with references. Wan rejects that combination.
- Duration: 5s per shot in a two-shot video, about 7s for a one-take. When a reference clip is attached, duration = the clip's length. Never pad past it; Wan invents filler motion.
- The video prompt contains:
  1. "Image 1 is the exact FIRST FRAME."
  2. The product line again, with negatives and length.
  3. Camera type: handheld mirror selfie, or static propped phone.
  4. A beat-by-beat timeline in seconds. She is already moving in the first second.
  5. The error locks (section 5.1).
  6. The tail: "Real candid iPhone footage, normal speed, crisp and sharp. One continuous take, nothing morphs. Exactly one person. No text, captions, watermarks. No audio."
- Movement comes from her body, not the camera. No slow motion, gimbal glide or orbiting camera. Fabric lags the body; hair swings and settles.
- Give each hand a concrete action on a visible object. Never write mental states ("searching", "looking for").
- Never write "lets go" or "drops" for a held prop. It vanishes.
- Run only a few jobs at a time (about 6 concurrent jobs causes rate-limit errors).

### 2.3 Finish

- Join shots, trim, grade and export as in section 7. Check the result as in section 6.

## 3. "Remake this" + a TikTok link

A near-copy of a reference video can earn an unoriginal-content violation. That is account damage, not wasted credits.

**Rule Zero: copy the motion, framing and pacing. Never the frame.** Think: a real affiliate saw a video, ordered the product, and remade it in her own life.

- Stays the same: the product (exact, from the listing), shot count and order, cut rhythm, pacing, type of movement, format (mirror stays mirror, POV stays POV), and how the garment is shown.
- Must change every time, without being asked:
  - Room: never the reference's place. Use your character's own rooms. An outdoor reference keeps an outdoor place of the same kind, but a different one.
  - Every non-product garment: a different TYPE of item, not the same one recoloured. A shade change is not a swap.
  - Hair, jewellery, nails, lighting, and camera height or distance where the format allows.
- Ban the reference's outfit by name in the prompt: colour, garment type, construction ("NO buttons, NO placket"), accessories.
- State each swap as a positive and a negative ("black ribbed tank, NOT cream, NOT a hoodie"). Naming what it must not be is what makes it stick.
- Do not copy the reference garment's details onto the product. Say "copy the product from the PRODUCT PHOTOS, NOT the motion clip" and ban details the reference garment has but the product does not (rips, distressing, logos, a different heel or collar, a different colourway).
- A one-line "different room" description does not work; the model keeps the reference layout. Supply your own room reference, or build the start still in your room first and pass it as image 1.
- Pre-submit test: laid beside the reference, does it read as a different person's video in the same format? If not, do not submit.

Preparing the reference clip:
- Mute it. Music in the audio triggers copyright blocks, which Higgsfield reports as "nsfw".
- Burned-in captions get copied onto walls. Pick a text-free segment, or go prompt-only. Blurring is risky: the blur patch itself can be copied.
- Logos and props in the reference get copied. Cut them out of the clip or go prompt-only.
- Quick-cut references (a hard cut every second or so) make Wan swap to the reference's outfit and person after the first cut. Go prompt-only: start still + product photo, beats written as one continuous take, cuts added in the edit.
- If the reference ends with the creator reaching for the phone to stop recording, trim that before upload.
- Pre-trim dragging or repeated parts before generating; you pay per second. Never trim the payoff or a feature beat.
- For the first render, the start still should copy the reference's framing and distance (how much of the frame she fills). Check that before rendering.

Which references are worth remaking:
- No talking to camera and no voiceover explaining the product. Music-only is fine.
- Short: 13s or less is ideal. Simple showcase motions: mirror try-on, fit check, turn to show the back, walk toward camera, hands on the product.
- Skip fast spins, heavy occlusion, several people, or clips where the product is barely visible.
- Prefer a recent top video of that exact product. If the product's selling point is on the front, use a front-facing format.

## 4. Format rules by product type

### 4.1 Shared rules

- She FILLS the frame: about 75-90% of frame height on full-body shots. Never a small figure in a big room. If the still shows her far away, regenerate the still.
- Two-shot is the main format: a 5s product CLOSE-UP, cut, then a 5s FULL-BODY outfit shot (about 10s total).
- Most two-shot videos are handheld mirror for both shots, with natural phone drift. Some are a static propped phone.
- SAME PHONE in both shots. Name the phone colour in both still prompts, or it changes colour at the cut.
- One-take alternative (about 7s): start very close on the garment, turn to show the fit, back up to head-to-toe, settle with a hip pop.
- One colour per video.
- Tight pieces sell the shape: every video of a tight garment includes a turn to the side or back. A front-only pose is not enough.
- Plan the side or back view in the first two thirds of the clip. Glitches tend to come late, so a late trim does not lose the key angle.
- Mirror selfies: turn only to a three-quarter back, toward the phone-holding side. Full back views come from a propped-phone shot or their own cut.
- Never show a tripod, ring light or second phone in a mirror shot.
- Requested styles copy the motion and how the garment is shown, but always in your character's own rooms.
- Never cover the product with a jacket or layer. A matching set is the whole outfit. Coverage is always complete: if the product is a top, she wears visible bottoms.

### 4.2 Bottoms (pants, jeans, leggings, skirts)

- Always two-shot or the one-take close-up to back-up. Every bottoms product also gets 1-2 tight mirror close-ups.
- Close-up shot: waist-down mirror selfie, phone at her chest, frame from ribs to floor, no face, the pants fill about 70% of the frame. Beats: weight on one hip, hand on waistband or into a pocket, slow quarter turn to show the seat and leg width, small step so the hem swings.
- Full-body shot: phone over her face, head to toe filling the frame, a step closer, a quarter turn.
- Shape-defining bottoms (barrel, flare, wide leg) need a full-body beat showing the whole silhouette.
- Lock the length in the garment text and the locks ("full-length, hem covers the ankle bone in every frame"). Otherwise pants turn capri-length when she steps back.
- Waistband-stretch move: ONLY for stretchy bottoms (leggings, pajamas, lounge pants, stretchy work pants). Jeans get it only if the listing says stretch or elastic. If unsure, no stretch; use a hand smoothing over the back pocket instead.
- Pockets, belt loops and buttons appear only if the listing has them. Pull-on waistbands get no belt.
- The top is cropped above or ends at the waistband so the waistband feature shows.

### 4.3 Tops, sweaters, jackets

- One-take close-up to back-up is the standard: start close on the garment, turn, back up, settle.
- Vary the hand beat by garment: knits = cuff or neckline, buttons and zips = a flat palm smoothing down the front.
- Printed tops: avoid mirror formats (the print reads backwards). Use a propped phone. Avoid rear-view formats for front-only prints.
- Outerwear: the listing decides open or closed, and it stays that way every frame. Name features like a hood, fur bands or the exact button count, and show them.
- Name the neckline exactly when a reference has a different collar.

### 4.4 Shoes

- Camera angled down, shoes big and centred. Small foot moves only; large pivots make fake-looking heels.
- Or two-shot: full body first (walk-up or turn, 3-4s), then a tight close-up.
- One shoe held = the other one on her foot, the same pair. Rotate a held shoe a quarter turn at most, hand on the sole the whole time.
- Shoes contrast with her skin. Every shoe is a complete shoe on a flat, unbroken floor. No bare feet when shoes are the product.
- Name the heel height and toe shape with negatives when similar shoes differ ("LOW stacked heel, NOT platform, NOT pointed toe").
- Colour variants: pass only photos of the exact colour. A reference photo in another colour recolours the shoe mid-clip.

### 4.5 Bags, accessories and sets

- Bags and accessories: the product fills the frame; hands hold it with real contact. Follow the listing for how it is carried. Linger 2-4s on a payoff (opening it, what fits inside).
- Hands-only product shots work best prompt-only: start still + product photo, beats in words.
- Sets: both halves always visible, nothing layered over them. Vary only hair, jewellery, shoes and light between versions.

### 4.6 Styling and prop logic

- Style non-product pieces like a real outfit that matches the product's vibe. Do not default to a plain tucked long-sleeve.
- Product type decides footwear: loungewear at home = socks or bare feet; dresses = slim heels or flats, no visible socks; activewear = clean trainers, never heels.
- Designer-looking styling accessories: write "a bag from a popular designer brand". Do not name a brand and do not write "no logo". The product itself never gets added logos.
- Props stay in the same hand. A prop is set down before any two-hand beat. One hand holds the phone, so only the other handles the product.
- Accessories and garment state (belt open, cardigan on, zip position) must be identical in every still for one video.

## 5. Mistakes and fixes

### 5.1 Error locks: append to every still and video prompt

- "Product details exactly as the listing photos. Add nothing they do not show: no extra buttons, pockets, zips, belts, logos or seams." Then the listing's own negatives.
- "The garment stays ONE colour (name it) for the whole clip."
- "She has exactly TWO hands and two arms in every frame, five fingers each. Both hands have the same nails."
- "Her RIGHT hand holds the phone for the entire clip, upright, camera lenses in the top corner. Her LEFT hand never touches the phone. The phone arm never crosses in front of her body." (Name the sides to match the still.)
- "Her free hand only smooths the fabric with a flat open palm or rests on her hip. She never pinches or twists zip pulls, ties or cords, and never reaches toward the camera."
- "Her body faces one consistent direction. When her back is to the camera we see the BACK of the garment, never front details on her back."
- "Her legs stay separate and never cross, overlap or pass through each other."
- "Her hair stays as in the first frame and only moves when her hand moves it."
- "ACCESSORIES (the only ones in the whole clip): list them. Nothing new appears on her wrists, hands, shoulders or neck."
- "GARMENT STATE (every frame): ..." and "GARMENT LENGTH: ..." and "ANGLES: ..." as the product needs.

### 5.2 Recurring failures

| # | What goes wrong | Fix |
|---|---|---|
| 1 | Fused or extra fingers, hand morphs | Flat-palm beats on large fabric areas or a hand on the hip. No fingertip work on zip pulls, ties or tails. |
| 2 | Third hand or arm | State the hand count. In a mirror selfie: phone hand + one free hand. Say where the free hand goes when it leaves the hip. Avoid back-to-mirror over-the-shoulder selfies. |
| 3 | Phone switches hands | Name the phone hand and say the other never touches it. Put the free hand on the hip opposite the phone in the still. |
| 4 | Phone upside down, floating or vanishing | "Upright, back to the mirror, lenses in the top corner." If the phone starts above the frame: "completely out of view, not even a corner". Avoid beats where the phone hand touches face or hair. |
| 5 | Back-only detail on the front, or front print on the back | Describe the plain side explicitly. Pick a format that faces the side with the detail. |
| 6 | Invented pockets, buttons, belts, logos | Write the specific negative from the listing every time. |
| 7 | Zip, belt or layer changes state with no hand on it | Lock the state in words and show it in every still. |
| 8 | Product colour drifts or flips | One-colour lock. Only same-colour reference photos. Name the reference's colour as banned if it differs. |
| 9 | Product picks up the reference garment's details | "Copy from product photos, not the motion clip" + ban the reference's extra details by name. |
| 10 | Giant or miniature scale | Scale anchor in the still prompt (counter at hip height, doorway above her head). |
| 11 | Subject far away | Fix the still: she fills 75-90% of the frame. Use a framing reference. Regenerate the still, not the video. |
| 12 | Dead first seconds | Write motion into second 0-1 ("already moving in frame 1"). Trim any dead start. |
| 13 | Close-up keeps backing up to full body | Make the back-up the LAST beat with no hold after it. "Exactly ONE small half-step back. Knees are the lowest thing ever visible." Render 5s. No full-distance video reference. |
| 14 | Pants turn capri, bare calves appear | Length lock in the garment text and the locks. |
| 15 | Mirror turn twists the body or pops the hair | Slow turn (2+ seconds), three-quarter only, toward the phone side, free hand stays on the hip. Full back views from a propped phone. |
| 16 | Object vanishes after she lets go | Say the prop stays put. Keep the same object in hand the whole clip. Never "drops" or "lets go". |
| 17 | Watch, bracelet or bag appears mid-clip | List the only accessories. Same props in every still. |
| 18 | Room or props change between start and end stills | Make the end still as an EDIT of the start still: same person, outfit, accessories, room and angle; change only distance and pose. |
| 19 | Listing-photo extras copied (model's tattoo, styled socks, other colour) | Reference only clean product-only photos of the exact colour. Check photos for tattoos and jewellery. Never use a past render as a framing reference. |
| 20 | Reference text, logos or props painted into the render | Clean the clip first or go prompt-only. |
| 21 | Outfit or person swaps after a cut | Prompt-only for multi-cut references; add cuts in the edit. |
| 22 | Face invented when the first frame hides her face | Add the character sheet as image 2: "when she turns, her face is image 2". |
| 23 | Flash pops on mid-clip | "Flash ON for the ENTIRE clip, already on in frame 1", and the start still shows strong flash glare. If it still pops, hard-cut there. |
| 24 | Legs pass through each other | Legs lock. Avoid leg-crossing beats. |
| 25 | Bottoms dropped or pulled low on bodysuit and back-turn clips | Lead the prompt with a coverage line: bottoms fully on and fastened in every frame. |
| 26 | "nsfw" or moderation block | Mute the reference first. Soften body wording, especially on mini lengths. One retry, then tell the student before spending more. |
| 27 | Filler motion or a teleporting hand late in the clip | Duration = reference length. For long clips, end the motion early and hold. |
| 28 | Non-product top comes back as the reference's top | Pick a top whose shape cannot be read as the reference's; state positives and negatives. |

## 6. Quality check

### 6.1 Check the still before any video credits

- Product matches the listing: colour, details, length, state, no invented extras.
- She fills the frame; scale against the room is believable.
- Two hands, five fingers; free hand on the hip opposite the phone.
- Phone: right colour, upright, lenses at the top.
- Accessories are exactly the planned ones; no logo on the product that the listing lacks.
- Start and end stills (if both are used) match in props, hair, room and angle.

### 6.2 What must pass before a video is handed to the student

- Run the kit's automated check against the product photo of the RIGHT colour. It must pass.
- Then check frames yourself. The automated checker misses things and also raises false alarms. Never write "checked" unless you looked.
- Make a contact sheet of the whole clip: 2 fps normally, 4 fps with larger tiles for anything with a turn. Go frame to frame for:
  - Hands: count them in every shot. Any hand or arm flag gets a full-size crop of each turn beat before you call it false.
  - Phone: which hand holds it in the FIRST vs the LAST frame (must match), no mid-clip handoff, never upside down.
  - Mirror logic: after a back turn, the same phone hand appears on the OPPOSITE side of the image. If it stays on the same side, the hand swapped.
  - Props: nothing appears, vanishes or changes hands. Zoom on every hand that holds a prop.
  - Garment state: zip, buttons, belt, hood, layers and logos do not change without a visible hand doing it.
  - Product: colour, length, and details on the correct side (front vs back).
  - Hair does not flip sides or change length untouched. Legs do not pass through each other.
  - Scale, flash state first vs last frame, and no text or watermark.
  - Step through short hand beats at full frame rate, not a sparse sheet.
- Checker false alarms to verify on frames before spending: anatomy flags on low-resolution copies, "same room as the reference" when only the KIND of place matches, styling pieces flagged as product mismatches, view-dependent details "missing". If the checker describes the reference instead of your render, rerun it without the reference.
- If a problem is real: trim around it if the key angles survive; re-render only when the product is wrong, the turn or reveal is broken, or anatomy is clearly off.
- A minor flaw of about a second that a viewer would not notice: accept it and note it. Do not spend credits on it.
- Never cut out the turn or back reveal to hide a defect. The turn is the feature.

## 7. Editing

- Length: every video is at least about 7s. Ideal is about 10-12s. Never over about 13-15s.
- Under 7s: slow the clip slightly (about 0.75x with frame interpolation) or extend with a continuation render from the last good frame (a simple full-body pose). Never fix a bad ending by trimming down to 4-5s.
- Trim only what drags or repeats, plus dead starts and glitches. Never trim a feature beat, a different angle or the payoff. A clip that ends on the reveal feels cut off; linger 2-4s on the payoff.
- If one render cannot hold all the beats, render two clips and cut them together. Prefer cuts between features over one long dragging take.
- A messed-up render is trimmed and used, not thrown away.
- Punch-in cut zooms (about 5-15%) ONLY on stable clips filmed from one spot, like a propped phone. Never on walking clips or moving handheld mirror clips; there use the grade and at most one slow subtle push-in.
- If the render already has cuts, add none. Keep any added cut at least 1.5s from an existing cut and leave at least 1s after every cut. After a cut zoom the frame holds still. When in doubt, grade only.
- No added shake or handheld sway in the edit.
- Grade every video: exposure -0.15 EV, contrast 0.97. No grain, no glow.
- Export 1080x1920 with a lanczos scale, constant 30 fps. A variable frame rate after a concat can make phones refuse the file.
- Export clean, with no text burned in. The student adds text in the TikTok editor.

## 8. Captions and on-screen text

Write these for the student to type by hand.

- NEVER a price, dollar amount, "$" or percent number anywhere: on-screen text, caption, hashtags, product name. Listings change price and a mismatch is a violation. Words without a number are fine ("cheap", "flash sale", "way cheaper than I thought").
- NEVER "before and after", "before/after", "wait for the after", "transformation" or `#beforeandafter`. Describe the product instead ("the tummy control on these").
- Product display names: no alcohol or drink words. "wine" is rejected; say burgundy or maroon.
- On-screen text: one or two short lines, each 28 characters or fewer. A reaction, not a pitch. No "link below" or shop language.
- Text sits around the vertical middle of the frame. Never at the top, never low where the caption and shop link cover it, never over her face or the product detail.
- Caption: a short lowercase hook in the page's own voice, 1-2 emojis after the hook, then 4-5 hashtags (product type, use or scene, discovery).
- Cute, not thirst-trap. Never break the illusion that she filmed it herself.
- Crop price badges out of product photos before using them as references, so no price leaks into a render.

## 9. Credit discipline

- Before generating, run the cost estimate tools and quote the student the total in credits and money, stills included. Do not guess from a balance change.
- Reference numbers to confirm with the estimate tools: a 2k still is about 2 credits; Wan 720p is about 1.75 credits per second.
- Check the still before spending on video. A wrong still always gives a wrong video.
- Never resubmit a job whose outcome is unknown. Wait for it or look it up first.
- Pre-trim reference clips before generating.
- Do not generate stills just for approval. Do not shorten videos or change formats to save credits; quote accurately and avoid remakes instead.
- Accept minor one-second flaws. Trim before you re-render.
- A content block: one retry with a fix, then stop and tell the student.
- After any new mistake, write the cause and the prompt fix into `memory/lessons.md` so it does not cost credits twice.
